def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        nums = [rng.choice([0, 1, 99999, 100000]) for _ in range(n)]  # extreme values
    else:
        nums = [rng.choice([0, 2, 3, 3, 5, 8, 8, 13, 20]) for _ in range(n)]  # repeats, not sorted
    return {"nums": nums, "k": rng.randint(1, n)}
