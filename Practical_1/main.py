import random
import networkx as nx
import matplotlib.pyplot as plt

def read_n_m():
    with open('input.txt', "r") as f:
        first_line = f.readline().strip()
    n, m = map(int, first_line.split())
    return n, m

def generate_random_edges(n, m):
    if m> n*(n-1)//2:
        raise ValueError("edges cant be more than vertices.")
    
    edges = set()
    while len(edges) < m:
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u == v:
            continue
        edge = tuple(sorted((u, v)))
        edges.add(edge)
    return list(edges)

def write_edges(n, m, edges):
    with open('input.txt', "w") as f:
        f.write(f"{n} {m}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")

def read_edges():
    edges = []
    with open('input.txt', "r") as f:
        lines = f.readlines()

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        u, v = map(int, line.split())
        edges.append((u, v))
    return edges

def display(edges, output_file='graph.png'):
    G = nx.Graph()
    G.add_edges_from(edges)

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="blue",
        edge_color='black',
        node_size=500,
    )
    plt.savefig(output_file, dpi=300)
    plt.close()

def main():
    n, m = read_n_m()
    edges = generate_random_edges(n, m)

    write_edges(n, m, edges)
    edges = read_edges()
    display(edges)

if __name__ == "__main__":
    main()