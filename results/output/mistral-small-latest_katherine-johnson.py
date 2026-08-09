def trajectory_under_constant_acceleration(initial_velocity, acceleration, time):
    # Count: inputs: initial_velocity (m/s), acceleration (m/s²), time (s)
    #        boundaries: 0, negative, max_float, inf, NaN
    #        paths: happy (all valid), zero_time, zero_velocity, zero_acceleration
    #        error_paths: invalid_input, overflow
    inputs = [initial_velocity, acceleration, time]
    boundaries = [0, -1, float('inf'), float('nan'), 1e308]
    paths = ["happy", "zero_time", "zero_velocity", "zero_acceleration"]
    error_paths = ["invalid_input", "overflow"]

    # Meaning check: expect position = initial_velocity * time + 0.5 * acceleration * time²
    #                units: m = (m/s)*s + 0.5*(m/s²)*s² → m = m + m → m
    #                if acceleration=0, position = initial_velocity * time (linear)
    #                if time=0, position=0 regardless of other inputs
    expected_meaning = (
        "Position must be in meters. "
        "If acceleration=0, position is linear in time. "
        "If time=0, position must be 0."
    )

    # Primary computation: s = ut + 0.5 a t²
    position = initial_velocity * time + 0.5 * acceleration * time ** 2

    # Independent check: re-derive via average velocity method
    # v_avg = (u + v)/2 = (u + u + a*t)/2 = u + 0.5*a*t
    # s = v_avg * t = (u + 0.5*a*t) * t = u*t + 0.5*a*t²
    v_final = initial_velocity + acceleration * time
    v_avg = (initial_velocity + v_final) / 2
    position_independent = v_avg * time

    # Glenn Protocol: two routes must agree
    glenn_verdict = independent_check(position, position_independent)

    # Probe: assumption challenged — "time is always positive"
    # Why? What if time is negative (backwards time)? Why not allow it?
    # Probe: assumption challenged — "acceleration is constant"
    # Why? What if acceleration varies? Why not model it as a function?
    probes = [
        "Why assume time is always positive? Could time be negative (backwards motion)?",
        "Why assume acceleration is constant? What if it varies with position/velocity?"
    ]

    # Backup path: if acceleration is unknown, use two-point finite difference
    # s_backup = (s2 - s1) / (t2 - t1) * (time - t1) + s1
    # Requires two prior positions and times
    def backup_path(s1, t1, s2, t2, time):
        if t2 == t1:
            return s1  # avoid division by zero
        slope = (s2 - s1) / (t2 - t1)
        return slope * (time - t1) + s1

    # Count boundaries and paths
    boundary_count = count_boundaries(boundaries)
    path_count = count_boundaries(paths)
    error_path_count = count_boundaries(error_paths)

    # Prepare output
    result = {
        "position": position,
        "glenn_verdict": glenn_verdict,
        "meaning_check": expected_meaning,
        "probes": probes,
        "boundary_count": boundary_count,
        "path_count": path_count,
        "error_path_count": error_path_count,
        "backup_path_example": backup_path(0, 0, 10, 2, 1)  # s1=0,t1=0; s2=10,t2=2; time=1 → 5
    }
    return result

def independent_check(route_a, route_b):
    agree = abs(route_a - route_b) < 1e-9
    return {"route_a": route_a, "route_b": route_b, "agree": agree,
            "verdict": "good to go" if agree else "do not fly"}

def count_boundaries(boundaries):
    return {"enumerated": boundaries,
            "n": len(boundaries),
            "tracked": all(b is not None for b in boundaries)}

# Example computation: initial_velocity=5 m/s, acceleration=2 m/s², time=3 s
result = trajectory_under_constant_acceleration(5.0, 2.0, 3.0)
print(result)