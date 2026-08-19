def subsets(index,subset,vertexset):
    if index >= len(vertexset):
        powerset.append(subset.copy())
        return 

    subset.append(vertexset[index])
    subsets(index+1,subset,vertexset)
    subset.pop()
    subsets(index+1,subset,vertexset)

vertexset = [1,2,3]
powerset = []
subsets(0,[],vertexset)

def isvc(g,subset):
    for u,v in g.edges():
        if u not in subset or v not in subset:
            return False
    return True

def vc(g,vertices,powerset):
    min = float('inf')
    vc = vertices
    for subset in powerset:
        if isvc(g,subset) and min < len(subset):
            min = len(subset)
            vc = subset
    return vc