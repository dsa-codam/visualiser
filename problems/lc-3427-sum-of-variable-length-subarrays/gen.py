def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [1, 1000]  # extreme values
    else:
        pool = [1, 1, 2, 3, 4, 5, 8, 20]  # short and long subarrays
    return {"nums": [rng.choice(pool) for _ in range(n)]}
