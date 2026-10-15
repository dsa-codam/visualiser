def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    white = rng.choice([0.0, 0.3, 0.5, 0.7, 1.0])  # sometimes all 'B' or all 'W'
    blocks = "".join('W' if rng.random() < white else 'B' for _ in range(n))
    return {"blocks": blocks, "k": rng.randint(1, n)}
