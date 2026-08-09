import os
import time
import hashlib
import sys

# (1) WHY does the watcher need a config file? Because PM guessed. Deleted: no config, no CLI args.
# (2) WHY does it need to watch directories recursively? The brief says "tiny". Deleted: recursion. Flat dir only.
# (3) WHY does it need to debounce events? We poll, so no event storm. Deleted: debounce logic.
# (4) WHY does it need to run callbacks? Print is the only consumer. Deleted: callback API, just print.

def file_sig(path):
    # physics: content hash is the ground truth for "changed". mtime lies (touch).
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def watch(directory, interval=1.0):
    # naive solution would use watchdog lib + event loop + async. Deleted: all deps, all async.
    # trade-off: polling costs CPU every interval, but for a tiny dir it's negligible vs. a 50MB dep tree.
    # trade-off: no atomic-rename detection (we hash content, so rename = delete+create, acceptable for demo).
    # trade-off: no symlink handling — symlinks are a security footgun, deleting that requirement is a win.
    known = {}
    while True:
        try:
            entries = [e for e in os.listdir(directory) if os.path.isfile(os.path.join(directory, e))]
        except FileNotFoundError:
            print(f"ERROR: {directory} does not exist")
            return
        current = {}
        for name in entries:
            path = os.path.join(directory, name)
            try:
                current[name] = file_sig(path)
            except (PermissionError, OSError):
                # why handle permission errors? because physics: files can be locked. We skip, not crash.
                continue
        # diff: added, removed, modified
        for name in current:
            if name not in known:
                print(f"ADDED: {name}")
        for name in known:
            if name not in current:
                print(f"REMOVED: {name}")
            elif known[name] != current[name]:
                print(f"MODIFIED: {name}")
        known = current
        time.sleep(interval)

if __name__ == "__main__":
    # hardcoded sample data, zero args, standalone
    test_dir = "_musk_watch_test"
    os.makedirs(test_dir, exist_ok=True)
    # seed a file
    with open(os.path.join(test_dir, "a.txt"), "w") as f:
        f.write("v1")
    # run watcher in a thread so we can mutate and then exit
    import threading
    stop = threading.Event()
    def run():
        watch(test_dir, interval=0.2)
    t = threading.Thread(target=run, daemon=True)
    t.start()
    time.sleep(0.5)
    # mutate: add, modify, delete
    with open(os.path.join(test_dir, "b.txt"), "w") as f:
        f.write("new")
    time.sleep(0.3)
    with open(os.path.join(test_dir, "a.txt"), "w") as f:
        f.write("v2")
    time.sleep(0.3)
    os.remove(os.path.join(test_dir, "b.txt"))
    time.sleep(0.5)
    # cleanup
    os.remove(os.path.join(test_dir, "a.txt"))
    os.rmdir(test_dir)
    print("DONE — all capabilities ran: add, modify, remove, no deps, no vaporware")