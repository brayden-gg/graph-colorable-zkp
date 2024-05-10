import socket
import secrets
import example_graphs
import graph_driver
import pickle

HOST = "localhost"
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use socket.gethostname() instead of "localhost" to be visible to other machines
s.connect((HOST, PORT))
print("Connected to server!")

graph = example_graphs.graphs[1] # choose graph... can automate this later

def verify_graph(graph):
    # receive color from server
    marshalled_colors = s.recv(1024) # assuming ints are 4 bytes, ~250 cols
    coloring = pickle.loads(marshalled_colors)


    u, v = secrets.choice(list(graph.edges))
    print(u, v) # TODO: REMOVE THIS DEBUG

    # send u, v to server
    marshalled_challenge = pickle.dumps([u, v])
    s.send(marshalled_challenge)
    print(f"Sent challenge {u}, {v} to server.")

    # receive pi(phi(u)), r_u, pi(phi(v)), r_v from server
    marshalled_response = s.recv(1024)
    print("Received response from server.")
    response = pickle.loads(marshalled_response)
    col_u, col_v, r_u, r_v = response[0], response[1], response[2], response[3]

    if col_u == col_v:
        return False

    c_u = graph_driver.hash_col_and_ri(col_u, r_u)
    c_v = graph_driver.hash_col_and_ri(col_v, r_v)

    if coloring[u] != c_u or coloring[v] != c_v:
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
    print(f"Verified coloring after {ntrials} trials :)")
else:
    print(f"Failed to verify given coloring >:(")

