def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [1, 9999, 10000]  # extreme values
        threshold = rng.choice([0, 1, 9999, 10000])
    else:
        pool = list(range(1, 7))  # few distinct values → many equal averages
        threshold = rng.randint(0, 7)
    arr = [rng.choice(pool) for _ in range(n)]
    return {"arr": arr, "k": rng.randint(1, n), "threshold": threshold}
