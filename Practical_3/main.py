import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import os
import csv

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


def approximation_algo(edges):
    match = set()
    vc = set()

    for u, v in edges:
        if u not in vc and v not in vc:
            match.add((u, v))
            vc.add(u)
            vc.add(v)

    return vc, match

def approximation_factor(vc, opt_size):
    return round(len(vc) / opt_size,5)

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

def brute_force_display(n, m, edges, i):
    os.makedirs('Visualize_brute',exist_ok=True)

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

    with open('result.csv', 'a', newline='') as f:
        w = csv.writer(f)
        w.writerow([(n,m),len(vc),execution_time])


    # color = []
    # for v in vertices:
    #     if v in vc:
    #         color.append('red')
    #     else:
    #         color.append('blue')
    
    # plt.figure(figsize=(8, 6))
    # coordinates = nx.circular_layout(G)
    # plt.title(f"Graph {i} = {n,m}")
    # nx.draw(
    #     G,coordinates,
    #     with_labels=True,node_color=color, node_size=600,
    # )
    # plt.savefig(f'Visualize_brute/graph{i}.png', dpi=300)

    # return len(vc)

def approximation_display(n,m,edges,opt_size,i):
    os.makedirs('Visualize_approx',exist_ok=True)

    st_time = time.perf_counter()
    vc, match = approximation_algo(edges)
    end_time = time.perf_counter()
    execution_time = (end_time-st_time)/1000

    factor = approximation_factor(vc, opt_size)

    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))
    G.add_edges_from(edges)

    edge_color = []
    for edge in edges:
        if edge in match:
            edge_color.append('red')
        else:
            edge_color.append('black')

    node_color = []
    for v in G.nodes():
        if v in vc:
            node_color.append('red')
        else:
            node_color.append('lightblue')

    plt.figure(figsize=(10, 8))
    # pos = nx.circular_layout(G)
    plt.title(f'G{i} = ({n,m})')
    nx.draw(G, with_labels=True, node_color=node_color, edge_color=edge_color,node_size=700)

    output_file = os.path.join('Visualize_approx', f"graph_{i}.png")
    plt.savefig(output_file,dpi=300)

def main():
    os.makedirs('Input',exist_ok=True)

    with open('result.csv', 'w', newline ='') as f:
        w = csv.writer(f)
        w.writerow(['(Vertex,Edge)','Size','Execution Time', 'vc_size(approx.)', 'Execution_Time', 'Match_size', 'Approximation_Factor'])

    n = 20
    i = 1
    for m in range(20,190,10):
        # edges = generate_edges(n, m)
        # write_edges(n, m, edges,i)
        edges = read_edges(i)
        opt_size = brute_force_display(n, m, edges, i)
        # approximation_display(n,m,edges,opt_size, i)
        i += 1

if __name__ == '__main__':
    main()