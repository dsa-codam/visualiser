def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 10)
    if rng.random() < 0.3:
        nums = [1 + (i % 2) + 2 * rng.randint(0, 3) for i in range(n)]  # mostly alternating, so true answers happen
        if n > 1 and rng.random() < 0.5:
            nums[rng.randrange(n)] += 1  # one break
    else:
        nums = [rng.randint(1, 9) for _ in range(n)]
    queries = []
    for _ in range(rng.randint(1, 6)):
        a, b = rng.randrange(n), rng.randrange(n)
        queries.append([min(a, b), max(a, b)])
    return {"nums": nums, "queries": queries}
