import socket
import threading
import networkx as nx
import example_graphs
import graph_driver
import pickle

HOST = "localhost"
PORT = 8080

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use socket.gethostname() instead of "localhost" to be visible to other machines
serversocket.bind((HOST, PORT))
serversocket.listen(5)

graph = example_graphs.graphs[0]
coloring = example_graphs.colorings[0]
graph_driver.show_graph(graph, coloring)
def handle_connection(clientsocket, address):
    perm = graph_driver.get_permutation(3)
    r = [graph_driver.get_ri() for _ in coloring]
    c =  [graph_driver.hash_col_and_ri(perm[col], ri) for col, ri in zip(coloring, r)]
    
    # send c to client
    marshalled = pickle.dumps(c)
    clientsocket.send(marshalled)
    print("Sent coloring to client.")

    # receive challenge, (u, v) from client
    u, v = -1, -1 # dummy values
    marshalled_pair = []
    try:
        marshalled_pair = clientsocket.recv(1024) # 1024 is prolly overkill
    except:
        print("rah")
        return False
    recv_pair = pickle.loads(marshalled_pair)
    u, v = recv_pair[0], recv_pair[1]
    print(f"Received challenge {u}, {v}.")

    # response to challenge
    u_col, v_col = perm[coloring[u]], perm[coloring[v]]
    r_u, r_v = r[u], r[v]
    
    # send response to client
    response = pickle.dumps([u_col, v_col, r_u, r_v])
    # response = pickle.dumps([0, 0, 0, 0])
    clientsocket.send(response)
    print(f"Sent response to client.")

    return True

(clientsocket, address) = serversocket.accept()
print(f"Connected with {address} :)")
while True:
    # accept connections from outside
    # (clientsocket, address) = serversocket.accept()
    # print(f"Connected with {address} :)")
    lol = handle_connection(clientsocket, address)
    # thd = threading.Thread(target=handle_connection, args=(clientsocket, address))
    # thd.run()
    if not lol:
        break
print("Client closed... bye bye!")
clientsocket.close()
serversocket.close()
