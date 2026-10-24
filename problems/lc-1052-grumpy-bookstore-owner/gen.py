def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        customers = [rng.choice([0, 1000]) for _ in range(n)]  # extreme values
    else:
        customers = [rng.choice([0, 0, 1, 2, 3, 5, 8]) for _ in range(n)]  # repeats and empty minutes
    grumpy = [rng.randint(0, 1) for _ in range(n)]
    return {"customers": customers, "grumpy": grumpy, "minutes": rng.randint(1, n)}
