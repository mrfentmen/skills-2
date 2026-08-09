import os
import sys

class ScopedFile:
    # owner: this instance owns the file descriptor fd; released on __exit__
    # invariant: fd is either a valid file descriptor or -1 (closed)
    #            if fd != -1, the file is open for the specified mode
    # lifetime binding: RAII — fd closed by __exit__ even if an exception escapes the with-block
    # overhead: zero — compiles to the same syscalls as hand-written open/close; no extra memory beyond the fd
    # guarantee: basic — if an operation raises, the file is still closed by __exit__

    def __init__(self, path, mode='r'):
        self.path = path
        self.mode = mode
        self.fd = -1
        self._open()

    def _open(self):
        flags = 0
        if 'r' in self.mode and '+' not in self.mode:
            flags |= os.O_RDONLY
        elif 'w' in self.mode:
            flags |= os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        elif 'a' in self.mode:
            flags |= os.O_WRONLY | os.O_CREAT | os.O_APPEND
        if '+' in self.mode:
            flags |= os.O_RDWR
        self.fd = os.open(self.path, flags)

    def read(self, n=-1):
        # basic guarantee: if read fails, fd still closed by scope exit
        if self.fd == -1:
            raise ValueError("file closed")
        if n == -1:
            n = os.path.getsize(self.path)
        data = b''
        while len(data) < n:
            chunk = os.read(self.fd, n - len(data))
            if not chunk:
                break
            data += chunk
        return data

    def write(self, data):
        # basic guarantee: if write fails, fd still closed by scope exit
        if self.fd == -1:
            raise ValueError("file closed")
        total = 0
        while total < len(data):
            written = os.write(self.fd, data[total:])
            if written == 0:
                break
            total += written
        return total

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.fd != -1:
            os.close(self.fd)
            self.fd = -1

def demo():
    # Write a small file, read it back, and ensure cleanup happens
    path = "stroustrup_demo.txt"
    try:
        with ScopedFile(path, 'w') as f:
            f.write(b"Hello, Stroustrup!\n")
        with ScopedFile(path, 'r') as f:
            print("Read:", f.read().decode())
    finally:
        if os.path.exists(path):
            os.unlink(path)

if __name__ == "__main__":
    demo()