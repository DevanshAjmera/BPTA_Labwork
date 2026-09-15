import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import time
import csv

def approximation_algo(edges):
    match = []
    vc = []

    for u,v in edges:
        if u not in vc and v not in vc:
            vc.append(u)
            vc.append(v)
            match.append((u,v))
    return vc, match

def approximation_factor(vc, opt_size):
    return round(len(vc) / opt_size,3)

def read_input(i):
    edges = []
    # with open(f'../Practical_1/Input/input{i}.txt', 'r') as f:
    with open(f'Input/input{i}.txt', 'r') as f:
        lines = f.readlines()
        n, m = map(int, lines[0].split())

        for line in lines[1:]:
            if not line:
                continue
            u, v = map(int, line.split())
            edges.append((u,v))
    return n, m, edges

def csv_update(rows, n, m, size, time, factor):
    for row in rows[1:]:
        if row[0] == str((n,m)):
            row[3] = size
            row[4] = time
            row[5] = factor
            break

def create_graph(match, vc, n, m, i, edges):

    os.makedirs("output", exist_ok=True)

    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))
    G.add_edges_from(edges)

    node_color = []
    for node in G.nodes:
        if node in vc:
            node_color.append('red') 
        else:
            node_color.append('lightblue')

    edge_color = []
    for edge in edges:
        if edge in match:
            edge_color.append('green')
        else:
            edge_color.append('black')
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, with_labels=True, node_color=node_color, edge_color=edge_color, node_size=700)

    plt.title(
        f"Graph {i} | n={n}, m={m}\n"
        f"Vertex Cover = {vc} | Matching Size = {len(match)}"
    )

    output_file = os.path.join('output', f"graph_{i}.png")
    plt.savefig(output_file,dpi=300)
    plt.close()
    print(f"Graph {i} saved to {output_file}")


def main():
    # with open('../Practical_1/result.csv','r',newline='') as f:
    with open('result.csv', 'r', newline='') as f:
        rows = list(csv.reader(f))
    
    if 'Vertex Cover' in rows[0]:
        for row in rows:
            del row[1]

    
    if 'Approximation_size' not in rows[0]:
        rows[0].extend(['vc_size(approx.)', 'Execution_Time', 'Approximation_Factor'])
    
        for row in rows[1:]:
                row.extend(['', '', ''])

    for i in range(1,9):
        n, m, edges = read_input(i)
        optimal_size = None

        for row in rows[1:]:
            if row[0] == str((n, m)):
                optimal_size = int(row[1])
                break
        
        st_time = time.perf_counter()
        vc, match = approximation_algo(edges)
        end_time = time.perf_counter()

        execution_time = round((end_time-st_time)*1000,4)

        factor = approximation_factor(vc, optimal_size)

        csv_update(rows, n,m,len(vc), execution_time, factor)

        create_graph( match, vc, n, m, i, edges)


    # with open('../Practical_1/result.csv', 'w', newline='') as f:
    with open('result.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(rows)


if __name__ == '__main__':
    main()