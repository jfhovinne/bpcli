# bpcli

Uses [Dagger](https://dagger.io/) Python SDK to build an app with
[buildpacks](https://buildpacks.io/) and pushes the built image to a registry.

## Install

```
pip install bpcli
```

## Usage

Currently, only `build` command available.

```
Usage: bpcli build [OPTIONS] IMAGE

  Generate app image from source code using the provided image name.

Options:
  --builder TEXT             Builder image  [default:
                             paketobuildpacks/builder:base]
  --path TEXT                Path to app dir  [default: .]
  --log-level TEXT           Log level  [default: info]
  --docker-config-json TEXT  Path to docker config json file with registry
                             credentials
  --help                     Show this message and exit.
```

## Examples

```
bpcli build --path=/path/to/your/go/app <your image name>
```

Build a PHP application using the paketo full builder, with debug logs,
registry authentication and report containing the image tag and digest.

```
bpcli build \
  --path=/path/to/your/php/app \
  --builder=paketobuildpacks/builder:full \
  --log-level=debug foo/bar \
  --docker-config-json=$HOME/.docker/config.json > report.toml
```
