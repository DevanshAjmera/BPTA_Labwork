import networkx as nx
import matplotlib.pyplot as plt


def input_data():
    n = int(input("Enter total vertices: "))
    m = int(input("Enter total edges: "))
    
    if m> n*(n-1)//2:
        raise ValueError("edges are more")
    elif m < n-1:
        raise ValueError("edges cant be less than vertices-1.")
    
    edge_set = set()
    i = 1
    while len(edge_set) < m:
        u = int(input(f'Enter 1st vertex of edge {i}: '))
        v = int(input(f'Enter 2nd vertex of edge {i}: '))
        if u == v:
            continue
        edge = tuple(sorted((u, v)))
        edge_set.add(edge)
        i += 1
    return n,m,list(edge_set)


def display():
    n,m,edges = input_data()
    G = nx.Graph()
    G.add_edges_from(edges)

    plt.figure(figsize=(8,6))
    pos = nx.circular_layout(G)
    plt.title(f"Graph = ({n},{m})")

    nx.draw(G,pos,
        with_labels=True,
        node_color="green", edge_color='black', node_size=600,   
    )
    plt.show()
    plt.close()

display()