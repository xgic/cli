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
| Dev Container / Docker Compose / lifecycle | `xgic.cli.dev` → https://github.com/xgic/dev-cli |
| Payload CMS project/setup/dev | `xgic.cli.payload` → https://github.com/xgic/payload-cms-cli |

After full modular cutover, living docs use **XGIC CLI only** (no long-term dual brand with transitional entrypoints).

## Layout

- `xgic.cli.app` — parser, entry-point plugins (`xgic.cli.commands`), dispatch  
- `xgic.cli.core.environment` — product-agnostic environment detection  
- `xgic.cli.utils.output` — Rich helpers  

## Rules


**Public GitHub writes:** Before `gh issue create|edit`, `gh pr create|edit`, or any public comment on this repository, complete the **mandatory public-safe draft gate** in https://github.com/xgic/ai/blob/main/docs/BASE-STANDARDS-FOR-ORCHESTRATED-REPOS.md (fictional placeholders only; never name private hosts, private projects, or private tracker IDs). Optional helper from the hub clone: `python scripts/public-safe-scan.py path/to/draft.md`.
- Public-safe content only (no private hosts, private tracker IDs, internal paths).  
- Human code review in the GitHub UI before merge to `main`.  
- Dedicated issue-number branches; Conventional Commits.  
- **Labels (mandatory):** Every issue and pull request gets exactly one type label in the create call: `bug`, `enhancement`, `documentation`, `standards`, or `chore`. Welcome Discussion posts use `welcome` and `documentation`. Do not put scoped GitLab labels on GitHub. https://github.com/xgic/ai/blob/main/docs/community-health.md#labels-required  
- **Before close:** verify Markdown checklist items on issues/PRs; mark completed items `- [x]`; do not close with unchecked required items unless a human documents a waiver.  
- Python 3.14+; Apache-2.0; root `CODEOWNERS` (`@xgic`).  
- No Makefiles for environment orchestration (CLI modules own that path).  
- Prefer pure, importable helpers; keep core free of product defaults (no Payload project names, no template compose project IDs).  
- **PyPI releases:** https://github.com/xgic/ai/blob/main/docs/python-package-release.md only (OIDC + `pypa/gh-action-pypi-publish`; `uv` build/smoke; no laptop publish).

## Local memory

Temporary status reports only under `.xgic/` (gitignored). Platform issues/PRs are authoritative.

