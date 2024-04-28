import socket
import threading
import networkx as nx
import example_graphs
import graph_driver

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use socket.gethostname() instead of "localhost" to be visible to other machines
serversocket.bind(("localhost", 8080))
serversocket.listen(5)

graph = example_graphs.graphs[0]
coloring = example_graphs.colorings[0]

def handle_connection(clientsocket, address):
    perm = graph_driver.get_permutation(3)
    r = [graph_driver.get_ri() for _ in coloring]
    c =  [graph_driver.hash_col_and_ri(perm[col], ri) for col, ri in zip(coloring, r)]
    # TODO: send c to client

    # TODO: receive challenge, (u, v) from client
    u, v = -1, -1 # dummy values

    # response to challenge
    u_col, v_col = perm[coloring[u]], perm[coloring[v]]
    r_u, r_v = r[u], r[v]
    # TODO: send response to client

    

while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    
    thd = threading.Thread(target=handle_connection, args=(clientsocket, address))
    thd.run()

