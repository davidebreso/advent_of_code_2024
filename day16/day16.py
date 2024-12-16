import sys
import heapq
import math

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def forward_cost(start, end, grid, costs):
    visited = set()
    heap = [(0, start[0], start[1], 0, 1)]
    heapq.heapify(heap)
    while len(heap) > 0:
        w, r, c, dr, dc = heapq.heappop(heap)
        if (r, c, dr, dc) in visited:
            continue
        costs[r, c, dr, dc] = w
        visited.add((r, c, dr, dc))
        if (r, c) == end:
            return w
        if grid[r + dr][c + dc] != '#':
            heapq.heappush(heap, (w + 1, r + dr, c + dc, dr, dc))
        heapq.heappush(heap, (w + 1000, r, c, dc, dr))
        heapq.heappush(heap, (w + 1000, r, c, -dc, -dr))
    return math.inf
    
def backward_cost(start, end, grid, costs, spots):
    visited = set()
    (r, c) = end
    heap = [(0, r, c, 0, 1), (0, r, c, 1, 0), (0, r, c, 0, -1), (0, r, c, -1, 0)]
    heapq.heapify(heap)
    while len(heap) > 0:
        w, r, c, dr, dc = heapq.heappop(heap)
        if (r, c, dr, dc) not in spots or (r, c, dr, dc) in visited:
            continue
        costs[r, c, dr, dc] = w
        visited.add((r, c, dr, dc))
        if (r, c) == start and (dr, dc) == (0, 1):
            return
        if grid[r - dr][c - dc] != '#':
            heapq.heappush(heap, (w + 1, r - dr, c - dc, dr, dc))
        heapq.heappush(heap, (w + 1000, r, c, dc, dr))
        heapq.heappush(heap, (w + 1000, r, c, -dc, -dr))

    
def find_endpoints(grid):
    found = 0
    start = end = (0, 0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'S':
                start = (r, c)
                found += 1
            if grid[r][c] == 'E':
                end = (r, c)
                found += 1
            if found >= 2:
                break
    return start, end

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "inputfile")
    sys.exit(1)

infile = open(sys.argv[1])
grid = [ list(row.strip()) for row in infile ]

start, end = find_endpoints(grid)
fcosts = dict()
print("Lowest score from", start, "to", end, "is", forward_cost(start, end, grid, fcosts))

bcosts = dict()
backward_cost(start, end, grid, bcosts, fcosts)

mincost = bcosts[start[0], start[1], 0, 1]
goodspots = { (p[0], p[1]) for p in bcosts if (fcosts[p] + bcosts[p] == mincost) }
print("Number of good spots:", len(goodspots))

