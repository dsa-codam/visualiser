def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    p = rng.choice([0.0, 0.2, 0.5, 0.8, 1.0])  # chance of 'Y': all-N and all-Y strings happen too
    return {"customers": "".join("Y" if rng.random() < p else "N" for _ in range(n))}
