import socket
import secrets
import example_graphs
import graph_driver

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use socket.gethostname() instead of "localhost" to be visible to other machines
s.connect(("localhost", 8080))

graph = example_graphs.graphs[0]

def verify_graph(graph):
    # TODO: receive commit from server
    c = [] # dummy value

    u, v = secrets.choice(graph.edges)
    # TODO: send u, v to server

    # TODO: receive pi(phi(u)), r_u, pi(phi(v)), r_v from server
    col_u, col_v, r_u, r_v = -1, -1, -1, -1 # dummy values

    if col_u == col_v:
        return False

    c_u = graph_driver.hash_col_and_ri(col_u, r_u)
    c_v = graph_driver.hash_col_and_ri(col_v, r_v)

    if c[u] != c_u or c[v] != c_v:
        return False
    
    return True

# do verify as many times as you want
ntrials = 10
verified = True
for i in range(ntrials):
    if not verify_graph(graph):
        verified = False
        break

if verified:
    print("yay!")
else:
    print("boo!")

