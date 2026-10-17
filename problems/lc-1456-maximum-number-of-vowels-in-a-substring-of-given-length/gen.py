def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    pool = rng.choice(["aeiou", "bcdxyz", "aeioubcdxz", "aaxz"])  # sometimes only vowels or no vowels
    s = "".join(rng.choice(pool) for _ in range(n))
    return {"s": s, "k": rng.randint(1, n)}
