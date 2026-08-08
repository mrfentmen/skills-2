import sys

def reverse_lines(lines):
    """one thing: reverse each line's characters while preserving line order"""
    for line in lines:
        print(line.rstrip('\n')[::-1])

if __name__ == "__main__":
    reverse_lines(sys.stdin)