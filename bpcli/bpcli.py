#!/usr/bin/env python3
"""
Python + Dagger + Buildpacks.
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
@click.option('--docker-config-json', default='', help='Path to docker config json file with registry credentials')
@click.argument('image')
async def build(image, builder, path, log_level, docker_config_json):
    """Generate app image from source code using the provided image name."""
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        src = client.host().directory(Path(path).resolve())
        cmd = f'/cnb/lifecycle/creator -app=/src -log-level={log_level} {image}'
        ctr = client.container().from_(builder)
        if docker_config_json:
            config_dir = client.host().directory(Path(docker_config_json).resolve().parent)
            config_json = config_dir.file(Path(docker_config_json).resolve().name)
            ctr = ctr.with_exec(['mkdir', '-p', '/home/cnb/.docker'])
            ctr = ctr.with_file('/home/cnb/.docker/config.json', config_json)
        bp = (
            ctr := ctr.with_mounted_directory('/src', src)
            .with_user('root')
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
