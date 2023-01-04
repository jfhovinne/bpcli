# bpcli

Inspired by [dagger-builpack](https://github.com/RealHarshThakur/dagger-builpack),
but in Python.

## Install

```
pip install -r requirements.txt
```

## Usage

Currently, only limited `build` command available.

```
./bpcli/bpcli.py build --help
Usage: bpcli.py build [OPTIONS] IMAGE

  Generate app image from source code using the provided image name.

Options:
  --builder TEXT  Builder image  [default: paketobuildpacks/builder:base]
  --path TEXT     Path to app dir  [default: .]
  --help          Show this message and exit.
```

## Examples

```
./bpcli/bpcli.py build --path=/path/to/your/go/app ttl.sh/yourgoappimage:1h
```

```
./bpcli/bpcli.py build --path=/path/to/your/php/app --builder=paketobuildpacks/builder:full ttl.sh/yourphpimage:2h
```
