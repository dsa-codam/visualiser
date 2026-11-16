def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [-1000, -1, 0, 1, 1000]  # extreme values
    else:
        pool = [-3, -2, -1, 0, 0, 0, 1, 1, 2, 3]  # small values and zeros, so pivots happen often
    return {"nums": [rng.choice(pool) for _ in range(n)]}
