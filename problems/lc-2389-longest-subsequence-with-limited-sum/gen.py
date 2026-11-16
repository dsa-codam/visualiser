def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 10)
    m = rng.randint(1, 6)
    if rng.random() < 0.1:
        pool = [1, 10**6]  # extreme values
    else:
        pool = list(range(1, 10))
    nums = [rng.choice(pool) for _ in range(n)]
    queries = [rng.choice([1, 2, 5, 10, 20, 40, 10**6]) for _ in range(m)]
    return {"nums": nums, "queries": queries}
