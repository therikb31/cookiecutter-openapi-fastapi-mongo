import pkgutil
import importlib

# Automatically import all modules in this package so that
# the API implementations defined in them are registered.
for _, module_name, _ in pkgutil.walk_packages(__path__):
    importlib.import_module(f"{__name__}.{module_name}")
