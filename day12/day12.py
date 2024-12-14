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

def add_h_segment(x1, y1, x2, y2, sides):
    change = True
    while change:
        change = False
        for (x3, y3, x4, y4) in sides:
            if x3 == x4 == x1:
                if y2 == y3:
                    sides.remove((x3, y3, x4, y4))
                    (x1, y1, x2, y2) = (x1, y1, x4, y4)
                    change = True
                    break
                elif y4 == y1:
                    sides.remove((x3, y3, x4, y4))
                    (x1, y1, x2, y2) = (x3, y3, x2, y2)
                    change = True
                    break
    sides.add((x1, y1, x2, y2))

def add_v_segment(x1, y1, x2, y2, sides):
    change = True
    while change:
        change = False
        for (x3, y3, x4, y4) in sides:
            if y3 == y4 == y1:
                if x2 == x3:
                    sides.remove((x3, y3, x4, y4))
                    (x1, y1, x2, y2) = (x1, y1, x4, y4)
                    change = True
                    break
                elif x4 == x1:
                    sides.remove((x3, y3, x4, y4))
                    (x1, y1, x2, y2) = (x3, y3, x2, y2)
                    change = True
                    break
    sides.add((x1, y1, x2, y2))

def compute_discount(x, y, grid, xmax, ymax, sides):
    rid = grid[x][y]
    grid[x][y] = rid.upper()
    area = 1
    if x > 0:
        if grid[x - 1][y] == rid:
            area += compute_discount(x - 1, y, grid, xmax, ymax, sides)
        elif grid[x - 1][y] != rid.upper():
            add_h_segment(x, y, x, y + 1, sides)
    else:
        add_h_segment(x, y, x, y + 1, sides)
    if x < xmax:
        if grid[x + 1][y] == rid:
            area += compute_discount(x + 1, y, grid, xmax, ymax, sides)
        elif grid[x + 1][y] != rid.upper():
            add_h_segment(x + 1, y, x + 1, y + 1, sides)
    else:
        add_h_segment(x + 1, y, x + 1, y + 1, sides)
    if y > 0:
        if grid[x][y - 1] == rid:
            area += compute_discount(x, y - 1, grid, xmax, ymax, sides)
        elif grid[x][y - 1] != rid.upper():
            add_v_segment(x, y, x + 1, y, sides)
    else:
        add_v_segment(x, y, x + 1, y, sides)
    if y < ymax:
        if grid[x][y + 1] == rid:
            area += compute_discount(x, y + 1, grid, xmax, ymax, sides)
        elif grid[x][y + 1] != rid.upper():
            add_v_segment(x, y + 1, x + 1, y + 1, sides)
    else:
        add_v_segment(x, y + 1, x + 1, y + 1, sides)
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
    sides = set()
    area = compute_discount(x, y, grid, xmax, ymax, sides)
    print("Region", grid[x][y], "from", x, y, "has area", area, "with sides", sides)
    #input()
    return area * len(sides)
    
xsize = len(grid)
ysize = len(grid[0])    
cost = sum( [ sum([ region_cost(x, y, grid, xsize - 1, ysize - 1) for y in range(ysize) ]) for x in range(xsize)] )
print("Standard cost:", cost)
cost = sum( [ sum([ region_discount(x, y, grid, xsize - 1, ysize - 1) for y in range(ysize) ]) for x in range(xsize)] )
print("Bulk discount cost:", cost)