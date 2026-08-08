# Psychedelic recursion: each branch a mirror of the whole, a consciousness fractal
import math

def sierpinski_triangle(order, x, y, size, grid):
    # Recursive structure: the triangle contains itself at every scale
    if order == 0:
        # Base case: draw a single point of the mind-bending pattern
        for i in range(int(y), int(y + size)):
            for j in range(int(x), int(x + size)):
                if i < len(grid) and j < len(grid[0]):
                    grid[i][j] = 1
        return
    # Divide and conquer: split into three sub-triangles, each a smaller reality
    half = size / 2
    sierpinski_triangle(order - 1, x, y, half, grid)
    sierpinski_triangle(order - 1, x + half, y, half, grid)
    sierpinski_triangle(order - 1, x + half / 2, y + half, half, grid)

# Emergent complexity: a simple rule creates infinite self-similar detail
order = 5
size = 2 ** order
grid = [[0 for _ in range(size)] for _ in range(size)]

# Generate the fractal structure
sierpinski_triangle(order, 0, 0, size, grid)

# Visual output: color-cycling ASCII art that bends perception
colors = ['\033[91m', '\033[93m', '\033[92m', '\033[96m', '\033[94m', '\033[95m']
reset = '\033[0m'

for i in range(size):
    row = ''
    for j in range(size):
        if grid[i][j]:
            # Color cycling: each point shifts hue, a trippy wave of consciousness
            color = colors[(i + j) % len(colors)]
            row += color + '█' + reset
        else:
            row += ' '
    print(row)