def gen(rng):
    """Random string inside the constraints: few distinct letters, so long runs are common."""
    n = rng.randint(1, 12)
    pool = "AAABBC"
    if rng.random() < 0.2:
        pool = "ABCDEFGH"  # many letters, few repeats
    s = "".join(rng.choice(pool) for _ in range(n))
    return {"s": s, "k": rng.randint(0, min(n, 4)) if rng.random() < 0.9 else n}
