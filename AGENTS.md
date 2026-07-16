# AI Agent Instructions — XGIC CLI (core)

Public repository. Follow https://github.com/xgic/ai for multi-repo standards.

## Product

- **Brand:** XGIC CLI  
- **Package:** `xgic.cli` (distribution `xgic-cli`)  
- **Entrypoint:** `xgic`  
- **Architecture:** [ADR-0005](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md)

After full modular cutover, living docs use **XGIC CLI only** (no long-term dual brand with transitional entrypoints).

## Layout

- `xgic.cli.app` — parser, entry-point plugins (`xgic.cli.commands`), dispatch  
- `xgic.cli.core` — shared library (`environment`, `docker`, `project`)  
- `xgic.cli.utils.output` — Rich helpers  
- Domain commands live in separate packages (B3+), not in this core repo long-term

## Rules

- Public-safe content only (no private hosts, private tracker IDs, internal paths).  
- Human code review in the GitHub UI before merge to `main`.  
- Dedicated issue-number branches; Conventional Commits.  
- Labels required on issues/PRs (`documentation`, `enhancement`, `bug`, `chore`, `standards` as appropriate).  
- Python 3.14+; Apache-2.0; root `CODEOWNERS` (`@xgic`).  
- No Makefiles for environment orchestration (CLI modules own that path).  
- Prefer pure, importable helpers in `core/` over shell scripts.

## Local memory

Temporary status reports only under `.xgic/` (gitignored). Platform issues/PRs are authoritative.
