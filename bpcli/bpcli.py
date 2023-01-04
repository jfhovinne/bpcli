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
@click.option('--builder', default="paketobuildpacks/builder:base", help='Builder image')
@click.option('--path', default=str(Path()), help='Path to app dir')
@click.argument('image')
async def build(image, builder, path):
    """Generate app image from source code using the provided image name."""
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        src = client.host().directory(Path(path).resolve())
        builder = (
            client.container().from_(builder)
            .with_mounted_directory('/src', src)
            .with_user('root')
            .with_exec(['chown', 'cnb:cnb', '/src'])
            .with_user('cnb')
            .with_exec(['bash', '-c', f'/cnb/lifecycle/creator -app=/src -cache-dir=/home/cnb {image}'])
        )
        out = await builder.stdout()

    print(out)


if __name__ == '__main__':
    cli()
