import matplotlib.pyplot as plt
import random
import networkx as nx

def subsets(index,subset,vertices):
    if index >= len(vertices):
        powerset.append(subset.copy())
        return 

    subset.append(vertices[index])
    subsets(index+1,subset,vertices)
    subset.pop()
    subsets(index+1,subset,vertices)

powerset = []


def isvc(g,subset):
    for u,v in g.edges():
        if u not in subset or v not in subset:
            return False
    return True

def min_vc(g,vertices,powerset):
    min = len(vertices)
    vc = vertices
    for subset in powerset:
        if isvc(g,subset) and min < len(subset):
            min = len(subset)
            vc = subset
    return vc




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

def write_edges(n, m, edges,i):
    with open(f'input{i}.txt', "w") as f:
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

def display(n, edges, i):
    G = nx.Graph()
    vertices = [i+1 for i in range(n)]
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)

    subsets(0,[],vertices)
    min_vc(G,vertices,powerset)

    plt.figure(figsize=(8, 6))
    pos = nx.circular_layout(G)
    plt.title(f"Graph {i}")
    nx.draw(
        G,pos,
        with_labels=True,node_color="blue", node_size=500,
    )
    plt.savefig(f'graph{i}.txt', dpi=300)
    
    plt.show()
    plt.close()

n = 10
i = 1

for m in range(10,46,5):
    edges = generate_random_edges(n, m)
    write_edges(n, m, edges,i)
    edges = read_edges()
    vertices = [i+1 for i in range(n)]
    display(n, edges, i)
    # subsets(0,[],vertices)
    i += 1

# for i in range(8):
#     open("input"+i+".txt")