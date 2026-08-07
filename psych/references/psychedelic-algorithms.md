# Psychedelic Algorithms Reference

A collection of mind-bending algorithms and implementations for psychedelic programming.

## Fractals

### Mandelbrot Set
```python
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

# ASCII visualization
for y in range(-2, 2, 0.1):
    for x in range(-2, 2, 0.05):
        c = complex(x, y)
        m = mandelbrot(c, 100)
        print(' ' if m == 100 else '*', end='')
    print()
```

### Julia Set
```python
def julia(c, max_iter):
    z = complex(-0.7, 0.27015)  # Classic Julia constant
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter
```

### Sierpinski Triangle
```python
def sierpinski(n):
    if n == 0:
        return ['*']
    else:
        prev = sierpinski(n-1)
        width = len(prev[0])
        result = []
        for line in prev:
            result.append(line + ' ' + line)
        for line in prev:
            result.append(' ' * width + line + ' ' * line)
        return result
```

### Koch Snowflake
```python
def koch(order, size):
    if order == 0:
        return [size]
    else:
        size3 = size / 3
        return koch(order-1, size3) + [size3] + koch(order-1, size3) + [size3] + koch(order-1, size3)
```

## Cellular Automata

### Conway's Game of Life
```python
import random

def create_grid(rows, cols):
    return [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

def count_neighbors(grid, x, y):
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = x + i, y + j
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbors += grid[nx][ny]
    return neighbors

def next_generation(grid):
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for x in range(rows):
        for y in range(cols):
            neighbors = count_neighbors(grid, x, y)
            if grid[x][y] == 1:
                new_grid[x][y] = 1 if neighbors in [2, 3] else 0
            else:
                new_grid[x][y] = 1 if neighbors == 3 else 0
    return new_grid
```

### Rule 110 (Elementary Cellular Automaton)
```python
def rule110(state):
    new_state = [0] * len(state)
    for i in range(1, len(state)-1):
        left = state[i-1]
        center = state[i]
        right = state[i+1]
        # Rule 110: 01101000 in binary
        pattern = (left << 2) | (center << 1) | right
        new_state[i] = (110 >> pattern) & 1
    return new_state
```

### Langton's Ant
```python
def langtons_ant(grid_size, steps):
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    x, y = grid_size//2, grid_size//2
    direction = 0  # 0=right, 1=down, 2=left, 3=up
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    
    for _ in range(steps):
        if grid[y][x] == 0:
            grid[y][x] = 1
            direction = (direction + 1) % 4
        else:
            grid[y][x] = 0
            direction = (direction - 1) % 4
        x = (x + dx[direction]) % grid_size
        y = (y + dy[direction]) % grid_size
    
    return grid
```

## Genetic Algorithms

### Basic Genetic Algorithm
```python
import random

def fitness(individual):
    # Maximize x^2 - 4x + 4 (parabola)
    return individual**2 - 4*individual + 4

def create_individual():
    return random.uniform(-10, 10)

def crossover(parent1, parent2):
    return (parent1 + parent2) / 2

def mutate(individual, rate=0.1):
    if random.random() < rate:
        return individual + random.gauss(0, 1)
    return individual

def genetic_algorithm(generations=100):
    population = [create_individual() for _ in range(20)]
    
    for gen in range(generations):
        # Evaluate fitness
        scored = [(ind, fitness(ind)) for ind in population]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Selection
        parents = [ind for ind, fit in scored[:10]]
        
        # Crossover and mutation
        children = []
        while len(children) < 20:
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            children.append(child)
        
        population = children
    
    # Return best
    best = max(population, key=fitness)
    return best, fitness(best)
```

