import networkx as nx
from matplotlib import pyplot as plt

cols = ["blue", "red", "green"]

k3 = nx.complete_graph(3)
k3_col = [0, 1, 2]
k3_col_cheat = [0, 1, 1]

petersen = nx.Graph()
petersen.add_edges_from([(0, 5), (1, 6), (2, 7), (3, 8), (4, 9), 
                         (5, 6), (6, 7), (7, 8), (8, 9), (9, 5),
                         (0, 2), (2, 4), (4, 1), (1, 3), (3, 0)])
petersen_col = [0, 1, 1, 2, 2, 1, 0, 2, 1, 0]
petersen_col_cheat = [0, 1, 1, 2, 0, 1, 1, 2, 2, 2]

graphs = {"k3": k3, "petersen": petersen}
colorings = {"k3": {"True": k3_col, "False": k3_col_cheat}, "petersen": {"True": petersen_col, "False": petersen_col_cheat}}
available_graphs = list(graphs.keys())
    
# assert valid_coloring(k3, k3_col)
# assert valid_coloring(petersen, petersen_col)

