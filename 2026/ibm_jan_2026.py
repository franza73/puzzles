'''
total elapsed 3.64 min for N = 10**6
Result: 160808197419276
Also with no caching for can_sum_to: 1.57 min

total elapsed 105.90 min for N = 10**7
Result: 26190672886645170
Also with no caching for can_sum_to: 51.61 min
'''
from functools import cache
import time

# --- can_sum_to  ---
def can_sum_to(n, target):
    if n == target:
        return True
    if n < target:
        return False
    s = str(n)
    L = len(s)
    for k in range(1, L):
        a = int(s[:k])
        if a > target:
            break
        b = int(s[k:])
        if can_sum_to(b, target - a):
            return True
    return False

# --- A(n) using cache ---
@cache
def partition_sums(s):
    if not s:
        return {0}
    res = set()
    for k in range(1, len(s) + 1):
        head = int(s[:k])
        for t in partition_sums(s[k:]):
            res.add(head + t)
    return res

def A(n):
    return partition_sums(str(n))

# --- digit sum ---
def digit_sum_mod9(n):
    return sum(map(int, str(n))) % 9

# --- main program ---
def main():
    N = 10**6
    batch_size = 100000
    valid_x = set()

    start_time = time.time()
    total_batches = (N + batch_size - 1) // batch_size

    for batch_idx, batch_start in enumerate(range(1, N + 1, batch_size), 1):
        batch_end = min(batch_start + batch_size, N + 1)
        batch_start_time = time.time()
        
        for ni in range(batch_start, batch_end):
            d_sum = digit_sum_mod9(ni)
            if d_sum not in (0, 1):
                continue
            for ai in A(ni):
                x = ni * ai
                if x in valid_x:
                    continue
                if can_sum_to(x, ni):
                    valid_x.add(x)
    
        # --- progress report ---
        elapsed = time.time() - batch_start_time
        total_elapsed = time.time() - start_time
        avg_per_batch = total_elapsed / batch_idx
        batches_left = total_batches - batch_idx
        est_remaining = avg_per_batch * batches_left
        
        print(f"Batch {batch_idx}/{total_batches} ({batch_start}-{batch_end-1}) "
            f"took {elapsed:.2f}s, "
            f"total elapsed {total_elapsed/60:.2f} min, "
            f"estimated remaining {est_remaining/60:.2f} min")

    print(f"Result: {sum(valid_x)}")

if __name__ == "__main__":
    main()