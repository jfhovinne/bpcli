# bpcli

Uses [Dagger](https://dagger.io/) Python SDK to build an app with
[buildpacks](https://buildpacks.io/) and pushes the built image to a registry.

`bpcli` calls the Cloud Native Buildpacks [lifecycle](https://buildpacks.io/docs/concepts/components/lifecycle/)
commands from within a [builder](https://buildpacks.io/docs/concepts/components/builder/)
container to build or rebase images.

It does not rely on the [Pack CLI](https://buildpacks.io/docs/tools/pack/).

Also `bpcli` does not require Docker, [if a buildkit daemon is available](https://docs.dagger.io/1013/operator-manual/#custom-runtime-setup). This has currently been tested with [Podman](https://podman.io/).

## Install

```
pip install bpcli
```

## Usage

### Build

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
  --env TEXT                 Set an environment variable
  --help                     Show this message and exit.
```

#### Examples

```
bpcli build --path=/path/to/your/go/app <your image name>
```

Build a PHP application using the paketo full builder, with debug logs,
registry authentication and report containing the image tag and digest:

```
bpcli build \
  --path=/path/to/your/php/app \
  --builder=paketobuildpacks/builder:full \
  --log-level=debug foo/bar \
  --docker-config-json=$HOME/.docker/config.json > report.toml
```

Adding environment variables:

```
bpcli build --path=/path/to/your/app foo/bar --env FOO=bar --env BAR=foo
```

### Rebase

```
Usage: bpcli rebase [OPTIONS] IMAGE

  Rebase app image.

Options:
  --builder TEXT             Builder image  [default:
                             paketobuildpacks/builder:base]
  --log-level TEXT           Log level  [default: info]
  --docker-config-json TEXT  Path to docker config json file with registry
                             credentials
  --help                     Show this message and exit.
```

#### Example

```
bpcli rebase --log-level=debug --docker-config-json=$HOME/.docker/config.json foo/bar
```
