"""
ascii_canvas.py, shared ASCII rendering helper for themed skills.

Drop-in module: copy it next to your code, or reference it from the code you
produce. Implements the line/circle/rect primitives that themed skills kept
reinventing, with ink-density characters (█ ▓ ▒ ░) for pressure-aware art.

Usage:
    from ascii_canvas import Canvas
    c = Canvas(40, 20, char=".")
    c.line(2, 2, 38, 18, pressure=0.8)
    c.circle(20, 10, 6)
    print(c.render())
"""
from __future__ import annotations

from typing import Optional

INK = (" ", "░", "▒", "▓", "█")  # 0..4 ink density


class Canvas:
    """A width x height character grid with classic drawing primitives."""

    def __init__(self, width: int = 40, height: int = 20, char: str = "."):
        self.width = width
        self.height = height
        self.grid = [[char for _ in range(width)] for _ in range(height)]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def set(self, x: int, y: int, char: Optional[str] = None,
            pressure: float = 1.0) -> None:
        """Set one cell. If char is None, map pressure 0..1 to ink density."""
        if not self.in_bounds(x, y):
            return
        if char is None:
            char = INK[min(len(INK) - 1, max(0, round(pressure * (len(INK) - 1))))]
        self.grid[y][x] = char

    def line(self, x1: int, y1: int, x2: int, y2: int,
             pressure: float = 1.0, char: Optional[str] = None) -> None:
        """Bresenham's line algorithm, the classic every theme redraws."""
        dx, dy = abs(x2 - x1), -abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx + dy
        while True:
            self.set(x1, y1, char=char, pressure=pressure)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x1 += sx
            if e2 <= dx:
                err += dx
                y1 += sy

    def circle(self, cx: int, cy: int, radius: int, pressure: float = 1.0,
               char: Optional[str] = None) -> None:
        """Midpoint circle algorithm."""
        x, y, err = radius, 0, 1 - radius
        while x >= y:
            for dx, dy in ((x, y), (y, x), (-y, x), (-x, y),
                           (-x, -y), (-y, -x), (y, -x), (x, -y)):
                self.set(cx + dx, cy + dy, char=char, pressure=pressure)
            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1

    def fill_rect(self, x0: int, y0: int, x1: int, y1: int,
                  pressure: float = 1.0, char: Optional[str] = None) -> None:
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                self.set(x, y, char=char, pressure=pressure)

    def clear(self, char: str = ".") -> None:
        self.grid = [[char for _ in range(self.width)] for _ in range(self.height)]

    def render(self) -> str:
        return "\n".join("".join(row) for row in self.grid)

    def __str__(self) -> str:
        return self.render()
