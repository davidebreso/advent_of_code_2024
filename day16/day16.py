import sys
import heapq

def print_grid(grid):
    print('\033[H\033[J', end="")
    for row in grid:
        print(''.join(row))

def lowest_score(start, end, grid):
    heap = [(0, start[0], start[1], 0, 1)]
    visited = set()
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


