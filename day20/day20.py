import sys
import heapq
import math

directions = { (0, 1), (0, -1), (1, 0), (-1, 0) }

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def compute_shortest_paths(end, grid):
    heap = [(0, end[0], end[1])]
    heapq.heapify(heap)
    rows = len(grid)
    cols = len(grid[0])
    costs = [ [-1] * cols for _ in range(rows) ];
    while len(heap) > 0:
        w, r, c = heapq.heappop(heap)
        if costs[r][c] >= 0:
            continue
        costs[r][c] = w
        for (dr, dc) in directions:
            if grid[r + dr][c + dc] != '#':
                heapq.heappush(heap, (w + 1, r + dr, c + dc))
    return costs
    
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
    
def find_cheats(minsave, costs):
    rows = len(costs)
    cols = len(costs[0])
    cheats = list()
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Check if horizontal cheat
            if costs[r][c - 1] >= 0 and costs[r][c + 1] >= 0:
                save = abs(costs[r][c - 1] - costs[r][c + 1]) - 2
                if save >= minsave:
                    cheats.append(save)
            # Check if vertical cheat
            if costs[r - 1][c] >= 0 and costs[r + 1][c] >= 0:
                save = abs(costs[r - 1][c] - costs[r + 1][c]) - 2
                if save >= minsave:
                    cheats.append(save)             
    return cheats
    
def find_longer_cheats(start, minsave, maxsteps, costs):
    rows = len(costs)
    cols = len(costs[0])
    cheats = list()
    startcost = costs[start[0]][start[1]]
    heap = [(0, start[0], start[1])]
    heapq.heapify(heap)
    visited = set()
    while len(heap) > 0:
        w, r, c = heapq.heappop(heap)
        if (r, c) in visited:
            continue
        visited.add((r, c))
        if w > maxsteps:
            continue
        if costs[r][c] >= 0:
            save = startcost - costs[r][c] - w
            if save >= minsave:
                cheats.append((save, start, (r, c)))
        for (dr, dc) in directions:
            if 0 < r + dr < rows - 1 and 0 < c + dc < cols - 1:
                heapq.heappush(heap, (w + 1, r + dr, c + dc))
    return cheats 
    
def find_all_cheats(minsave, maxsteps, costs):
    rows = len(costs)
    cols = len(costs[0])
    cheats = list()
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if costs[r][c] > 0:
                cheats.extend(find_longer_cheats((r, c), minsave, maxsteps, costs))
    return cheats

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "inputfile")
    sys.exit(1)

infile = open(sys.argv[1])
grid = [ list(row.strip()) for row in infile ]

start, end = find_endpoints(grid)
costs = compute_shortest_paths(end, grid)
print("Lowest score with no cheating from", start, "to", end, "is", costs[start[0]][start[1]])
cheats = find_cheats(100, costs)
print(len(cheats), "cheats saves at least 100 picoseconds")
cheats = find_all_cheats(100, 20, costs)
print(len(cheats), "longer cheats saves at least 100 picoseconds")

