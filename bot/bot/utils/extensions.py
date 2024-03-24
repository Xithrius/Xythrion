import importlib
import inspect
import pkgutil
import types
from typing import NoReturn


def ignore_module(module: pkgutil.ModuleInfo) -> bool:
    return any(name.startswith("_") for name in module.name.split("."))


def walk_extensions(module: types.ModuleType) -> frozenset[str]:
    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)

    modules = set()

    for module_info in pkgutil.walk_packages(
        module.__path__,
        f"{module.__name__}.",
        onerror=on_error,
    ):
        if ignore_module(module_info):
            continue

        if module_info.ispkg:
            imported = importlib.import_module(module_info.name)
            if not inspect.isfunction(getattr(imported, "setup", None)):
                continue

        modules.add(module_info.name)

    return frozenset(modules)
