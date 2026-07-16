# XGIC CLI

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**XGIC CLI** is the modular command-line framework for XGIC tools and environment orchestration.

This repository is the **core** package (`xgic.cli`, console entry **`xgic`**). Domain modules (for example Dev Container / environment helpers and Payload CMS commands) will ship as separate packages under `xgic.cli.*`.

Architecture decision: [ADR-0005 - Modular XGIC CLI](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md).

Multi-repo standards: [xgic/ai](https://github.com/xgic/ai).

## Status

**0.2.0 — shared core library extract (Phase B2).** Installable framework + importable core APIs. Domain subcommands (lifecycle, Payload CMS, etc.) land in later modules. Product templates may still ship a transitional in-tree surface until hard cutover.

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

Domain modules register additional subcommands via the entry point group **`xgic.cli.commands`**.

## Library API (shared core)

Importable surface for modules and automation:

```python
from xgic.cli.core import EnvironmentContext, DockerComposeController
from xgic.cli.core.project import load_create_payload_config, ensure_payload_project
from xgic.cli.utils.output import print_info, print_error
```

| Module | Role |
|--------|------|
| `xgic.cli.core.environment` | Host / Dev Container / container detection |
| `xgic.cli.core.docker` | Docker Compose controller (subprocess layer) |
| `xgic.cli.core.project` | Project ensure / create helpers (Payload CMS-oriented defaults) |
| `xgic.cli.utils.output` | Rich console helpers |
| `xgic.cli.app` | Parser, plugin loading, dispatch |

## Plugin entry points

Packages can register CLI subcommands:

```toml
[project.entry-points."xgic.cli.commands"]
my_module = "my_package.cli:register"
```

```python
def register(subparsers):
    p = subparsers.add_parser("example", help="...")
    p.set_defaults(func=run_example)
```

Handlers may accept a `CommandContext` or legacy-style `(args, env=, docker=)`.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).  
Copyright form: `Copyright 2026 XGIC`.
