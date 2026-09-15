import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import time
import csv

def maximal_matching(edges):
    match = []
    vc = []

    for u,v in edges:
        if u not in vc and v not in vc:
            vc.append(u)
            vc.append(v)
            match.append((u,v))

    return vc, match



def read_input(i):
    edges = []
    with open(f'../Practical_1/Input/input{i}.txt', 'r') as f:
        lines = f.readlines()
        n, m = map(int, lines[0].split())

        for line in lines[1:]:
            if not line:
                continue
            u, v = map(int, line.split())
            edges.append((u,v))
    return n, m, edges

def csv_update(rows, n, m, vc, size, time):
    for row in rows[1:]:
        if row[0] == str((n,m)):
            row[4] = vc
            row[5] = size
            row[6] = time
            break

def create_graph(match, vc, n, m, i, edges):

    os.makedirs("output", exist_ok=True)

    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))
    G.add_edges_from(edges)

    vc_set = set(vc)

    node_colors = ["red" if node in vc_set else "lightblue" for node in G.nodes() ]

    match_set = {tuple(sorted(edge)) for edge in match}

    edge_colors = [
        "green" if tuple(sorted(edge)) in match_set else "black"
        for edge in G.edges()
    ]

    # pos = nx.circular_layout(G)

    plt.figure(figsize=(10, 8))

    nx.draw( G, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=700, font_size=10, font_weight="bold", width=2)

    plt.title(
        f"Graph {i} | n={n}, m={m}\n"
        f"Vertex Cover = {vc} | Matching Size = {len(match)}"
    )

    legend_elements = [
        Line2D(
            [0], [0],
            marker="o",
            color="w",
            label="Vertex Cover",
            markerfacecolor="red",
            markersize=10
        ),
        Line2D(
            [0], [0],
            color="green",
            lw=3,
            label="Matching Edge"
        )
    ]

    plt.legend(handles=legend_elements)

    output_file = os.path.join('output', f"graph_{i}.png")
    plt.savefig(output_file,dpi=300)
    plt.close()
    print(f"Graph {i} saved to {output_file}")


def main():
    with open('../Practical_1/result.csv','r',newline='') as f:
            rows = list(csv.reader(f))
    
    if 'Approximation_vc' not in rows[0]:
        rows[0].extend(['Approximation_vc', 'Size', 'Execution_Time'])
    
        for row in rows[1:]:
                row.extend(['', '', ''])

    for i in range(1,9):
        n, m, edges = read_input(i)
        
        st_time = time.perf_counter()
        vc, match = maximal_matching(edges)
        end_time = time.perf_counter()

        execution_time = (end_time-st_time)*1000

        csv_update(rows, n,m,vc, len(vc), execution_time)

        create_graph( match, vc, n, m, i, edges)

    with open('../Practical_1/result.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(rows)


if __name__ == '__main__':
    main()