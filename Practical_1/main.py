import matplotlib.pyplot as plt
import random
import networkx as nx
import time
import os

os.makedirs('Input',exist_ok=True)
os.makedirs('Visualize',exist_ok=True)

def subsets(index,subset,vertices,powerset):
    if index >= len(vertices):
        powerset.append(subset.copy())
        return 

    subset.append(vertices[index])
    subsets(index+1,subset,vertices,powerset)
    subset.pop()
    subsets(index+1,subset,vertices,powerset)

def isvc(g,subset):
    for u,v in g.edges():
        if u not in subset and v not in subset:
            return False
    return True

def min_vc(g,vertices,powerset):
    min = len(vertices)
    vc = vertices
    for subset in powerset:
        if isvc(g,subset) and min > len(subset):
            min = len(subset)
            vc = subset
    return vc


def generate_edges(n, m):
    if m < n-1:
        raise ValueError('edges cant be less than n-1')
    if m> n*(n-1)//2:
        raise ValueError("edges cant be more than n*(n-1)/2.")
    
    edges = set()
    while len(edges) < m:
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u == v:
            continue
        edge = tuple(sorted((u, v)))
        edges.add(edge)
    return list(edges)

def connected_edges(n,m):
    while True:
        edges = generate_edges(n, m)
        g= nx.Graph()
        
        g.add_nodes_from(range(1,n+1))
        g.add_edges_from(edges)

        if nx.is_connected(g):
            return edges

def write_edges(n, m, edges,i):
    with open(f'Input/input{i}.txt', "w") as f:
        f.write(f"{n} {m}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")

def read_edges(i):
    edges = []
    with open(f'Input/input{i}.txt', "r") as f:
        lines = f.readlines()

    for line in lines[1:]:
        if not line:
            continue

        u, v = map(int, line.split())
        edges.append((u, v))
    return edges

def display(n, m, edges, i):
    G = nx.Graph()
    vertices = [i+1 for i in range(n)]
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)

    st_time = time.perf_counter()

    powerset = []
    subsets(0,[],vertices,powerset)
    vc = min_vc(G,vertices,powerset)

    end_time = time.perf_counter()

    execution_time = (end_time-st_time)*1000

    with open('result.txt', 'a') as f:
        f.write(f"Graph {i}\n"
            f"Total vertices : {n}\n" f"Total edges    : {m}\n"
            f"Vertex cover   : {vc}\n" f"VC size        : {len(vc)}\n"
            f"Execution time : {execution_time:.6f} ms\n"
            f"Time complexity: O((2^{n})*{n}*{m}) or {(2**n)*n*m}\n"
            f"--------------------------------\n"
        )

    color = []
    for v in vertices:
        if v in vc:
            color.append('red')
        else:
            color.append('blue')
    
    plt.figure(figsize=(8, 6))
    coordinates = nx.circular_layout(G)
    plt.title(f"Graph {i} = {n,m}")
    nx.draw(
        G,coordinates,
        with_labels=True,node_color=color, node_size=600,
    )
    plt.savefig(f'Visualize/graph{i}.png', dpi=300)
    # plt.show()

with open('result.txt','w') as f:
    f.write("Result file\n")
    f.write("-------------\n")

n = 10
i = 1
for m in range(10,46,5):
    edges = connected_edges(n, m)
    write_edges(n, m, edges,i)
    edges = read_edges(i)
    display(n, m, edges, i)
    i += 1