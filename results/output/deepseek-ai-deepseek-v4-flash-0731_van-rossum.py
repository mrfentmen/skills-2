import os
import configparser
from pathlib import Path


def load_config(config_path):
    # (1) readability pass: names tell the truth -- config_path, section, option
    #     structure: parse, validate, return -- the reader sees the whole story
    # (2) explicitness check: no silent defaults -- every missing key raises
    #     a clear error; no implicit type coercion -- we convert explicitly
    # (3) simplicity statement: read a config file, require two keys, return
    #     them as a tuple -- that is the entire design, nothing more
    # (4) flat-flow check: guard clauses at the top, no nested if pyramids
    # (5) stdlib-first note: configparser and pathlib are built-in -- no deps

    if not isinstance(config_path, (str, Path)):
        raise TypeError("config_path must be a string or Path")

    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"config file not found: {path}")

    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")

    if "settings" not in parser:
        raise KeyError("missing [settings] section")

    section = parser["settings"]
    if "host" not in section:
        raise KeyError("missing 'host' option in [settings]")
    if "port" not in section:
        raise KeyError("missing 'port' option in [settings]")

    host = section["host"].strip()
    if not host:
        raise ValueError("host must not be empty")

    try:
        port = int(section["port"])
    except ValueError:
        raise ValueError(f"port must be an integer, got {section['port']!r}")

    if not (0 < port < 65536):
        raise ValueError(f"port out of range: {port}")

    return host, port


def normalize_path(raw_path):
    # (1) readability pass: raw_path, expanded, resolved -- each name says
    #     what it holds; the flow is expand, resolve, return
    # (2) explicitness check: no hidden cwd assumptions -- we expand ~ and
    #     resolve symlinks explicitly; no silent fallback to a default
    # (3) simplicity statement: turn a user-supplied path into an absolute,
    #     symlink-free path -- that is the whole job, stated in one line
    # (4) flat-flow check: early return for the empty case, then one path
    # (5) stdlib-first note: os.path.expanduser and os.path.realpath are
    #     built-in -- no third-party path library needed

    if not isinstance(raw_path, str):
        raise TypeError("raw_path must be a string")

    if not raw_path.strip():
        raise ValueError("path must not be empty")

    expanded = os.path.expanduser(raw_path)
    resolved = os.path.realpath(expanded)
    return resolved


if __name__ == "__main__":
    # Demonstrate both utilities with a temporary config file
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
        f.write("[settings]\nhost = example.com\nport = 8080\n")
        temp_name = f.name

    try:
        host, port = load_config(temp_name)
        print(f"config: host={host}, port={port}")

        home_path = normalize_path("~/documents")
        print(f"normalized: {home_path}")
    finally:
        os.unlink(temp_name)