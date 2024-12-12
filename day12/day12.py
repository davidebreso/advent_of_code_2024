from itertools import repeat

infile = open("input.txt")
grid = [ [ c for c in row.strip() ] for row in infile ]

def compute(rid, x, y, grid, xmax, ymax):
    cid = grid[x][y]
    if cid == rid.lower():
        return (0, 0)
    if cid != rid:
        return (0, 1)
    grid[x][y] = cid.lower()
    if x > 0:
        la, lp = compute(rid, x - 1, y, grid, xmax, ymax)
    else:
        la, lp = 0, 1
    if x < xmax:
        ra, rp = compute(rid, x + 1, y, grid, xmax, ymax)
    else:
        ra, rp = 0, 1
    if y > 0:
        da, dp = compute(rid, x, y - 1, grid, xmax, ymax)
    else:
        da, dp = 0, 1
    if y < ymax:
        ua, up = compute(rid, x, y + 1, grid, xmax, ymax)
    else:
        ua, up = 0, 1
    area = 1 + la + ra + ua + da
    perimeter = lp + rp + up + dp
    return(area, perimeter)
    
def region_cost(x, y, grid, xmax, ymax):
    if grid[x][y].islower():
        return 0
    area, perimeter = compute(grid[x][y], x, y, grid, xmax, ymax)
    # print("Region", grid[x][y], "from", x, y, "has cost", area * perimeter)
    return area * perimeter
    
xsize = len(grid)
ysize = len(grid[0])    
cost = sum( [ sum([ region_cost(x, y, grid, xsize - 1, ysize - 1) for y in range(ysize) ]) for x in range(xsize)] )
print(cost)
