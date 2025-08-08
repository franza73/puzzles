import numpy as np
from numba import njit

@njit(cache=True)
def fd(length: int, cycle: int) -> float:
    values = np.zeros(length, dtype=np.float64)
    prefix = np.zeros(length + 1, dtype=np.float64)

    for j in range(cycle, length):
        count = j - cycle + 1
        sum_values = prefix[count] - prefix[0]
        avg_values = sum_values / count
        values[j] = 1 + 2 * avg_values
        prefix[j + 1] = prefix[j] + values[j]

    return (values[length - 1] * cycle) / length

FD_1 = 36 / 51
FD_2 = 38 / 51
a_n, a_d = 645331523, 106654632
b_n, b_d =  84815000,  14017300

# TODO: 1. try this && remember to divide by the GCD
#       2. how does the result with / without gcd compare?
# 605072186 / 100000000 
# 605072200 / 100000000
#a_n, a_d = 605072186 // 2,  100000000 //2
#b_n, b_d = 605072200 // 2, 100000000 // 2

a_n, a_d = 8472804771, 83918106
b_n, b_d = 1595043820, 15797963
'''
Final result(a): 0.7450980299 for (l, c) = (8472804771, 83918106)
Final result(b): 0.7450980407 for (l, c) = (1595043820, 15797963)
Delta: 0.0000000625

Final result(a): 0.7058823520 for (l, c) = (8975639569, 1483399796)
Final result(b): 0.7058823532 for (l, c) = (3020151523, 499139032)

6.05072200 1st
'''

while True:
    m_n, m_d = a_n + b_n, a_d + b_d
    if fd(m_n, m_d) < FD_2:
        a_n, a_d = m_n, m_d
    else:
        b_n, b_d = m_n, m_d
    print(f"Final result(a): {fd(a_n, a_d):.10f} for (l, c) = ({a_n}, {a_d})")
    print(f"Final result(b): {fd(b_n, b_d):.10f} for (l, c) = ({b_n}, {b_d})")
    delta = abs(a_n / a_d - b_n / b_d)
    print(f"Delta: {delta:.10f}")
    if delta < 1e-9:
        break