import json
import os
import tempfile
import sys
from pathlib import Path


class TodoStore:
    """
    The one way to persist todos. No sync, no tags, no due dates — cut.
    Reason: every extra field is a second product; a todo is a line of text.
    """

    def __init__(self, path: Path):
        self._path = path
        self._todos: list[str] = []
        self._load()

    def _load(self) -> None:
        # Empty state: missing file is not an error, it is a fresh start.
        if not self._path.exists():
            self._todos = []
            return
        try:
            raw = self._path.read_text(encoding="utf-8")
            data = json.loads(raw)
            # Boundary: reject malformed shapes, never guess.
            if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
                raise ValueError("corrupt store")
            self._todos = data
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            # Error state: fail loudly, never silently lose data.
            raise RuntimeError(f"cannot read store at {self._path}: {exc}") from exc

    def add(self, text: str) -> None:
        # Boundary: empty or whitespace-only todos are not todos.
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("todo cannot be empty")
        self._todos.append(cleaned)
        self._save()

    def remove(self, index: int) -> None:
        # Boundary: out-of-range is a user error, not a silent no-op.
        if not 0 <= index < len(self._todos):
            raise IndexError(f"no todo at index {index}")
        del self._todos[index]
        self._save()

    def list(self) -> list[str]:
        # Empty state: return a copy, never expose internal list.
        return list(self._todos)

    def _save(self) -> None:
        # Atomic write: never leave a half-written file on crash.
        temp_fd, temp_name = tempfile.mkstemp(dir=self._path.parent, suffix=".tmp")
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as handle:
                json.dump(self._todos, handle, ensure_ascii=False, indent=2)
            os.replace(temp_name, self._path)
        except OSError as exc:
            # Cleanup on failure: no orphan temp files.
            try:
                os.unlink(temp_name)
            except OSError:
                pass
            raise RuntimeError(f"cannot write store: {exc}") from exc


def demo() -> None:
    # End-to-end proof: create, persist, reload, remove, verify.
    with tempfile.TemporaryDirectory() as tmp:
        store_path = Path(tmp) / "todos.json"
        store = TodoStore(store_path)

        # Empty state first.
        assert store.list() == []

        # Add and persist.
        store.add("  polish the edges  ")
        store.add("cut the feature list")
        assert store.list() == ["polish the edges", "cut the feature list"]

        # Reload from disk — the file is the truth.
        reloaded = TodoStore(store_path)
        assert reloaded.list() == ["polish the edges", "cut the feature list"]

        # Remove and verify persistence.
        reloaded.remove(0)
        assert reloaded.list() == ["cut the feature list"]
        final = TodoStore(store_path)
        assert final.list() == ["cut the feature list"]

        # Error boundaries are first-class.
        try:
            final.add("   ")
            raise AssertionError("empty todo must fail")
        except ValueError:
            pass

        try:
            final.remove(5)
            raise AssertionError("out-of-range must fail")
        except IndexError:
            pass

        # Corrupt file is a loud error, not silent corruption.
        store_path.write_text("{not json", encoding="utf-8")
        try:
            TodoStore(store_path)
            raise AssertionError("corrupt store must fail")
        except RuntimeError:
            pass

        print("status=ok")
        print("todos=" + json.dumps(final.list()))
        print("cut=themes,sync,due_dates,search — every one a second product")


if __name__ == "__main__":
    demo()