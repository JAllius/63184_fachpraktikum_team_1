import importlib.util
from pathlib import Path

def loader(task: str, algorithm: str, base_dir: str = "./src/mlcore/presets"):
    """
    Dynamically load and return build_model() from
    presets/<task>/<algorithm>.py
    """
    path = Path(base_dir) / task / f"{algorithm}.py"
    if not path.exists():
        raise FileNotFoundError(f"Preset not found: {path}")

    # Create a specification of the module from */*.py
    spec = importlib.util.spec_from_file_location(f"{task}_{algorithm}", path)
    # Create an empty container/module from this specification
    module = importlib.util.module_from_spec(spec)
    # Run all top-level code to populate the module
    spec.loader.exec_module(module)

    # Check if build_model() exists in the created module
    if not hasattr(module, "build_model"):
        raise AttributeError(f"There is no function 'build_model()' in {path.name}")

    return module.build_model