def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 10)
    if rng.random() < 0.1:
        pool = [-100000, -1, 0, 1, 100000]  # extreme values
    else:
        pool = [-5, -3, -1, 0, 1, 2, 4, 7]
    nums = [rng.choice(pool) for _ in range(n)]
    calls, args = ["NumArray"], [[nums]]
    for _ in range(rng.randint(1, 6)):
        a, b = rng.randrange(n), rng.randrange(n)
        calls.append("sumRange")
        args.append([min(a, b), max(a, b)])
    return {"calls": calls, "args": args}
