import sys
from itertools import repeat

infile = open(sys.argv[1])
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

def check_corner(rid, x, y, grid, xmax, ymax):
    n = []
    if x > 0:
        if y > 0:
            n.append(grid[x - 1][y - 1].lower())
        else:
            n.append("#")
        if y <= xmax:
            n.append(grid[x - 1][y].lower())
        else:
            n.append("#")
    else:
        n.extend(['#', '#'])        
    if x <= xmax:
        if y > 0:
            n.append(grid[x][y - 1].lower())
        else:
            n.append('#')
        if y <= ymax:
            n.append(grid[x][y].lower())
        else:
            n.append('#')
    else:
        n.extend(['#', '#'])  
    matches = n.count(rid)
    return (matches == 3) or (matches == 1) or (matches == 2 and n[0] == n[3])    
    
def compute_discount(rid, sx, sy, grid, xmax, ymax):
    ry = ymax
    for y in range(sy + 1, ymax + 1):
        if grid[sx][y] != rid:
            ry = y - 1
            break
        grid[sx][y] = rid.upper()        
    grid[sx][ry] = rid.upper()        
    ly = 0
    for y in range(sy - 1, -1, -1):
        if grid[sx][y] != rid:
            ly = y + 1
            break
        grid[sx][y] = rid.upper()
    grid[sx][ly] = rid.upper()                
    grid[sx][sy] = rid.upper()
    #print(rid, "line at", sx,"from",ly,"to", ry)
    area = ry - ly + 1
    if sx > 0:
        for y in range(ly, ry + 1):
            if grid[sx - 1][y] == rid:
                area += compute_discount(rid, sx - 1, y, grid, xmax, ymax)
    if sx < xmax:
        for y in range(ly, ry + 1):
            if grid[sx + 1][y] == rid:
                area += compute_discount(rid, sx + 1, y, grid, xmax, ymax)
    return area        
        
def region_cost(x, y, grid, xmax, ymax):
    if grid[x][y].islower():
        return 0
    area, perimeter = compute(grid[x][y], x, y, grid, xmax, ymax)
    # print("Region", grid[x][y], "from", x, y, "has cost", area * perimeter)
    return area * perimeter
    
def region_discount(x, y, grid, xmax, ymax):
    if grid[x][y].isupper():
        return 0
    area = compute_discount(grid[x][y], x, y, grid, xmax, ymax)
    print("Region", grid[x][y], "from", x, y, "has area", area)
    return area
    
xsize = len(grid)
ysize = len(grid[0])    
cost = sum( [ sum([ region_cost(x, y, grid, xsize - 1, ysize - 1) for y in range(ysize) ]) for x in range(xsize)] )
print("Standard cost:", cost)
cost = sum( [ sum([ region_discount(x, y, grid, xsize - 1, ysize - 1) for y in range(ysize) ]) for x in range(xsize)] )
print("Bulk discount cost:", cost)