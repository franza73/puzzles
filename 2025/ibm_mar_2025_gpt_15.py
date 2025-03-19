import itertools
from collections import Counter
import numpy as np
from fractions import Fraction
from collections import defaultdict


def to_fraction(x: float) -> Fraction:
    return Fraction(x).limit_denominator()

def effective_resistance(i, j, L_pinv):
    return L_pinv[i, i] + L_pinv[j, j] - 2 * L_pinv[i, j]

def create_a(pos, n):
    a = np.zeros([n, n])
    H = defaultdict(set)
    for x, y in pos:
        H[x].add(y)
        H[y].add(x)
        a[x, y] += 1
        a[y, x] += 1
    return a, all(len(H[a]) > 1 for a in range(8))

def score(A):
    n = 8
    D = np.diag(np.sum(A, axis=1))
    L = D - A
    L_pinv = np.linalg.pinv(L)
    values = set()
    for i in range(n):
        for j in range(n):
            if i >= j:
                continue
            r = effective_resistance(i, j, L_pinv)
            values.add(to_fraction(r))
    return len(values) if '0' not in values else -1

def count_valid_multigraphs(num_vertices, max_edges):
    # Generate all possible edges (unordered pairs of vertices)
    edge_options = list(itertools.combinations(range(num_vertices), 2))
    num_pairs = len(edge_options)  # Number of unique edges available
    
    valid_graphs = 0

    # Generate all possible ways to distribute max_edges among edge pairs
    for edge_distribution in itertools.combinations_with_replacement(range(num_pairs), max_edges):
        edge_counts = Counter(edge_distribution)  # Count occurrences of each edge

        # Compute vertex degrees
        degree_count = {v: 0 for v in range(num_vertices)}
        for edge_idx, count in edge_counts.items():
            u, v = edge_options[edge_idx]
            degree_count[u] += count
            degree_count[v] += count

        # Ensure all vertices have at least degree 2
        if all(degree >= 2 for degree in degree_count.values()):
            _edges = [edge_options[i] for i in edge_distribution]
            a, is_valid = create_a(_edges, num_vertices)
            if not is_valid:
                continue
            _score = score(a)
            if _score >= 28:
                print(num_vertices, _edges, _score)
                break
            valid_graphs += 1

    return valid_graphs

# Compute for 5 and 6 vertices
# 5->9, 6->11, 7->13, 8->15, 
valid_multigraphs_5 = count_valid_multigraphs(9, 17)
#valid_multigraphs_6 = count_valid_multigraphs(6, 9)

print(f"Valid graphs with 5 vertices: {valid_multigraphs_5}")
#print(f"Valid graphs with 6 vertices: {valid_multigraphs_6}")

