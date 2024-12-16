import sys
import heapq

def print_grid(grid):
    print('\033[H\033[J', end="")
    for row in grid:
        print(''.join(row))

def lowest_score(start, end, grid):
    visited = set()
    heap = [(0, start[0], start[1], 0, 1)]
    heapq.heapify(heap)
    while len(heap) > 0:
        w, r, c, dr, dc = heapq.heappop(heap)
        if (r, c) == end:
            return w
        if (r, c) in visited:
            continue
        visited.add((r, c))
        if grid[r + dr][c + dc] != '#':
            heapq.heappush(heap, (w + 1, r + dr, c + dc, dr, dc))
        if grid[r + dc][c + dr] != '#':
            heapq.heappush(heap, (w + 1001, r + dc, c + dr, dc, dr))
        if grid[r - dc][c - dr] != '#':
            heapq.heappush(heap, (w + 1001, r - dc, c - dr, -dc, -dr))
    return None

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
            continue
        if grid[r + dr][c + dc] != '#':
            heapq.heappush(heap, (w + 1, r + dr, c + dc, dr, dc))
        heapq.heappush(heap, (w + 1000, r, c, dc, dr))
        heapq.heappush(heap, (w + 1000, r, c, -dc, -dr))

def backward_cost(start, end, grid, costs):
    visited = set()
    (r, c) = end
    heap = [(0, r, c, 0, 1), (0, r, c, 1, 0), (0, r, c, 0, -1), (0, r, c, -1, 0)]
    heapq.heapify(heap)
    while len(heap) > 0:
        w, r, c, dr, dc = heapq.heappop(heap)
        if (r, c, dr, dc) in visited:
            continue
        costs[r, c, dr, dc] = w
        visited.add((r, c, dr, dc))
        if (r, c) == start and (dr, dc) == (0, 1):
            continue
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
    
infile = open(sys.argv[1])

grid = [ list(row.strip()) for row in infile ]
print_grid(grid)

start, end = find_endpoints(grid)
print("Lowest score from", start, "to", end, "is", lowest_score(start, end, grid))

fcosts = dict()
bcosts = dict()
forward_cost(start, end, grid, fcosts)
backward_cost(start, end, grid, bcosts)

mincost = bcosts[start[0], start[1], 0, 1]
seats = fcosts.keys() & bcosts.keys()
goodseats = { (p[0], p[1]) for p in seats if (fcosts[p] + bcosts[p] == mincost) }
print("Number of good seats:", len(goodseats))
for r, c in goodseats:
    grid[r][c] = 'O'

