def gen(rng):
    """Random string inside the constraints: few distinct characters, so repeats are common."""
    n = rng.randint(0, 12)
    pool = "abcab A1 !"  # letters (both cases), a digit, spaces and a symbol
    if rng.random() < 0.2:
        pool = "abcdefgh"  # longer unique runs
    return {"s": "".join(rng.choice(pool) for _ in range(n))}
