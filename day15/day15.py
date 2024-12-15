import sys
import time

def print_grid(grid):
    print('\033[H\033[J', end="")
    for row in grid:
        print(''.join(row))
        
def robot_start(grid):
    width = len(grid[0])
    height = len(grid)
    for ry in range(height):
        for rx in range(width):
            if grid[ry][rx] == '@':
                return (rx, ry)
    return None           

movements = {'^': (0, -1),  'v': (0, 1), '>': (1, 0), '<': (-1, 0)}

def push_box(bx, by, dx, dy, grid):
    nx = bx + dx
    ny = by + dy
    if grid[ny][nx] == '#':
        # Box hit obstacle, stop and return False
        return False
    if grid[ny][nx] == 'O':
        # Box is pushing box
        if not push_box(nx, ny, dx, dy, grid):
            # Cannot push other boxes, stop and return False
            return False
    # Everything ok, update box position
    grid[ny][nx] = 'O'
    return True

def try_vertical_push(bx, by, dy, grid):
    nx = bx
    ny = by + dy
    if grid[ny][nx] == '#' or grid[ny][nx + 1] == '#':
        # Box hit obstacle, return False
        return False
    if grid[ny][nx] == '[':
        # Single push
        return try_vertical_push(nx, ny, dy, grid)
    if grid[ny][nx] == ']':
        # Push box on the left
        left = try_vertical_push(nx - 1, ny, dy, grid)
    else:
        left = True
    if grid[ny][nx+1] == '[':
        # Push box on the right
        right = try_vertical_push(nx + 1, ny, dy, grid)
    else:
        right = True
    return left and right

def do_vertical_push(bx, by, dy, grid):
    nx = bx
    ny = by + dy
    if grid[ny][nx] == '[':
        # Single push
        do_vertical_push(nx, ny, dy, grid)
    if grid[ny][nx] == ']':
        # Left push
        do_vertical_push(nx - 1, ny, dy, grid)
    if grid[ny][nx + 1] == '[':
        # Right push
        do_vertical_push(nx + 1, ny, dy, grid)
    # Update box position
    grid[ny][nx] = '['
    grid[ny][nx+1] = ']'
    grid[by][bx] = '.'
    grid[by][bx+1] = '.'
    

def push_widebox(bx, by, dx, dy, grid):
    print("Push box at", bx, by, "by", dx, dy)
    nx = bx + dx
    ny = by + dy
    if dx == 0:
        if not try_vertical_push(bx, by, dy, grid):
            return False
        do_vertical_push(bx, by, dy, grid)
        return True
    if grid[ny][nx] == '#' or grid[ny][nx + 1] == '#':
        # Box hit obstacle, stop and return False
        return False
    if grid[ny][nx] == ']' and grid[ny][nx + 1] == '[':
        # Box is pushing box
        if not push_widebox(bx + 2*dx, by + 2*dy, dx, dy, grid):
            # Cannot push other boxes, stop and return False
            return False
    # Everything ok, update box position
    grid[ny][nx] = '['
    grid[ny][nx+1] = ']'
    return True
        

def do_command(rx, ry, cmd, grid):
    width = len(grid[0])
    height = len(grid)
    (dx, dy) = movements[cmd]
    nx = rx + dx
    ny = ry + dy
    if grid[ny][nx] == '#':
        # Robot hit obstacle, stop and return current position
        return (rx, ry)
    if grid[ny][nx] == '[':
        # Push the box(es)
        if not push_widebox(nx, ny, dx, dy, grid):
            # Cannot push boxes, stop and return current position
            return (rx, ry)
    if grid[ny][nx] == ']':
        # Push the box(es)
        if not push_widebox(nx - 1, ny, dx, dy, grid):
            # Cannot push boxes, stop and return current position
            return (rx, ry)
    # Robot can move, update robot position
    grid[ry][rx] = '.'
    grid[ny][nx] = '@'
    return (nx, ny)
    
def sum_of_coordinates(grid):
    width = len(grid[0])
    height = len(grid)
    result = sum([ sum([100 *j + i for i in range(width) if grid[j][i] in ['O','['] ]) for j in range(height)])
    return result
    
widen = {'.': '..', '#': '##', 'O': '[]', '@': '@.'}

if len(sys.argv) != 2:
    filename = "test1.txt"
else:
    filename = sys.argv[1]
infile = open(filename)

## Load grid from file. Stop at first empty line
grid = []
for line in infile:
    if len(line) == 1:
        break
    line = line.strip()
    for c in '.#O@':
        line = line.replace(c, widen[c])
    grid.append(list(line.strip()))

## Load robot commands from file
cmd = ''
for line in infile:
    cmd += line.strip()

rx, ry = robot_start(grid)



for c in cmd:
    print_grid(grid)
    print(rx, ry, c)    
    time.sleep(0.01)
    # input()
    (nx, ny) = do_command(rx, ry, c, grid)
    (rx, ry) = (nx, ny)

print_grid(grid)
print(rx, ry, c)    

print(sum_of_coordinates(grid))

    