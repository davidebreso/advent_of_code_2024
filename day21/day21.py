import sys
import heapq
import math

# Graph of the numeric keypad
# Node IDs (A is node 10)
numbuttons = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A']
numnodes = { '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
             '7': 7, '8': 8, '9': 9, 'A': 10 }
# Adjacency lists of the graph. 
# In each list, 0 is up, 1 si down, 2 is left, 3 is right
numpad = [
    [ 2,    None,   None,   10   ],     # Key 0
    [ 4,    None,   None,   2    ],     # Key 1
    [ 5,    0,      1,      3    ],     # Key 2
    [ 6,    10,     2,      None ],     # Key 3
    [ 7,    1,      None,   5    ],     # Key 4
    [ 8,    2,      4,      6    ],     # Key 5
    [ 9,    3,      5,      None ],     # Key 6
    [ None, 4,      None,   8    ],     # Key 7
    [ None, 5,      7,      9    ],     # Key 8
    [ None, 6,      8,      None ],     # Key 9
    [ 3,    None,   0,      None ]      # Key A
]

# Graph of the directional keypad
# Node IDs (A is node 4)
dirbuttons = ['^', 'v', '<', '>', 'A']
dirnodes = {'^': 0, 'v': 1, '<': 2, '>': 3, 'A': 4}
# Adjacency lists of the graph. 
# In each list, 0 is up, 1 si down, 2 is left, 3 is right
dirpad = [
    [ None, 1,      None,   4    ],     # Key ^
    [ 0,    None,   2,      3    ],     # Key v
    [ None, None,   None,   1    ],     # Key <
    [ 4,    None,   1,      None ],     # Key >
    [ None, 3,      0,      None ]      # Key A
]


def shortest_path(code, graph, buttons):
    heap = [(0, 10, code)]
    heapq.heapify(heap)
    visited = set()
    while len(heap) > 0:
        w, n, c = heapq.heappop(heap)
        if buttons[n] == c:
            return w + 1
        if (n, c) in visited:
            continue
        visited.add((n, c))
        if buttons[n] == c[0]:
            # Push button and consume first char of code
            heapq.heappush(heap, (w + 1, n, c[1:]))
        else:
            # Move on the four directions
            for d in range(4):
                succ = graph[n][d]
                if succ != None:
                    heapq.heappush(heap, (w + 1, succ, c))
    return math.inf
    
def all_paths(graph):
    size = len(graph)
    dist = [ [math.inf] * size for _ in range(size) ]
    for n in range(size):
        dist[n][n] = 1
        for d in range(4):
            succ = graph[n][d]
            if succ != None:
                dist[n][succ] = 2
    for k in range(size):
        for i in range(size):
            for j in range(size):
                if dist[i][j] > dist[i][k] + dist[k][j] - 1:
                    dist[i][j] = dist[i][k] + dist[k][j] - 1
    return dist

def single_source_all_paths(source, graph, dist):
    size = len(graph)
    newdist = [math.inf] * size
    heap = [(0, source, 4)]
    heapq.heapify(heap)
    visited = set()
    while len(heap) > 0:
        w, n, c = heapq.heappop(heap)
        if (n, c) in visited:
            continue
        visited.add((n, c))
        if newdist[n] > w + dist[c][4]:
            newdist[n] = w + dist[c][4]
        # Move on the four directions
        for d in range(4):
            succ = graph[n][d]
            if succ != None:
                heapq.heappush(heap, (w + dist[c][d], succ, d))
    return newdist

def indirect_all_paths(graph, dist):
    size = len(graph)
    newdist = []
    for n in range(size):
        newdist.append(single_source_all_paths(n, graph, dist))
    return newdist

def dial_code(code, dist, nodes):
    curr = nodes['A']       # Start from button A
    length = 0
    for c in code:
        succ = nodes[c]
        length += dist[curr][succ]
        curr = succ
    return length

def indirect_shortest_path(code, graph, buttons, dist):
    heap = [(0, 10, 4, code)]
    heapq.heapify(heap)
    visited = set()
    while len(heap) > 0:
        w, n, k, c = heapq.heappop(heap)
        if buttons[n] == c:
            return w + dist[k][4]
        if (n, c, k) in visited:
            continue
        visited.add((n, c, k))
        if buttons[n] == c[0]:
            # Push button and consume first char of code
            heapq.heappush(heap, (w + dist[k][4], n, 4, c[1:]))
        else:
            # Move on the four directions
            for d in range(4):
                succ = graph[n][d]
                if succ != None:
                    heapq.heappush(heap, (w + dist[k][d], succ, d, c))
    return math.inf

infile = open(sys.argv[1])

dirdist = all_paths(dirpad)
for _ in range(24):
    dirdist = indirect_all_paths(dirpad, dirdist)

complexity = 0
for code in infile:
    code = code.strip()
    cost = indirect_shortest_path(code, numpad, numbuttons, dirdist)
    print("Code", code, "with cost", cost)
    complexity += cost * int(code[:-1])
print("Sum of complexities:", complexity)
