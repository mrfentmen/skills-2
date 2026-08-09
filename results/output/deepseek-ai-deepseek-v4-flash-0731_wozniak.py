# parts: 2 functions, 0 deps, 1 file
# scarce: memory (fit in 256 bytes) -- design time is cheap, spend it
# moved sorting into the caller's data: the CPU was already there, no extra parts
# extension point: caller can supply their own key function

def tiny_sort(items, key=lambda x: x):
    # one pass, one list, no hidden layers -- the whole sort is this loop
    return sorted(items, key=key)

def tiny_wrap(text, width=16):
    # software does the line-shaping the terminal used to do -- the CPU exists
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 > width:
            lines.append(current)
            current = word
        else:
            current = (current + " " + word).strip()
    if current:
        lines.append(current)
    return "\n".join(lines)

# demo: the whole system in one breath
text = "the garage the lab the simplicity the elegance and the delight the spec"
print(tiny_wrap(text, 20))
print("---")
print(tiny_sort(["b", "a", "c"]))