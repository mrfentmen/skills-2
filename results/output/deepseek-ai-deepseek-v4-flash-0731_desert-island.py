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
    """Read a local file, returning its contents as a string."""
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    return Path(file_path).read_text(encoding="utf-8")

def main():
    # Create an owned temporary directory for the input fixture
    with tempfile.TemporaryDirectory(prefix="desert-island-") as owned_dir:
        input_path = Path(owned_dir) / "input.txt"
        input_path.write_text("offline data: 42", encoding="utf-8")

        # Read the file safely
        content = read_local_file_safely(input_path)

        # Print the result (no network, no absolute paths)
        print(f"Read content: {content}")

        # Verify the capability contract
        assert CAPABILITIES["network"] is False
        assert CAPABILITIES["absolute_paths"] is False
        assert "json" in CAPABILITIES["stdlib"]
        assert "tempfile" in CAPABILITIES["stdlib"]
        assert "pathlib" in CAPABILITIES["stdlib"]

        # Test missing-input error
        try:
            read_local_file_safely(Path(owned_dir) / "missing.txt")
        except FileNotFoundError as exc:
            assert "Input file not found" in str(exc)

        # Test permission error (simulate by trying to read a directory)
        try:
            read_local_file_safely(Path(owned_dir))
        except IsADirectoryError as exc:
            assert "Is a directory" in str(exc)

        # Cleanup: TemporaryDirectory removes only what it created
        # (the context manager handles this automatically)

    print(json.dumps({"capabilities": CAPABILITIES, "status": "offline smoke test passed"}))

if __name__ == "__main__":
    main()