def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [1, 2, 99999, 100000]  # extreme values
    else:
        pool = [1, 2, 2, 3, 4, 5, 6, 7, 8]  # odd and even, with repeats
    nums = [rng.choice(pool) for _ in range(n)]
    return {"nums": nums, "k": rng.randint(1, n)}
