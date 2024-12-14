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

def compute_discount(x, y, grid, xmax, ymax, segments):
    rid = grid[x][y]
    grid[x][y] = rid.upper()
    area = 1
    if x > 0:
        if grid[x - 1][y] == rid:
            area += compute_discount(x - 1, y, grid, xmax, ymax, segments)
        elif grid[x - 1][y] != rid.upper():
            segments.add((x, y, x, y + 1))
    else:
        segments.add((x, y, x, y + 1))
    if x < xmax:
        if grid[x + 1][y] == rid:
            area += compute_discount(x + 1, y, grid, xmax, ymax, segments)
        elif grid[x + 1][y] != rid.upper():
            segments.add((x + 1, y, x + 1, y + 1))
    else:
        segments.add((x + 1, y, x + 1, y + 1))
    if y > 0:
        if grid[x][y - 1] == rid:
            area += compute_discount(x, y - 1, grid, xmax, ymax, segments)
        elif grid[x][y - 1] != rid.upper():
            segments.add((x, y, x + 1, y))
    else:
        segments.add((x, y, x + 1, y))
    if y < ymax:
        if grid[x][y + 1] == rid:
            area += compute_discount(x, y + 1, grid, xmax, ymax, segments)
        elif grid[x][y + 1] != rid.upper():
            segments.add((x, y + 1, x + 1, y + 1))
    else:
        segments.add((x, y + 1, x + 1, y + 1))
    return area      
        
def region_cost(x, y, grid, xmax, ymax):
    if grid[x][y].islower():
        return 0
    area, perimeter = compute(grid[x][y], x, y, grid, xmax, ymax)
    # print("Region", grid[x][y], "from", x, y, "has cost", area * perimeter)
    return area * perimeter
    
def walk(x, y, dx, dy, segments, visited, xmax, ymax):
    if (x, y) in visited:
        return 0
    #print("Walking", x, y, dx, dy)
    visited.add((x, y))
    corners = 0
    if dx == 0:
        # Horizontal movement direction. Try to find a corner first
        if (x, y, x+1, y) in segments:
            # Change direction to NORTH and continue walk
            corners += 1 + walk(x+1, y, 1, 0, segments, visited, xmax, ymax)
        if (x - 1, y, x, y) in segments:
            # Change direction to SOUTH and continue walk
            corners += 1 + walk(x - 1, y, -1, 0, segments, visited, xmax, ymax)
    else:
        # Vertical movement direction. Try to find a corner first
        if (x, y, x, y+1) in segments:
            # Change direction to EAST and continue walk
            corners += 1 + walk(x, y+1, 0, 1, segments, visited, xmax, ymax)
        if (x, y - 1, x, y) in segments:
            # Change direction to WEST and continue walk
            corners += 1 + walk(x, y-1, 0, -1, segments, visited, xmax, ymax)
    # No corners, go straight
    (x1, y1, x2, y2) = (x, y, x + dx, y + dy)
    if dx < 0 or dy < 0:
        (x1, y1, x2, y2) = (x2, y2, x1, y1)
    if (x1, y1, x2, y2) in segments:
        corners += walk(x + dx, y + dy, dx, dy, segments, visited, xmax, ymax)
    return corners
    
def compute_corners(segments, xmax, ymax):
    visited = set()
    corners = 0
    for (x1, y1, x2, y2) in segments:
        if (x2, y2) not in visited:
            corners += walk(x2, y2, x2-x1, y2-y1, segments, visited, xmax, ymax)
    return corners

def region_discount(x, y, grid, xmax, ymax):
    if grid[x][y].isupper():
        return 0
    segments = set()
    area = compute_discount(x, y, grid, xmax, ymax, segments)
    perimeter = len(segments)
    sides = compute_corners(segments, xmax, ymax)
    #print("Region", grid[x][y], "from", x, y, "has area", area, "with perimeter", perimeter, "and sides", sides)
    #input()
    return area * sides
    
xsize = len(grid)
ysize = len(grid[0])    
cost = sum( [ sum([ region_cost(x, y, grid, xsize - 1, ysize - 1) for y in range(ysize) ]) for x in range(xsize)] )
print("Standard cost:", cost)
cost = sum( [ sum([ region_discount(x, y, grid, xsize - 1, ysize - 1) for y in range(ysize) ]) for x in range(xsize)] )
print("Bulk discount cost:", cost)