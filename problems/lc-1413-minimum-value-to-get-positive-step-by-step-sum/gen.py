def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [-100, -1, 0, 1, 100]  # extreme values
    else:
        pool = [-7, -5, -3, -2, -1, 0, 1, 2, 3, 4, 6]  # negatives, zeros, repeats
    return {"nums": [rng.choice(pool) for _ in range(n)]}
