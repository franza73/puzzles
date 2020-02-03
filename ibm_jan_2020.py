from copy import deepcopy


def combine(a, b):
    # How to combine the barrel contents.
    # 0 beats 1,2,3
    # 1 beats 2,3
    # etc. So we can use min function for each plant.
    # Using 3 for 'not' using a barrel for this plant.
    c = []
    for i in range(4):
        c += [min(a[i], b[i])]
    return str(c)


def all_feasible():
    # List all the options for positioning content from one barrel.
    # If 0, 1, 2 then the corresponding barrel should kill the plant 
    # on the location indicated. If 3, then the plant will not die.
    # That allows for a simple 'combine' function.
    R = range(4)
    v = [[i, j, k, l] for i in R for j in R for k in R for l in R]

    # Insight: inspired on the solution provided for the smaller case,
    # we can look at the smaller set where the barrel is used on 2 or all
    # of the plants.
    v = list(filter(lambda x: x.count(3) in [2, 4], v))
    return v


def all_hashes(v):
    # Calculate all hashes of combinations of pairs of choices for barrel
    # locations, given a list of barrel position choices.
    KEY = str(v)
    if KEY in H:
        return H[KEY]
    if len(v) == 2:
        new = combine(v[0], v[1])
        H[KEY] = {new}
        return H[KEY]
    new = set(combine(v[-1], v2) for v2 in v[:-1])
    result = H[str(v[:-1])].union(new)
    H[KEY] = result
    return result


# Keep adding items to complete lists of hashes, until we find a solution.
def explore(indexes, N):
    if len(indexes) > 11:
        print(len(indexes))
        print([v[i] for i in indexes])
    if len(indexes) > 0:
        last = indexes[-1]
    else:
        last = -1
    for i in range(last+1, N):
        new_indexes = deepcopy(indexes)
        new_indexes += [i]
        size = len(new_indexes)
        if size > 1 and len(all_hashes([v[i] for i in new_indexes])) < size*(size-1)/2:
            continue
        explore(new_indexes, N)


if __name__ == '__main__':
    from random import shuffle
    v = all_feasible()
    shuffle(v)
    #v = [[3, 0, 3, 2], [3, 2, 3, 0], [3, 2, 0, 3], [3, 1, 1, 3], [0, 3, 3, 2], [2, 3, 1, 3], [3, 0, 2, 3], [3, 3, 3, 3], [1, 3, 3, 1], [1, 3, 2, 3], [3, 1, 3, 1], [2, 3, 3, 0]]
    len_v = len(v)
    print('len =', len_v)
    H = {}
    indexes = []
    explore(indexes, len_v)
    #for key, value in H.items():
    #    if len(value) == 66:
    #        print(key, '--->', value)
