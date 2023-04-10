'''
    We've used a DFS program to explore the graph that starts with the
original sequence and where each neighbor node is obtained from the original
plus one move as defined in the problem formulation. We adopted the
heuristic of, for each level, only exploring a smaller number of options
that originate smaller values at the begining of the sequence that defines
 that node. We were able to tune the values of (MAX_DEPTH, SIZE), to
obtain a solution in 10 steps:

[[855661, 1395050, 1402703, 1575981, 2956165, 4346904, 5516627, 5693538, 6096226, 7359806],
 [173278, 855661, 1395050, 2805406, 2956165, 4346904, 5516627, 5693538, 6096226, 7359806],
 [173278, 579599, 855661, 1395050, 2805406, 2956165, 4346904, 5693538, 7359806, 11033254],
 [173278, 579599, 855661, 1346634, 1395050, 2805406, 2956165, 7359806, 8693808, 11033254],
 [173278, 579599, 855661, 1334002, 1346634, 1395050, 2805406, 2956165, 11033254, 14719612],
 [61048, 173278, 579599, 855661, 1346634, 2668004, 2805406, 2956165, 11033254, 14719612],
 [61048, 173278, 579599, 855661, 1346634, 2668004, 2805406, 5912330, 8077089, 14719612],
 [61048, 173278, 579599, 855661, 1346634, 2164759, 2668004, 2805406, 11824660, 14719612],
 [61048, 173278, 579599, 640647, 855661, 1346634, 2668004, 4329518, 11824660, 14719612],
 [61048, 61048, 173278, 855661, 1159198, 1346634, 2668004, 4329518, 11824660, 14719612],
 [0, 122096, 173278, 855661, 1159198, 1346634, 2668004, 4329518, 11824660, 14719612]]

 We started with a MAX_DEPTH of 20 and SIZE 3, obtaining a solution at depth 12.
 We then decreased the MAX_DEPTH and increased the SIZE to look for better solutions.

 For the (*) portion of the problem, if we increase the first seven numbers to be all equal
 to l[7] and make new l[8] to be equal to l[9], then in 8 steps we get to all zeros but the last two elements,
and these two elements will be 8*l[7] and 2*l[9]. In order to simplify the remaining steps, we also
want the total sum of the values to be the next power of two.
To obtain that, we can add x and y to the first 8 and next 2 items, respectively. The last two
elements will now be 8*(l[7] + x) and 2*(l[9] + y). We now choose x and y by maximizing the gcd of
the two remaining numbers, still under the constraint that the total sum should be the suitable power of two.
 We calculate the delta value and show that it does not exceed the specified value.

Given 
l = [855661, 1395050, 1402703, 1575981, 2956165, 4346904, 5516627, 5693538, 6096226, 7359806]
and 
delta = [5435795, 4896406, 4888753, 4715475, 3335291, 1944552, 774829, 597918, 2292382, 1028802]
we have:
sum(delta) = 29910203 < 30 * 10**6
and the sequence is now:
newL = [6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 8388608, 8388608]
for which:
sum(newL) = 2**26
And the required sequence of steps is indicated here:

 [[6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 8388608, 8388608], 
  [0, 6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 16777216], 
  [0, 0, 6291456, 6291456, 6291456, 6291456, 6291456, 6291456, 12582912, 16777216], 
  [0, 0, 0, 6291456, 6291456, 6291456, 6291456, 12582912, 12582912, 16777216], 
  [0, 0, 0, 0, 6291456, 6291456, 6291456, 6291456, 16777216, 25165824], 
  [0, 0, 0, 0, 0, 6291456, 6291456, 12582912, 16777216, 25165824], 
  [0, 0, 0, 0, 0, 0, 12582912, 12582912, 16777216, 25165824], 
  [0, 0, 0, 0, 0, 0, 0, 16777216, 25165824, 25165824], 
  [0, 0, 0, 0, 0, 0, 0, 0, 16777216, 50331648], 
  [0, 0, 0, 0, 0, 0, 0, 0, 33554432, 33554432], 
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 67108864]]

  Better solution (9 steps):
  s = 4*[2**22] + 6*[2**23]
  sum(s) = 2**26
  >>> delta = [s[i] - l[i] for i in range(len(l))]
  >>> delta
[3338643, 2799254, 2791601, 2618323, 5432443, 4041704, 2871981, 2695070, 2292382, 1028802]
  >>> sum(delta)
29910203
2**22 *
[
 1 1 1 1 2 2 2 2 2 2
 0 1 1 2 2 2 2 2 2 2
 0 0 2 2 2 2 2 2 2 2
 0 0 0 2 2 2 2 2 2 4
 0 0 0 0 2 2 2 2 4 4
 0 0 0 0 0 2 2 4 4 4 
 0 0 0 0 0 0 4 4 4 4
 0 0 0 0 0 0 0 4 4 8
 0 0 0 0 0 0 0 0 8 8
 0 0 0 0 0 0 0 0 0 16
]
'''
from math import gcd, log2, ceil


def dig(v, index, path):
    if v[0] == 0:
        print(index, path)
        return
    if index == MAX_DEPTH:
        return 
    L = len(v)
    s = []
    for i in range(L):
        for j in range(i+1, L):
            newV = list(v)
            newV[i], newV[j] = newV[j] - newV[i], 2*newV[i]
            newV.sort()
            K = ','.join(map(str, newV))
            if K not in visited:
                s.append(newV)
                visited.add(K)
    s.sort()
    for v in s[:SIZE]:
        newPath = list(path) + [v]
        dig(v, index + 1, newPath)


l = [855661, 1395050, 1402703, 1575981, 2956165, 4346904, 5516627, 5693538, 6096226, 7359806]
MAX_DEPTH = 12
SIZE = 3
visited = set()
dig(l, 0, [l])


EXP = ceil(log2(sum(l)))
V = 2**EXP - (8*l[7] + 2*l[9])
# For all the options of x and y that make the total sum equal to V,
# choose the one with higher GCD, so we can resolve the remaining problem in fewer steps.
x = 0
best_gcd = 0
while True:
    y = (V - 8*x) // 2
    if y < 0:
        break
    gcd_value = gcd(8*(l[7] + x), 2*(l[9] + y))
    if gcd_value > best_gcd:
        best = gcd_value
        best_x, best_y = x, y
    x += 1
x, y = best_x, best_y
deltas = [l[7] + x - l[i] for i in range(8)] + [l[9] + y - l[i] for i in range(8, 10)]
assert(sum(deltas)) < 30*10**6
assert(sum(l) + sum(deltas) == 2**EXP)
newL = [l[7] + x for i in range(8)] + [l[9] + y for i in range(8, 10)]
assert(sum(newL) == 2**EXP)