### Neural Evolution (NEAT Simplified)
```python
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights_ih = [[random.random() for _ in range(hidden_size)] for _ in range(input_size)]
        self.weights_ho = [[random.random() for _ in range(output_size)] for _ in range(hidden_size)]
    
    def activate(self, x):
        return 1 / (1 + max(0, -x))  # Leaky ReLU
    
    def forward(self, inputs):
        hidden = []
        for i in range(len(self.weights_ih[0])):
            sum = 0
            for j in range(len(inputs)):
                sum += inputs[j] * self.weights_ih[j][i]
            hidden.append(self.activate(sum))
        
        outputs = []
        for i in range(len(self.weights_ho[0])):
            sum = 0
            for j in range(len(hidden)):
                sum += hidden[j] * self.weights_ho[j][i]
            outputs.append(self.activate(sum))
        
        return outputs
    
    def mutate(self, rate=0.1):
        for i in range(len(self.weights_ih)):
            for j in range(len(self.weights_ih[i])):
                if random.random() < rate:
                    self.weights_ih[i][j] += random.gauss(0, 0.5)
        for i in range(len(self.weights_ho)):
            for j in range(len(self.weights_ho[i])):
                if random.random() < rate:
                    self.weights_ho[i][j] += random.gauss(0, 0.5)
```

## Esoteric Languages

### Brainfuck Interpreter
```python
def brainfuck(code, input_stream=""):
    tape = [0] * 30000
    pointer = 0
    code_ptr = 0
    output = []
    input_ptr = 0
    
    while code_ptr < len(code):
        cmd = code[code_ptr]
        
        if cmd == '>':
            pointer = (pointer + 1) % 30000
        elif cmd == '<':
            pointer = (pointer - 1) % 30000
        elif cmd == '+':
            tape[pointer] = (tape[pointer] + 1) % 256
        elif cmd == '-':
            tape[pointer] = (tape[pointer] - 1) % 256
        elif cmd == '.':
            output.append(chr(tape[pointer]))
        elif cmd == ',':
            if input_ptr < len(input_stream):
                tape[pointer] = ord(input_stream[input_ptr])
                input_ptr += 1
        elif cmd == '[':
            if tape[pointer] == 0:
                # Find matching ]
                depth = 1
                while depth > 0:
                    code_ptr += 1
                    if code[code_ptr] == '[':
                        depth += 1
                    elif code[code_ptr] == ']':
                        depth -= 1
        elif cmd == ']':
            if tape[pointer] != 0:
                # Find matching [
                depth = 1
                while depth > 0:
                    code_ptr -= 1
                    if code[code_ptr] == ']':
                        depth += 1
                    elif code[code_ptr] == '[':
                        depth -= 1
        
        code_ptr += 1
    
    return ''.join(output)

# Hello World in Brainfuck
hello_world = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
print(brainfuck(hello_world))
```

