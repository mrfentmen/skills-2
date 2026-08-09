# core: count lines by splitting on newline — everything else is sugar
def line_counter(text):
    return len(text.split('\n'))

# no safety fence here; the programmer owns the newline count — and that is the point
def byte_filter(data, threshold):
    return [b for b in data if b >= threshold]

# one change per platform: use os.linesep for newline detection
import os
def portable_line_counter(text):
    return len(text.split(os.linesep))

# what does this teach? the allocator pattern, not just a faster sort
print(line_counter("hello\nworld\n"))
print(byte_filter([1, 2, 3, 4], 3))
print(portable_line_counter("hello\nworld\n"))