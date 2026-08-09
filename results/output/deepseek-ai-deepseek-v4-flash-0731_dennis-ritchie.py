# core: a stream of bytes, a filter, a count — everything else is sugar
def count_lines(stream):
    # no safety fence here; the programmer owns the stream and its encoding — that is the point
    count = 0
    for chunk in iter(lambda: stream.read(4096), b''):
        count += chunk.count(b'\n')
    return count

# portability move: one change per platform — pass any binary stream, not a filename
import sys
print(count_lines(sys.stdin.buffer))