import socket
import secrets
import example_graphs
import graph_driver
import pickle
import argparse

HOST = "localhost"
PORT = 8080
verbose = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use socket.gethostname() instead of "localhost" to be visible to other machines
s.connect((HOST, PORT))
print("Connected to server!")



def verify_graph(graph, u=None, v=None):
    # receive color from server
    marshalled_colors = s.recv(1024) # assuming ints are 4 bytes, ~250 cols
    coloring = pickle.loads(marshalled_colors)

    if u is None or v is None:
        u, v = secrets.choice(list(graph.edges))

    # send u, v to server
    marshalled_challenge = pickle.dumps([u, v])
    s.send(marshalled_challenge)
    if verbose:
        print(f"Sent challenge {u}, {v} to server.")

    # receive pi(phi(u)), r_u, pi(phi(v)), r_v from server
    marshalled_response = s.recv(1024)
    if verbose:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Challenger',
                    description='Tell the prover which graph you would like them to prove for you')
    parser.add_argument('graph', choices=example_graphs.available_graphs)
    parser.add_argument('-n', '--ntrials', required=False, type=int)
    parser.add_argument('-u','--u', required=False, type=int)
    parser.add_argument('-v', '--v', required=False, type=int)
    parser.add_argument('-y', '--verbose', required=False, choices=["true", "false"])

    args = parser.parse_args()

    graph = example_graphs.graphs[args.graph]

    if args.verbose == "true":
        verbose = True

    if args.ntrials is not None:
        verified = True
        for i in range(args.ntrials):
            if not verify_graph(graph):
                verified = False
                break
        if verified:
            print(f"Verified coloring after {args.ntrials} trials :)")
        else:
            print(f"Failed to verify given coloring >:(")

    elif args.u is not None and args.v is not None:
        if not (0 <= args.u < len(graph.vertices) and 0 <= args.v < len(graph.vertices)):
            s.close()
            raise Exception(f"please select u and v that are valid vertices 0 <= u, v < {len(graph.vertices)}")
        if verify_graph(graph, args.u, args.v):
            print(f"Verified coloring for (u, v) = ({args.u}, {args.v})")
        else:
            print(f"Failed to verify coloring for (u, v) = ({args.u}, {args.v})")
    else:
        s.close()
        raise Exception("please specify --ntrials or an edge via -u and -v")

    s.close()
    print("Closed connection: bye bye!")

    