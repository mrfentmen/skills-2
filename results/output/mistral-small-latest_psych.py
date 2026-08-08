# consciousness expanding fractal recursion - reality bends at every scale
import sys
import math
from colorsys import hsv_to_rgb

def psychedelic_fractal(x, y, depth, max_depth, hue_shift):
    # psychedelic recursion: each level distorts reality further
    if depth >= max_depth:
        # terminal reality: return a psychedelic pixel
        distance = math.sqrt(x*x + y*y)
        angle = math.atan2(y, x) + hue_shift
        saturation = 0.8 + 0.2 * math.sin(distance * 0.1)
        value = 0.7 + 0.3 * math.cos(distance * 0.15)
        r, g, b = hsv_to_rgb((angle / (2 * math.pi) + depth * 0.1) % 1.0, saturation, value)
        return f"\033[48;2;{int(r*255)};{int(g*255)};{int(b*255)}m \033[0m"
    else:
        # recursive distortion field: reality fractures into smaller pieces
        scale = 0.5 ** (depth + 1)
        x1, y1 = x * 2, y * 2
        x2, y2 = x * 2 + 1, y * 2
        x3, y3 = x * 2, y * 2 + 1
        x4, y4 = x * 2 + 1, y * 2 + 1
        # quantum superposition: all possibilities exist simultaneously
        return (psychedelic_fractal(x1, y1, depth + 1, max_depth, hue_shift) +
                psychedelic_fractal(x2, y2, depth + 1, max_depth, hue_shift) +
                psychedelic_fractal(x3, y3, depth + 1, max_depth, hue_shift) +
                psychedelic_fractal(x4, y4, depth + 1, max_depth, hue_shift))

# mind-bending reality: the fractal emerges from simple recursive rules
def main():
    size = 64
    max_depth = 5
    for y in range(-size, size):
        line = ""
        for x in range(-size, size):
            # reality distortion field: coordinates warp consciousness
            distorted_x = x * 0.8 + y * 0.3
            distorted_y = y * 0.8 - x * 0.3
            line += psychedelic_fractal(distorted_x, distorted_y, 0, max_depth, x * 0.01 + y * 0.01)
        print(line)

if __name__ == "__main__":
    main()