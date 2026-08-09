import json
import tempfile
from pathlib import Path

CAPABILITIES = {
    "runtime": "python3",
    "stdlib": ["json", "tempfile", "pathlib"],
    "network": False,
    "absolute_paths": False,
}

def read_local_file_safely(file_path):
    """Read a local file, ensuring it exists and is a regular file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"missing input file: {file_path}")
    if not path.is_file():
        raise ValueError(f"not a regular file: {file_path}")
    return path.read_text(encoding="utf-8")

def main():
    # Create an owned temporary directory for the input fixture and output
    with tempfile.TemporaryDirectory(prefix="desert-island-") as owned_dir:
        owned = Path(owned_dir)
        input_file = owned / "input.txt"
        input_file.write_text("offline data: 42\n", encoding="utf-8")

        # Read the local file safely
        content = read_local_file_safely(input_file)

        # Write result to an owned output file (inspectable)
        output_file = owned / "result.json"
        result = {"content": content.strip(), "capabilities": CAPABILITIES}
        output_file.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")

        # Read back and print the result
        printed = json.loads(output_file.read_text(encoding="utf-8"))
        print(json.dumps(printed, sort_keys=True))

        # Cleanup: TemporaryDirectory removes only what we created

# Offline smoke test
assert CAPABILITIES["network"] is False
assert CAPABILITIES["absolute_paths"] is False
try:
    read_local_file_safely("/nonexistent/absolute/path")
    raise AssertionError("should have raised FileNotFoundError")
except FileNotFoundError as exc:
    assert "missing input file" in str(exc)

if __name__ == "__main__":
    main()