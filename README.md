# XGIC CLI

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**XGIC CLI** is the modular command-line framework for XGIC tools.

This repository is the **thin core** package (`xgic.cli`, console entry **`xgic`**). It is **product-agnostic**: no Payload CMS or Dev Container orchestration implementations live here.

| Package | Namespace | Repository |
|---------|-----------|------------|
| Core (this repo) | `xgic.cli` | [xgic/cli](https://github.com/xgic/cli) |
| Dev Container / env | `xgic.cli.dev` | [xgic/dev-cli](https://github.com/xgic/dev-cli) |
| Payload CMS | `xgic.cli.payload` | [xgic/payload-cms-cli](https://github.com/xgic/payload-cms-cli) |

Architecture: [ADR-0005 - Modular XGIC CLI](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md).

Multi-repo standards: [xgic/ai](https://github.com/xgic/ai).

## Status

**0.2.0 — thin core.** Framework + environment detection + output helpers. Domain modules ship separately.

## Requirements

- Python **3.14+**

## Install (development)

```bash
python -m pip install -e ".[dev]"
xgic --help
xgic --version
xgic info
```

## Console commands (core)

| Command | Purpose |
|---------|---------|
| `xgic --help` | Top-level help |
| `xgic --version` | Package version |
| `xgic info` | Detected execution environment summary |

Domain packages register additional subcommands via entry point group **`xgic.cli.commands`**.

## Library API (core only)

```python
from xgic.cli.core import EnvironmentContext, EnvironmentType
from xgic.cli.utils.output import print_info, print_error
from xgic.cli.app import CommandContext, build_parser, main
```

| Module | Role |
|--------|------|
| `xgic.cli.app` | Parser, plugin loading, dispatch |
| `xgic.cli.core.environment` | Host / Dev Container / container detection |
| `xgic.cli.utils.output` | Rich console helpers |

## Plugin entry points

```toml
[project.entry-points."xgic.cli.commands"]
my_module = "my_package.cli:register"
```

```python
def register(subparsers):
    p = subparsers.add_parser("example", help="...")
    p.set_defaults(func=run_example)
```

Handlers may accept a `CommandContext` or `(args, env=...)`.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).  
Copyright form: `Copyright 2026 XGIC`.