### Befunge-93 Interpreter
```python
import random

def befunge(program):
    stack = []
    output = []
    pc = [0, 0]
    direction = [1, 0]  # right
    grid = [list(line) for line in program.split('\n')]
    width = max(len(row) for row in grid)
    height = len(grid)
    
    # Pad grid
    for row in grid:
        row.extend([' '] * (width - len(row)))
    
    string_mode = False
    
    while True:
        x, y = pc
        if y >= height or x >= width or x < 0 or y < 0:
            break
            
        char = grid[y][x]
        
        if string_mode:
            if char == '"':
                string_mode = False
            else:
                stack.append(ord(char))
        elif char == '"':
            string_mode = True
        elif char.isdigit():
            stack.append(int(char))
        elif char == '+':
            a, b = stack.pop(), stack.pop()
            stack.append(b + a)
        elif char == '-':
            a, b = stack.pop(), stack.pop()
            stack.append(b - a)
        elif char == '*':
            a, b = stack.pop(), stack.pop()
            stack.append(b * a)
        elif char == '/':
            a, b = stack.pop(), stack.pop()
            stack.append(b // a if a != 0 else 0)
        elif char == '%':
            a, b = stack.pop(), stack.pop()
            stack.append(b % a if a != 0 else 0)
        elif char == '!':
            stack.append(1 if stack.pop() == 0 else 0)
        elif char == '`':
            a, b = stack.pop(), stack.pop()
            stack.append(1 if b > a else 0)
        elif char == '>':
            direction = [1, 0]
        elif char == '<':
            direction = [-1, 0]
        elif char == '^':
            direction = [0, -1]
        elif char == 'v':
            direction = [0, 1]
        elif char == '?':
            direction = random.choice([[1,0], [-1,0], [0,1], [0,-1]])
        elif char == '_':
            direction = [-1, 0] if stack.pop() else [1, 0]
        elif char == '|':
            direction = [0, -1] if stack.pop() else [0, 1]
        elif char == ':':
            stack.append(stack[-1] if stack else 0)
        elif char == '\\':
            a, b = stack.pop() if stack else 0, stack.pop() if stack else 0
            stack.append(a)
            stack.append(b)
        elif char == '$':
            stack.pop()
        elif char == '.':
            output.append(str(stack.pop() if stack else 0))
        elif char == ',':
            output.append(chr(stack.pop() if stack else 0))
        elif char == '#':
            pc[0] += direction[0]
            pc[1] += direction[1]
        elif char == 'p':
            y, x, v = stack.pop(), stack.pop(), stack.pop()
            grid[y][x] = chr(v)
        elif char == 'g':
            y, x = stack.pop(), stack.pop()
            stack.append(ord(grid[y][x]))
        elif char == '&':
            stack.append(int(input()))
        elif char == '~':
            stack.append(ord(input()))
        elif char == '@':
            break
        
        pc[0] += direction[0]
        pc[1] += direction[1]
    
    return ''.join(output)
```

## Quines (Self-Replicating Programs)

### Python Quine
```python
s = 's = %r\nprint(s %% s)'
print(s % s)
```

### JavaScript Quine
```javascript
(function(){var a='(function(){var a=%22'+a+'%22;console.log(decodeURIComponent(a))})()';console.log(decodeURIComponent(a))})()
```

### C Quine
```c
#include<stdio.h>
int main(){char*q="#include<stdio.h>%cint main(){char*q=%c%s%c;printf(q,10,34,q,34);}";printf(q,10,34,q,34);}
```

## Visual Output Patterns

### ASCII Art Mandelbrot
```python
for y in range(-2, 2, 0.1):
    for x in range(-2, 2, 0.05):
        c = complex(x, y)
        m = mandelbrot(c, 100)
        print(' ' if m == 100 else '*', end='')
    print()
```

### Terminal Color Cycling
```python
import time

def color_cycle():
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
    reset = '\033[0m'
    
    for i in range(100):
        color = colors[i % len(colors)]
        print(f'{color}Psychedelic color {i}{reset}', end='\r')
        time.sleep(0.1)

color_cycle()
```

### Fractal Tree with Turtle Graphics
```python
import turtle

def draw_tree(t, length, angle):
    if length > 5:
        t.forward(length)
        t.right(angle)
        draw_tree(t, length - 15, angle)
        t.left(angle * 2)
        draw_tree(t, length - 15, angle)
        t.right(angle)
        t.backward(length)

# Setup turtle
t = turtle.Turtle()
t.left(90)
t.speed(0)
draw_tree(t, 100, 30)
turtle.done()
```

## Tips for Psychedelic Programming

1. **Start Simple**: Begin with basic fractals or cellular automata
2. **Add Complexity**: Layer multiple algorithms together
3. **Visualize**: Always show the output, not just the code
4. **Iterate**: Run the algorithm multiple times to see evolution
5. **Combine**: Mix different paradigms (fractals + cellular automata)
6. **Document**: Explain the mind-bending parts
7. **Share**: Psychedelic code is meant to be seen and experienced

Remember: The goal is to create code that makes people question reality, see patterns everywhere, and appreciate the infinite complexity that can arise from simple rules.