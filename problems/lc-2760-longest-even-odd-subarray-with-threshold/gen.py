def gen(rng):
    """Random input inside the constraints: small values, so parity repeats and threshold cuts are common."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        return {"nums": [rng.choice([1, 2, 99, 100]) for _ in range(n)], "threshold": rng.choice([1, 2, 99, 100])}  # extreme values
    nums = [rng.randint(1, 9) for _ in range(n)]
    return {"nums": nums, "threshold": rng.randint(1, 10)}
