import os
import csv
import time
import scipy.optimize as opt

def copy_inputs():
    os.makedirs("Input", exist_ok=True)
    for i in range(1, 9):
        with open(f"../Practical_2/Input/input{i}.txt", "r") as f:
            data = f.read()
        with open(f"Input/input{i}.txt", "w") as f:
            f.write(data)

    for i in range(1, 11):
        with open(f"../Practical_3/Input/input{i}.txt", "r") as f:
            data = f.read()
        with open(f"Input/input{i+8}.txt", "w") as f:
            f.write(data)

def read_input(i):
    edges = []
    with open(f"Input/input{i}.txt", "r") as f:
        lines = f.readlines()
        n, m = map(int, lines[0].split())
        for line in lines[1:]:
            if not line:
                continue
            u,v =map(int, line.split())
            edges.append((u, v))
    return n , m,edges

def lp_vertex_cover(n, edges):
    c = [1] * n
    A = []
    b = []

    for u,v in edges:
        constraint = [0] * n
        constraint[u - 1] = -1
        constraint[v - 1] = -1
        A.append(constraint)
        b.append(-1)
    bound = [(0, 1)] * n
    result = opt.linprog( c, A_ub=A, b_ub=b, bounds=bound, method="highs")
    lp_optimal = result.fun
    return result.x, lp_optimal

def lp_rounding(x):
    vc = set()
    for v in range(len(x)):
        if x[v] >= 0.5:
            vc.add(v + 1)
    return vc

def greedy_algorithm(edges):
    vc = set()
    matching = set()
    for u, v in edges:
        if u not in vc and v not in vc:
            matching.add((u, v))
            vc.add(u)
            vc.add(v)
    return vc, matching

def read_factors():
    with open("Input/approx_factor.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    # copy_inputs()
    factors = read_factors()

    with open("result.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["(Vertex,Edge)", "Lp_optimal", "Lp_Round_size", "Greedy_Size","Lp_Factor", "Greedy_Factor", "Lp_Time"])

    for i in range(1, 19):
        n, m, edges = read_input(i)

        startime = time.perf_counter()
        x, lp_optimal = lp_vertex_cover(n, edges)
        endtime = time.perf_counter()
        lp_time = endtime - startime

        lp_vc = lp_rounding(x)
        greedy_vc, match = greedy_algorithm(edges)
        greedy_factor = round(len(greedy_vc)/lp_optimal, 6)

        with open("result.csv", "a", newline="") as f:
            w = csv.writer(f)
            w.writerow([(n, m), round(lp_optimal, 6), len(lp_vc), len(greedy_vc), greedy_factor, factors[i-1], f"{lp_time:.8f}"])

main()