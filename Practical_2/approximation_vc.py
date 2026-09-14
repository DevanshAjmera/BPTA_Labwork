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
    with open(f'Input/input{i}.txt', 'r') as f:
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

    with open('../Practical_1/result.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(rows)


if __name__ == '__main__':
    main()