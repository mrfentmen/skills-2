import sys

def uppercase_lines(lines):
    # one thing: read lines from stdin, write uppercase lines to stdout
    for line in lines:
        sys.stdout.write(line.upper())

if __name__ == "__main__":
    uppercase_lines(sys.stdin)