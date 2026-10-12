def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [-10**4, -1, 0, 1, 10**4]  # extreme values
    else:
        pool = [-5, -3, -2, -2, 0, 1, 2, 2, 3, 4]  # repeats, equal squares (-2 and 2), zeros
    return {"nums": sorted(rng.choice(pool) for _ in range(n))}
