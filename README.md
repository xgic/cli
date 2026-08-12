# XGIC CLI

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![CI](https://github.com/xgic/cli/actions/workflows/ci.yml/badge.svg)](https://github.com/xgic/cli/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/xgic-cli.svg)](https://pypi.org/project/xgic-cli/)
[![Python](https://img.shields.io/pypi/pyversions/xgic-cli.svg)](https://pypi.org/project/xgic-cli/)
[![Release](https://img.shields.io/github/v/release/xgic/cli)](https://github.com/xgic/cli/releases)

**The thin modular framework behind every `xgic` command—one brand for humans and AI agents.**

Namespace: **`xgic.cli`** · Console entry: **`xgic`** · Brand: **XGIC CLI only**
([ADR-0005](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md))

Standards hub: [xgic/ai](https://github.com/xgic/ai) ·
[README standards](https://github.com/xgic/ai/blob/main/docs/readme-standards.md)

---

## Vision

XGIC products share a **single CLI brand** (`xgic`) with a **thin core** and **domain modules**.
This repository is the core only: argument parsing, plugin loading, environment detection, and
output helpers. Payload, Dev Container lifecycle, and GitLab ops live in separate packages so each
module can version, test, and publish independently.

Humans get a stable `xgic --help` surface. AI agents (including Grok Build) get the same map in
[AGENTS.md](AGENTS.md)—no inventing Make targets or host-global tooling.

---

## Why this package exists

| Benefit | Detail |
|---------|--------|
| **One entrypoint** | `xgic` everywhere; modules register via entry points |
| **Product-agnostic core** | No Payload or Compose implementations here |
| **AI + human parity** | Same commands in README, AGENTS, and container images |
| **Release discipline** | Apache-2.0, Python 3.14+, RC → TestPyPI → PyPI |
| **Composable stack** | Domain packages depend on this core, not the reverse |

---

## Ecosystem

| Package | Namespace | Repository |
|---------|-----------|------------|
| **Core (this repo)** | `xgic.cli` | [xgic/cli](https://github.com/xgic/cli) |
| Dev Container / env | `xgic.cli.dev` | [xgic/dev-cli](https://github.com/xgic/dev-cli) |
| Payload CMS | `xgic.cli.payload` | [xgic/payload-cms-cli](https://github.com/xgic/payload-cms-cli) |
| GitLab ops | `xgic.cli.gitlab` | [xgic/gitlab-cli](https://github.com/xgic/gitlab-cli) |

Architecture: [ADR-0005](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md).

---

## Quick start

### Install (PyPI)

```bash
uv pip install xgic-cli
xgic --help
xgic --version
xgic info
```

### Development (editable)

```bash
uv pip install -e ".[dev]"
xgic --help
```

### Typical stack install

```bash
uv pip install \
  "xgic-cli>=0.2.0" \
  "xgic-dev-cli>=0.2.0" \
  "xgic-payload-cms-cli>=0.2.0"
xgic up --help
xgic payload --help
```

---

## Console commands (core)

| Command | Purpose |
|---------|---------|
| `xgic --help` | Top-level help (includes loaded plugins) |
| `xgic --version` | Core package version |
| `xgic info` | Detected execution environment summary |

Domain packages register additional subcommands via entry point group **`xgic.cli.commands`**.

---

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

---

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

---

## AI agent guidance

- Prefer **`xgic`** over ad-hoc scripts for environment and product ops.
- Install **core + needed domain modules**; do not reimplement lifecycle in the app repo.
- Destructive or credential-regenerating flows belong in domain modules with explicit confirmation.
- Follow hub [public-safe](https://github.com/xgic/ai/blob/main/docs/BASE-STANDARDS-FOR-ORCHESTRATED-REPOS.md)
  rules for any public GitHub issue/PR text.

---

## Status and publishing

**0.2.0 — thin core.** Framework + environment detection + output helpers. Domain modules ship
separately.

**Publishing to PyPI:** follow
[python-package-release.md](https://github.com/xgic/ai/blob/main/docs/python-package-release.md)
(TestPyPI RC + smoke → PyPI via OIDC Trusted Publishing; `uv` build/smoke).
Tags: `vX.Y.ZrcN` → TestPyPI; `vX.Y.Z` → PyPI. Requires GitHub Environments `testpypi` / `pypi`
and matching Trusted Publishers on the index.

### Requirements

- Python **3.14+**

---

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).  
Copyright form: `Copyright 2026 XGIC`.
