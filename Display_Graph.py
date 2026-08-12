import random
import networkx as nx
import matplotlib.pyplot as plt


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


def display(edges):
    G = nx.Graph()
    G.add_edges_from(edges)

    plt.figure(figsize=(8, 6))
    pos = nx.circular_layout(G)
    plt.title("A simple Graph")
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="green",
        edge_color='black',
        node_size=500,
        
    )
    plt.show()
    plt.close()

def main():
    n, m = 10, 20
    edges = generate_random_edges(n, m)

    display(edges)

if __name__ == "__main__":
    main()