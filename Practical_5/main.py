import csv
import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import (load_iris,load_wine,
    load_breast_cancer,load_digits,load_diabetes)



def calculate_cost(X, centers):
    distances = np.linalg.norm(
        X[:, np.newaxis, :] - centers[np.newaxis, :, :], axis=2)
    nearest_distances = np.min(distances, axis=1)
    return np.max(nearest_distances)

def library_kcenter(X, k):
    start = time.perf_counter()
    model = KMeans(n_clusters=k,random_state=42,n_init=10)
    model.fit(X)
    elapsed = time.perf_counter() - start

    centers = model.cluster_centers_
    cost = calculate_cost(X, centers)
    return cost, elapsed


def greedy_kcenter(X, k):
    start = time.perf_counter()
    n = len(X)

    centers = [X[0]]
    nearest_distances = np.linalg.norm(X - X[0], axis=1)


    for i in range(1, k):
        farthest_index = np.argmax(nearest_distances)
        new_center = X[farthest_index]
        centers.append(new_center)
        new_distances = np.linalg.norm(X - new_center, axis=1)

        nearest_distances = np.minimum(nearest_distances,new_distances)

    elapsed = time.perf_counter() - start
    centers = np.array(centers)
    cost = np.max(nearest_distances)
    return cost, elapsed


toy_data = np.array([[1, 1],[2, 1],[3, 2],[8, 8],
     [9, 8],[10, 9],[15, 15],[16, 15],[17, 16]], dtype=float)
k = 3

cost1, time1 = library_kcenter(toy_data, k)
cost2, time2 = greedy_kcenter(toy_data, k)
results = [["Toy", len(toy_data), toy_data.shape[1], k, cost1, time1, cost2, time2],]



datasets = {"Iris": load_iris(),"Wine": load_wine(),
    "Breast Cancer": load_breast_cancer(),
    "Digits": load_digits(),"Diabetes": load_diabetes()}
k = 5

for name, dataset in datasets.items():
    X = dataset.data

    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    cost1, time1 = library_kcenter(X, k)
    cost2, time2 = greedy_kcenter(X, k)
    results.append([name, len(X), X.shape[1], k, cost1, time1, cost2, time2])


with Path(__file__).with_name("result.csv").open("w", newline="") as output_file:
    w = csv.writer(output_file)
    w.writerow([
        "Dataset", "Points", "Features", "K",
        "KMeans Cost", "KMeans Time", "Greedy Cost", "Greedy Time",
    ])
    w.writerows(results)