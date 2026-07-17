# AI Agent Instructions — XGIC CLI (core)

Public repository. Follow https://github.com/xgic/ai for multi-repo standards.

## Product

- **Brand:** XGIC CLI  
- **Package:** `xgic.cli` (distribution `xgic-cli`)  
- **Entrypoint:** `xgic`  
- **Architecture:** [ADR-0005](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md)

This repo is **thin core only**. Do **not** add Payload CMS, Docker Compose product orchestration, or other domain command implementations here.

| Concern | Package / repo |
|---------|----------------|
| Framework, env detect, output | **this repo** (`xgic.cli`) |
| Dev Container / Compose / lifecycle | `xgic.cli.dev` → https://github.com/xgic/dev-cli |
| Payload CMS project/setup/dev | `xgic.cli.payload` → https://github.com/xgic/payload-cms-cli |

After full modular cutover, living docs use **XGIC CLI only** (no long-term dual brand with transitional entrypoints).

## Layout

- `xgic.cli.app` — parser, entry-point plugins (`xgic.cli.commands`), dispatch  
- `xgic.cli.core.environment` — product-agnostic environment detection  
- `xgic.cli.utils.output` — Rich helpers  

## Rules

- Public-safe content only (no private hosts, private tracker IDs, internal paths).  
- Human code review in the GitHub UI before merge to `main`.  
- Dedicated issue-number branches; Conventional Commits.  
- Labels required on issues/PRs (`documentation`, `enhancement`, `bug`, `chore`, `standards` as appropriate).  
- Python 3.14+; Apache-2.0; root `CODEOWNERS` (`@xgic`).  
- No Makefiles for environment orchestration (CLI modules own that path).  
- Prefer pure, importable helpers; keep core free of product defaults (no Payload project names, no template compose project IDs).  
- **PyPI releases:** https://github.com/xgic/ai/blob/main/docs/python-package-release.md only (OIDC + `pypa/gh-action-pypi-publish`; `uv` build/smoke; no laptop publish).

## Local memory

Temporary status reports only under `.xgic/` (gitignored). Platform issues/PRs are authoritative.
