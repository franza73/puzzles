from collections import defaultdict

# https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python
l22 = [1399, 1489, 1579, 1597, 1669, 1759, 1777, 1867, 1993, 2389, 2659, 2677, 2749, 2767, 2857, 3469, 3559, 3739, 3793, 3847, 3919, 4099, 4297, 4549, 4567, 4639, 4657, 4729, 4783, 4909, 5179, 5197, 5449, 5557, 5647, 5683, 5737, 5791, 5827, 5881, 5953, 6079, 6277, 6367, 6529, 6547, 6619, 6637, 6673, 6691, 6709, 6763, 6781, 6871, 6907, 6961, 7069, 7159, 7177, 7393, 7537, 7573, 7591, 7681, 7717, 7753, 7933, 7951, 8059, 8167, 8293, 8329, 8419, 8527, 8563, 8581, 8707, 8761, 8923, 8941, 9049, 9067, 9157, 9283, 9319, 9337, 9391, 9463, 9643, 9661, 9733, 9931]
# - construct a trie -
root = dict()
for li in l22:
    curr = root
    for lii in list(map(int, list(str(li)))):
        curr = curr.setdefault(lii, {})
    curr['_end_'] = '_end_'
print(root)
# - find in trie -
curr = root
for d in [2]:
    if d not in curr:
        print('NONE')
        break
    curr = curr[d]
print(curr.keys())

# global: N, root
def dig(part, pos):
    x, y = pos
    if x == N - 1 and y == N - 1:
        # filled a square
        cost(part)
        return
    if find_in_trie()