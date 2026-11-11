import pandas as pd
from sklearn.datasets import (load_iris,load_wine,load_breast_cancer,load_digits,load_diabetes)
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import time
import matplotlib.pyplot as plt

def eucl_distance(p1, p2):
    total = 0.0
    for i in range(len(p1)):
        diff = float(p1[i]) - float(p2[i])
        total += diff * diff
    return total**0.5

def distance_matrix(data):
    n = len(data)
    dist = [[0.0 for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            d = eucl_distance(data[i], data[j])
            dist[i][j] = d
            dist[j][i] = d
    return dist

def calculate_cost(dist, centers):
    n = len(dist)
    max_distance = 0.0
    for i in range(n):
        nearest = float('inf')
        for c in centers:
            if dist[i][c] < nearest:
                nearest = dist[i][c]

        if nearest > max_distance:
            max_distance = nearest
    return max_distance


def library_heuristic(data, dist, k):
    start = time.perf_counter()
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10,
        max_iter=300
    )
    model.fit(data)
    centers = []
    for centroid in model.cluster_centers_:
        best_index = -1
        best_distance = float('inf')
        for i in range(len(data)):
            if i in centers:
                continue
            d = eucl_distance(data[i], centroid)
            if d < best_distance:
                best_distance = d
                best_index = i
        centers.append(best_index)

    cost = calculate_cost(dist, centers)
    end = time.perf_counter()
    execution_time = end - start
    return cost, execution_time, centers


def greedy_k_center(dist, k):
    start = time.perf_counter()
    n = len(dist)
    centers = [0]
    min_dist = [float('inf')] * n
    while len(centers) < k:
        last_center = centers[-1]
        for i in range(n):
            d = dist[i][last_center]
            if d < min_dist[i]:
                min_dist[i] = d

        farthest_point = -1
        maximum_distance = -1.0

        for i in range(n):
            if min_dist[i] > maximum_distance:
                maximum_distance = min_dist[i]
                farthest_point = i
        centers.append(farthest_point)

    cost = calculate_cost(dist, centers)
    end = time.perf_counter()
    execution_time = end - start
    return cost, execution_time, centers


def main():
    toy_data = [[1.0, 2.0],[2.0, 3.0],[3.0, 1.0],[8.0, 8.0],[9.0, 8.0],[10.0, 9.0],[15.0, 2.0],[16.0, 3.0]]
    k = 3
    dist = distance_matrix(toy_data)

    cost, t, centers = library_heuristic(toy_data, dist, k)
    g_cost, g_time, g_centers = greedy_k_center(dist, k)

    datasets = {
        "Iris": load_iris().data,
        "Wine": load_wine().data,
        "Breast_Cancer": load_breast_cancer().data,
        "Digits": load_digits().data,
        "Diabetes": load_diabetes().data
    }
    results = []
    k = 5

    for name, original_data in datasets.items():
        data = original_data.tolist()
        scaler = StandardScaler()
        data = scaler.fit_transform(data).tolist()

        points = len(data)
        features = len(data[0])
        dist = distance_matrix(data)

        cost, execution_time, centers = library_heuristic(data, dist, k)
        g_cost, g_time, g_centers = greedy_k_center(dist, k)

        results.append({"data": name,"points": points,"features": features,
            "cost": cost,"time": execution_time,"g_cost": g_cost,"g_time": g_time})

    df = pd.DataFrame(results)
    df.to_csv("kcenter_results.csv", index=False)

    plt.figure(figsize=(8, 4))
    plt.plot(df["data"],df["cost"], marker='o', label="heuristic")
    plt.plot(df["data"],df["g_cost"], marker='o', label="Greedy")
    plt.title("Cost Compare")
    plt.ylabel("Cost")
    plt.legend()
    plt.grid()
    plt.show()

    plt.figure(figsize=(8, 4))
    plt.plot(df["data"],df["time"]* 1000, marker='o', label="heuristic")
    plt.plot(df["data"],df["g_time"]*1000, marker='o', label="Greedy")
    plt.title("Execution Time Compare")
    plt.ylabel("Time")
    plt.legend()
    plt.grid()
    plt.show()

main()