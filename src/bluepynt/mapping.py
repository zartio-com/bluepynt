import importlib
import importlib.util
import os
import sys
import traceback

NODE_MAP = {}


def load_nodes_from_module(module_path: str) -> bool:
    module_name = os.path.basename(module_path)
    if os.path.isfile(module_path):
        sp = os.path.splitext(module_path)
        module_name = sp[0]

    try:
        if os.path.isfile(module_path):
            module_spec = importlib.util.spec_from_file_location(module_name, module_path)
            module_dir = os.path.split(module_path)[0]
        else:
            module_spec = importlib.util.spec_from_file_location(module_name, os.path.join(module_path, "__init__.py"))
            module_dir = module_path

        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = module
        module_spec.loader.exec_module(module)

        if hasattr(module, "NODE_MAP") and getattr(module, "NODE_MAP") is not None:
            for name in module.NODE_MAP:
                NODE_MAP[name] = module.NODE_MAP[name]
            return True
        else:
            print(f"Skip {module_path} module for custom nodes due to the lack of NODE_MAP.")
            return False
    except Exception as e:
        print(traceback.format_exc())
        print(f"Cannot import {module_path} module for custom nodes:", e)
    return False

