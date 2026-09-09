def maximal_matching(edges):
    match = []
    vc = []

    vc.append(edges[0][0])
    vc.append(edges[0][1])

    for u,v in edges:
        if u not in vc and v not in vc:
            vc.append(u)
            vc.append(v)
            match.append((u,v))

    return match