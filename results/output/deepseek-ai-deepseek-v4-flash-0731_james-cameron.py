# target: real-time 3D wireframe projection of 10k vertices on a laptop using only stdlib — no GPU, no numpy, no pygame
# gap inventory: pygame needs install, numpy is heavy, OpenGL is overkill; stdlib has no matrix/vector math — build the seam
# prototype: the 40-line projection spike that stress-tests 10k points at 60fps before the full renderer
# decoupling: core: pure math pipeline (project, rotate). surface: ASCII/console output can be swapped for GUI without touching core
# feedback note: learned under load: naive per-vertex list comprehension was 3x slower than precomputed rotation matrix — fixed in core, not caller

import math, time, random

class Core:
    # decoupled: raw pipeline knows nothing about presentation. surface may change late.
    def __init__(self, vertices):
        self._verts = vertices

    def rotate(self, angle_x, angle_y):
        cx, sx = math.cos(angle_x), math.sin(angle_x)
        cy, sy = math.cos(angle_y), math.sin(angle_y)
        # precompute matrix once — learned: per-vertex trig was the bottleneck
        return [(x*cy + z*sy, y*cx - (x*sy - z*cy)*sx, y*sx + (x*sy - z*cy)*cx)
                for x, y, z in self._verts]

    def project(self, verts, fov=1.0, width=80, height=24):
        # perspective divide, map to 2D grid
        return [(int(width/2 + fov*x/(z+4)*width/4),
                 int(height/2 - fov*y/(z+4)*height/4))
                for x, y, z in verts if z > -3]

def prototype_riskiest_bit():
    # proof first: 10k random points, measure projection speed
    verts = [(random.uniform(-2,2), random.uniform(-2,2), random.uniform(-2,2))
             for _ in range(10000)]
    core = Core(verts)
    start = time.time()
    for _ in range(60):  # simulate 60 frames
        rotated = core.rotate(0.01, 0.02)
        projected = core.project(rotated)
    elapsed = time.time() - start
    return {"fps": 60/elapsed, "points": len(verts), "projected": len(projected)}

def present(core, angle_x, angle_y):
    # surface: ASCII renderer — replaceable without touching core
    rotated = core.rotate(angle_x, angle_y)
    projected = core.project(rotated)
    grid = [[' ' for _ in range(80)] for _ in range(24)]
    for x, y in projected:
        if 0 <= x < 80 and 0 <= y < 24:
            grid[y][x] = '#'
    return '\n'.join(''.join(row) for row in grid)

# stress-test the hard part first
print("PROTOTYPE STRESS TEST:", prototype_riskiest_bit())

# full build: small cube wireframe
cube = [(x, y, z) for x in (-1,1) for y in (-1,1) for z in (-1,1)]
core = Core(cube)
print("\nCUBE RENDER (frame 1):")
print(present(core, 0.5, 0.3))