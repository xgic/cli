"""XGIC CLI core package (modular thin framework).

Namespace: ``xgic.cli`` (extended across domain packages via pkgutil).
Distribution: ``xgic-cli``
Console entry: ``xgic``

This package is **product-agnostic**:
- Framework: ``xgic.cli.app`` (plugins via entry points ``xgic.cli.commands``)
- Environment detection: ``xgic.cli.core.environment``
- Output helpers: ``xgic.cli.utils.output``

Domain logic lives in separate packages:
- Dev Container / Compose: ``xgic.cli.dev`` → https://github.com/xgic/dev-cli
- Payload CMS: ``xgic.cli.payload`` → https://github.com/xgic/payload-cms-cli
"""

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

__version__ = "0.2.0rc1"

__all__ = ["__version__"]
