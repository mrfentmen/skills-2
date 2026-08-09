import json
import os
import tempfile
from typing import Dict, List, Optional

# Product promise: A one-command todo store that feels effortless because it never asks the user to remember where the file is or how to format it.

# Cut list:
# - GUI: adds noise, maintenance, and a second product. Users only need CLI.
# - Tags/Categories: dilutes focus on the essential todo list. Users can put context in the title.
# - Due dates: another abstraction that complicates the core promise. Users can write dates in titles if needed.
# - Sync/Cloud: out of scope for a local tool. Users who need sync can use a file sync service externally.
# - Undo/Redo: adds complexity and state management. Users can edit the file directly if they make a mistake.

class TodoStore:
    def __init__(self, path: Optional[str] = None):
        self.path = path or os.path.join(tempfile.gettempdir(), "the_one_way_todos.json")
        self.todos: List[Dict[str, str]] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self.path, "r") as f:
                self.todos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.todos = []

    def _save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.todos, f)

    def add(self, title: str) -> None:
        if not title.strip():
            raise ValueError("Title cannot be empty")
        self.todos.append({"title": title.strip(), "done": False})
        self._save()

    def list(self) -> List[Dict[str, str]]:
        return self.todos.copy()

    def done(self, index: int) -> None:
        if index < 0 or index >= len(self.todos):
            raise IndexError("Invalid todo index")
        self.todos[index]["done"] = True
        self._save()

    def delete(self, index: int) -> None:
        if index < 0 or index >= len(self.todos):
            raise IndexError("Invalid todo index")
        del self.todos[index]
        self._save()

    def clear(self) -> None:
        self.todos = []
        self._save()

def demo() -> None:
    # Use a temp file so the demo works from any directory
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        store = TodoStore(tmp_path)

        # Empty state
        print("Empty state:", store.list())

        # Add todos
        store.add("Buy milk")
        store.add("Call mom")
        print("After adding two:", store.list())

        # Mark one done
        store.done(0)
        print("After marking first done:", store.list())

        # Delete one
        store.delete(1)
        print("After deleting second:", store.list())

        # Clear all
        store.clear()
        print("After clearing:", store.list())

        # Error state: invalid index
        try:
            store.done(0)
        except IndexError as e:
            print("Error state (invalid index):", e)

        # Error state: empty title
        try:
            store.add("")
        except ValueError as e:
            print("Error state (empty title):", e)

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    demo()