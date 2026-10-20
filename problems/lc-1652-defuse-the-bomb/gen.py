def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    top = rng.choice([3, 100])  # small values give many repeats
    code = [rng.randint(1, top) for _ in range(n)]
    return {"code": code, "k": rng.randint(-(n - 1), n - 1)}
