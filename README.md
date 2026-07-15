# XGIC CLI

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**XGIC CLI** is the modular command-line framework for XGIC tools and environment orchestration.

This repository is the **core** package (`xgic.cli`, console entry **`xgic`**). Domain modules (for example Dev Container / environment helpers and Payload CMS commands) will ship as separate packages under `xgic.cli.*`.

Architecture decision: [ADR-0005 — Modular XGIC CLI](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md).

Multi-repo standards: [xgic/ai](https://github.com/xgic/ai).

## Status

**Early scaffold (0.1.0).** Installable `xgic --help` / `xgic --version` only. Shared library extract and domain modules land in later releases.

## Requirements

- Python **3.14+**

## Install (development)

```bash
python -m pip install -e ".[dev]"
xgic --help
xgic --version
```

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).  
Copyright form: `Copyright 2026 XGIC`.
