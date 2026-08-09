import math
import random

# hypothesis: a projectile launched at 45 degrees with initial speed v0
# will have maximum range v0^2 / g (ignoring air resistance), and the
# measured range from a numerical simulation will match this within 1%.

G = 9.81  # m/s^2, standard gravity

def simulate_range(v0, angle_deg, dt=0.001):
    """Numerically integrate projectile motion until y < 0."""
    angle = math.radians(angle_deg)
    vx = v0 * math.cos(angle)
    vy = v0 * math.sin(angle)
    x, y = 0.0, 0.0
    while y >= 0:
        x += vx * dt
        y += vy * dt
        vy -= G * dt
    return x

# control: known-good baseline — analytic range at 45 degrees
v0 = 20.0
control_range = v0**2 / G  # 40.77 m

# falsifiable test: if simulation deviates from control by >1%, hypothesis is wrong
tolerance = 0.01 * control_range
measured_range = simulate_range(v0, 45.0)

# lab record: log multiple runs with different dt to check convergence
lab_log = []
for dt in [0.01, 0.001, 0.0001]:
    r = simulate_range(v0, 45.0, dt)
    lab_log.append(f"dt={dt}: range={r:.4f} m")

# failed attempt: try a wrong angle (30 deg) to confirm the test can fail
wrong_angle_range = simulate_range(v0, 30.0)
wrong_angle_expected = v0**2 * math.sin(math.radians(60)) / G

# responsibility: verify before shipping — someone might use this for real physics
verified = abs(measured_range - control_range) <= tolerance

print("=== PROJECTILE RANGE EXPERIMENT ===")
print(f"hypothesis: max range at 45° = v0^2/g = {control_range:.2f} m")
print(f"falsifiable test: simulation must be within ±{tolerance:.2f} m of control")
print("lab record:")
for entry in lab_log:
    print(f"  {entry}")
print(f"  measured at 45°: {measured_range:.4f} m")
print(f"  failed attempt (30°): {wrong_angle_range:.4f} m vs expected {wrong_angle_expected:.4f} m")
print(f"control: analytic range = {control_range:.2f} m")
print(f"responsibility: verified={verified} — result safe to use for demo only, not flight planning")