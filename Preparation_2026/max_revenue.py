def getMaxRevenue(supplierStock, orders):
    MOD = 10**9 + 7  # safe even if not required
    supplierStock.sort(reverse=True)

    revenue = 0
    n = len(supplierStock)

    for i in range(n):
        curr = supplierStock[i]
        next_val = supplierStock[i + 1] if i + 1 < n else 0

        count = i + 1
        height = curr - next_val
        total_units = count * height

        if orders >= total_units:
            # sum from curr down to next_val + 1
            revenue += count * (curr * (curr + 1) // 2 - next_val * (next_val + 1) // 2)
            orders -= total_units
        else:
            # partial fill
            full = orders // count
            rem = orders % count

            low = curr - full
            revenue += count * (curr * (curr + 1) // 2 - low * (low + 1) // 2)
            revenue += rem * low

            return revenue % MOD

    return revenue % MOD
