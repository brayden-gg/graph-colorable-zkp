import networkx as nx
import hashlib
import secrets
from matplotlib import pyplot as plt

import constants

def get_permutation(n): # probably overkill but maybe more secure?
    lst = list(range(n))
    sz = n
    perm = []
    while sz > 0:
        rand_elt = lst.pop(secrets.choice(list(range(sz))))
        perm.append(rand_elt)
        sz -= 1
    return perm

def get_ri():
    return secrets.randbits(constants.LAMBDA).to_bytes(constants.LAMBDA // 8, 'big')

def hash_col_and_ri(col, ri):
    permuted_color = col.to_bytes(1, 'big')
    return hashlib.sha256(ri + permuted_color).hexdigest()

def show_graph(graph, coloring):
    cols = ["blue", "red", "green"]
    nx.draw(graph, node_color=[cols[i] for i in coloring])
    plt.show()

def valid_coloring(graph, coloring):
    for (u, v) in graph.edges:
        if coloring[u] == coloring[v]:
            return False
    return True

    
    
