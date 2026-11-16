class Solution:
    def bestClosingTime(self, customers: str) -> int:
        penalty = 0  # penalty if the shop closes at hour 0: every 'Y' is missed  # @a:init
        # @trace-begin
        best = None
        best_hour = None
        n = len(customers)

        def cost_cells(j):
            # hours that add to the penalty when the shop closes at hour j
            return {p: "+1" for p in range(n) if (p < j and customers[p] == 'N') or (p >= j and customers[p] == 'Y')}

        def snap(j, close, roles=None, flash=None, counted=None):
            tags = cost_cells(close) if close is not None else {}
            if counted is not None:  # first pass: only the 'Y' counted so far
                tags = {p: "+1" for p in range(counted + 1) if customers[p] == 'Y'}
            return dict(
                state={"arr": list(customers), "j": j, "close": close, "penalty": penalty,
                       "best": best, "best_hour": best_hour, "tags": tags},
                roles=roles or {},
                vars=[
                    {"label": "j", "value": "—" if j is None else j, "role": "front"},
                    {"label": "penalty", "value": penalty, "flash": flash == "penalty"},
                    {"label": "best", "value": "—" if best is None else best, "flash": flash == "best"},
                    {"label": "best_hour", "value": "—" if best_hour is None else best_hour, "flash": flash == "best"},
                ],
            )

        T.step("init", "init", "First pass: find the penalty for closing at hour 0. The shop is never open, "
               "so every hour with customers ('Y') costs 1.", **snap(None, None))
        # @trace-end
        for i in range(len(customers)):  # first pass: count the 'Y'  # @a:count
            T.op()  # @trace
            if customers[i] == 'Y':  # @a:count
                penalty += 1  # @a:count
            # @trace-begin
            T.step("count", "count", f"customers[{i}] = '{customers[i]}': " +
                   (f"customers come, penalty = {penalty}." if customers[i] == 'Y' else f"no customers, penalty stays {penalty}."),
                   **snap(None, None, {i: "current"}, "penalty", counted=i))
            # @trace-end
        best = penalty  # lowest penalty so far  # @a:start
        best_hour = 0  # the earliest hour with that penalty  # @a:start
        # @trace-begin
        T.step("start", "start", f"Closing at hour 0 costs penalty = {penalty}. That is the best so far: best = {best}, best_hour = 0.",
               **snap(None, 0, None, "best"))
        # @trace-end
        for j in range(len(customers)):  # hour j becomes an open hour: now the shop closes at j + 1  # @a:move
            T.op()  # @trace
            if customers[j] == 'Y':  # @a:move
                penalty -= 1  # these customers are served now  # @a:move
            else:  # @a:move
                penalty += 1  # open, but nobody comes  # @a:move
            # @trace-begin
            change = (f"customers[{j}] = 'Y': the shop is open for them now, penalty − 1 = {penalty}." if customers[j] == 'Y'
                      else f"customers[{j}] = 'N': open with nobody, penalty + 1 = {penalty}.")
            if penalty < best:
                T.step("move", "move", f"Close at hour {j + 1} instead of {j}. {change} That is lower than best = {best}, so we update.",
                       **snap(j, j + 1, {j: "current"}, "penalty"))
            else:
                T.step("move", "move", f"Close at hour {j + 1} instead of {j}. {change} Not lower than best = {best}"
                       + (" (equal is not enough: we want the earliest hour)." if penalty == best else "."),
                       **snap(j, j + 1, {j: "current"}, "penalty"))
            # @trace-end
            if penalty < best:  # strictly lower, so ties keep the earlier hour  # @a:update
                best = penalty  # @a:update
                best_hour = j + 1  # @a:update
                # @trace-begin
                T.step("update", "update", f"best = {best}, best_hour = {best_hour}.", **snap(j, j + 1, {j: "current"}, "best"))
                # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return best_hour = {best_hour}: closing then costs {best}. "
               "We tried every hour from 0 to n and kept the first one with the lowest penalty.", **snap(None, best_hour))
        # @trace-end
        return best_hour  # @a:return
