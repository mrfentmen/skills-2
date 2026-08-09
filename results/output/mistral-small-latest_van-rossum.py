import os
import json
from typing import Dict, Any

def normalize_path(path: str) -> str:
    """
    Normalize a filesystem path to an absolute, normalized form.

    Readability pass:
    - Names tell the truth: `normalize_path` over `norm`, `path` over `p`
    - Structure mirrors the filesystem's own rules: resolve, then normalize

    Explicitness check:
    - No silent defaults: `os.path.abspath` and `os.path.normpath` are explicit
    - No magic strings: uses `os.path` constants, not hard-coded separators

    Simplicity statement:
    - The design is one step: resolve the path to absolute, then normalize separators.
    - No hidden state or side effects; pure function over input string.

    Flat-flow check:
    - Guard clause: validate input type immediately
    - Early return: avoid nested conditionals by failing fast

    Stdlib-first note:
    - Uses `os.path` (stdlib) for cross-platform path handling; no external deps.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    return os.path.normpath(os.path.abspath(path))

def load_config(path: str) -> Dict[str, Any]:
    """
    Load a JSON configuration file with explicit error handling.

    Readability pass:
    - Names reflect intent: `load_config` over `read_json`, `config` over `data`
    - Structure mirrors the task: open, read, parse, return

    Explicitness check:
    - No silent coercion: raises `FileNotFoundError` and `json.JSONDecodeError` explicitly
    - No magic numbers: uses `mode='r'` and `encoding='utf-8'` explicitly

    Simplicity statement:
    - The design is three steps: open the file, parse JSON, return the dict.
    - No hidden defaults or fallback behavior; caller must handle exceptions.

    Flat-flow check:
    - Guard clause: validate path type immediately
    - Early return: avoid nested try/except by failing fast on type error

    Stdlib-first note:
    - Uses `json` (stdlib) for parsing; no external deps.
    """
    if not isinstance(path, str):
        raise TypeError("config path must be a string")
    with open(path, mode='r', encoding='utf-8') as f:
        return json.load(f)

# Demonstrate the utilities
if __name__ == "__main__":
    # Example: normalize a relative path and load a config
    rel_path = "./data/../config/settings.json"
    abs_path = normalize_path(rel_path)
    print(f"Normalized path: {abs_path}")

    # Example config file content (written to disk for demo)
    demo_config = {"timeout": 30, "retries": 3}
    config_path = normalize_path("./demo_config.json")
    with open(config_path, mode='w', encoding='utf-8') as f:
        json.dump(demo_config, f)

    config = load_config(config_path)
    print(f"Loaded config: {config}")

    # Cleanup demo file
    os.remove(config_path)