def maximal_matching(edges):
    match = []
    vc = []
    u,v = edges[0][0], edges[0][1]
    vc.append(u)
    vc.append(v)
    match.append((u,v))

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

n, m, edges = read_input(1)
vc, match = maximal_matching(edges)
print(n, m, edges)
print(vc, len(vc), match)