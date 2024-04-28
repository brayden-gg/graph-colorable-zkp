import networkx as nx
import hashlib
import secrets

import constants

def get_permutation(n): # probably overkill but maybe more secure?
    lst = list(range(n))
    perm = []
    while lst != []:
        rand_elt = lst.pop(secrets.choice(lst))
        perm.append(rand_elt)
    return perm

def get_ri():
    return secrets.randbits(constants.LAMBDA).to_bytes(constants.LAMBDA // 8, 'big')

def hash_col_and_ri(col, ri):
    permuted_color = col.to_bytes(1, 'big')
    return hashlib.sha256().hexdigest(ri + permuted_color), random_bits

    
    
