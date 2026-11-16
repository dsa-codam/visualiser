def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [-10**6, -1, 0, 1, 10**6]  # extreme values
    else:
        pool = [-5, -3, -1, 0, 0, 1, 2, 3, 4, 10]  # negatives, zeros, repeats
    return {"nums": [rng.choice(pool) for _ in range(n)]}
