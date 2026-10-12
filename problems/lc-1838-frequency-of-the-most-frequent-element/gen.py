def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        return {"nums": [rng.choice([1, 100000]) for _ in range(n)], "k": rng.choice([1, 99999, 100000])}  # extreme values
    nums = [rng.choice([1, 2, 2, 3, 5, 5, 8, 13]) for _ in range(n)]  # repeats, not sorted
    return {"nums": nums, "k": rng.randint(1, 12)}
