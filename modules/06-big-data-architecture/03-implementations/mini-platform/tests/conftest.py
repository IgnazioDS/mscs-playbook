from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


MINI_PLATFORM_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    module_path = MINI_PLATFORM_ROOT / relative_path
    service_root = module_path.parents[1]
    shared_root = MINI_PLATFORM_ROOT / "shared"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")

    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            sys.modules.pop(name, None)

    if str(service_root) in sys.path:
        sys.path.remove(str(service_root))
    if str(shared_root) in sys.path:
        sys.path.remove(str(shared_root))
    sys.path.insert(0, str(shared_root))
    sys.path.insert(0, str(service_root))

    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(module_name, None)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def load_service_module():
    return _load_module
