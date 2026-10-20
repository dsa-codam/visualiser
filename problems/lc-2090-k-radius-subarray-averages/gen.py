def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    top = rng.choice([5, 100000])  # small values give many repeats
    nums = [rng.randint(0, top) for _ in range(n)]
    k = rng.choice([0, rng.randint(0, 3), rng.randint(0, n), rng.randint(0, 100000)])  # sometimes 2k + 1 > n
    return {"nums": nums, "k": k}
