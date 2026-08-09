import json
import tempfile
from pathlib import Path

CAPABILITIES = {
    "runtime": "python3",
    "stdlib": ["json", "tempfile", "pathlib"],
    "network": False,
    "forbidden": ["network", "package_installation", "absolute_paths"]
}

def read_local_file_safely(input_path: str) -> str:
    """
    Read a local file safely using a temporary-artifact policy.
    Returns the file content as a string.
    """
    input_path_obj = Path(input_path)
    if not input_path_obj.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not input_path_obj.is_file():
        raise IsADirectoryError(f"Input path is a directory: {input_path}")

    with tempfile.TemporaryDirectory(prefix="desert-island-read-") as owned_dir:
        temp_output = Path(owned_dir) / "read_result.json"
        content = input_path_obj.read_text(encoding="utf-8")
        temp_output.write_text(content, encoding="utf-8")
        return temp_output.read_text(encoding="utf-8")

# Offline smoke test
if __name__ == "__main__":
    assert CAPABILITIES["network"] is False
    assert "absolute_paths" in CAPABILITIES["forbidden"]

    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as test_file:
        test_file.write("desert island test content")
        test_file_path = test_file.name

    try:
        result = read_local_file_safely(test_file_path)
        assert result == "desert island test content"
        print({"capabilities": CAPABILITIES, "status": "offline smoke test passed"})
    finally:
        Path(test_file_path).unlink(missing_ok=True)