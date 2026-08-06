"""
box_drawing.py, shared decorative header helpers for themed skills.

Builds the ╔══╗ / ║ ║ / ╚══╝ headers that several themed skills kept
reimplementing by hand. Copy next to your code or reference from outputs.

Usage:
    from box_drawing import header, section, rule
    print(header("STEAM PRESSURES"))
    print(section("boiler one"))
    print(rule())
"""
from __future__ import annotations


def rule(char: str = "═", width: int = 60) -> str:
    """A horizontal rule."""
    return char * width


def header(title: str, width: int = 60) -> str:
    """A centered box-drawing header: ╔════ title ════╗"""
    mid = max(0, width - 2)
    line = "║" + f"{title}".center(mid) + "║"
    top = "╔" + "═" * mid + "╗"
    bottom = "╚" + "═" * mid + "╝"
    return "\n".join((top, line, bottom))


def section(title: str, width: int = 60) -> str:
    """A plain section divider: ── title ──────────────"""
    inner = f" {title} "
    dashes = max(0, width - len(inner))
    left = dashes // 2
    right = dashes - left
    return "─" * left + inner + "─" * right


def label(key: str, value: str, width: int = 60) -> str:
    """A key/value line aligned to a given width."""
    return f"  {key:<20} {value}"
