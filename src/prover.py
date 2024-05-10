import socket
import threading
import networkx as nx
import example_graphs
import graph_driver
import pickle
import argparse

HOST = "localhost"
PORT = 8080

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))
serversocket.listen(5)

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
        return False
    
    recv_pair = pickle.loads(marshalled_pair)
    u, v = recv_pair[0], recv_pair[1]
    print(f"Received challenge {u}, {v}.")

    # response to challenge
    u_col, v_col = perm[coloring[u]], perm[coloring[v]]
    r_u, r_v = r[u], r[v]
    
    # send response to client
    response = pickle.dumps([u_col, v_col, r_u, r_v])
    clientsocket.send(response)
    print(f"Sent response to client.")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Prover',
                    description='Proves to the challenger that they know a valid coloring')
    parser.add_argument('graph', choices=example_graphs.available_graphs)
    parser.add_argument('honest', choices=["True", "False"])
    parser.add_argument('-s', '--show', required=False, choices=["True", "False"])
    args = parser.parse_args()

    graph = example_graphs.graphs[args.graph]
    coloring = example_graphs.colorings[args.graph][args.honest]
    print(args.honest)
    print(coloring)
    if args.show == "True":
        graph_driver.show_graph(graph, coloring)

    (clientsocket, address) = serversocket.accept()
    print(f"Connected with {address} :)")
    while True:
        success = handle_connection(clientsocket, address)
        if not success:
            break
    print("Client closed... bye bye!")
    clientsocket.close()
    serversocket.close()
