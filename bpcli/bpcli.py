#!/usr/bin/env python3
"""
Build apps with buildpacks and Dagger
"""

import asyncclick as click
import dagger
import sys
from pathlib import Path


@click.group()
def cli():
    pass


@cli.command(context_settings={'show_default': True})
@click.option('--builder', default='paketobuildpacks/builder:base', help='Builder image')
@click.option('--path', default=str(Path()), help='Path to app dir')
@click.option('--log-level', default='info', help='Log level')
@click.option('--docker-config-json', help='Path to docker config json file with registry credentials')
@click.option('--env', help='Set an environment variable', multiple=True)
@click.argument('image')
async def build(image, builder, path, log_level, docker_config_json, env):
    """Generate app image from source code using the provided image name."""
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        src = client.host().directory(str(Path(path).resolve()))
        cmd = f'/cnb/lifecycle/creator -app=/src -log-level={log_level} {image}'
        ctr = client.container().from_(builder)
        # Docker config
        if docker_config_json:
            config_dir = client.host().directory(str(Path(docker_config_json).resolve().parent))
            config_json = config_dir.file(str(Path(docker_config_json).resolve().name))
            ctr = ctr.with_exec(['mkdir', '-p', '/home/cnb/.docker'])
            ctr = ctr.with_file('/home/cnb/.docker/config.json', config_json)
        # Environment variable(s) to platform/env files
        ctr = ctr.with_user('root')
        for e in env:
            var = e.split('=')[0]
            val = e.split('=')[1]
            ctr = ctr.with_exec(['bash', '-c', f'echo -n "{val}" > /platform/env/{var}'])
        # Lifecycle
        bp = (
            ctr := ctr.with_mounted_directory('/src', src)
            .with_exec(['chown', '-R', 'cnb:cnb', '/home/cnb'])
            .with_exec(['chown', '-R', 'cnb:cnb', '/src'])
            .with_user('cnb')
            .with_exec(['bash', '-c', cmd])
        )
        report = ctr.file('/layers/report.toml')
        stdout = await report.contents()

    print(stdout)


if __name__ == '__main__':
    cli()
