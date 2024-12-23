import sys

def find_paths(source, target, hops, graph, visited):
    if hops == 0:
        if source == target:
            return 1
        else:
            return 0
    paths = 0
    for succ in graph[source] - visited:
        paths += find_paths(succ, target, hops - 1, graph, visited)
    return paths

def count_all_3cliques(graph):
    visited = set()
    cliques = 0
    for source in graph:
        if source[0] == 't':
            cliques += find_paths(source, source, 3, graph, visited)
            visited.add(source)
    return cliques // 2

def maximal_clique(graph):
    # Build empty set of cliques
    cliques = list()
    for node in graph:
        found = False
        for clique in cliques:
            if clique <= graph[node]:
                clique.add(node) 
                found = True
                break
        if not found:
            cliques.append({node})
    return max(cliques, key=len)

def maximum_clique(graph):
    r = set()
    p = set(graph.keys())
    x = set()
    cliques = BronKerbosh(r, p, x, graph)
    return max(cliques, key=len)
    
def BronKerbosh(r, p, x, graph):
    if len(p) == 0 and len(x) == 0:
        return [r]
    cliques = list()
    u = (p | x).pop()
    for v in list(p - graph[u]):
        cliques.extend(BronKerbosh(r | {v}, p & graph[v], x & graph[v], graph))
        p.remove(v)
        x.add(v)
    return cliques

infile = open(sys.argv[1])

graph = dict()
for line in infile:
    s, t = line.strip().split('-') 
    graph[s] = graph.get(s, set()) | {t}
    graph[t] = graph.get(t, set()) | {s}

print("Part 1:", count_all_3cliques(graph))
clique = maximum_clique(graph)
print("Part 2:", ",".join(sorted(clique)))

