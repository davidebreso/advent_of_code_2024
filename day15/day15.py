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

def do_command(rx, ry, cmd, grid):
    width = len(grid[0])
    height = len(grid)
    (dx, dy) = movements[cmd]
    nx = rx + dx
    ny = ry + dy
    if grid[ny][nx] == '#':
        # Robot hit obstacle, stop and return current position
        return (rx, ry)
    if grid[ny][nx] == 'O':
        # Push the box(es)
        if not push_box(nx, ny, dx, dy, grid):
            # Cannot push boxes, stop and return current position
            return (rx, ry)
    # Robot can move, update robot position
    grid[ry][rx] = '.'
    grid[ny][nx] = '@'
    return (nx, ny)
    
def sum_of_coordinates(grid):
    width = len(grid[0])
    height = len(grid)
    result = sum([ sum([100 *j + i for i in range(width) if grid[j][i] == 'O']) for j in range(height)])
    return result
    
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
    (nx, ny) = do_command(rx, ry, c, grid)
    (rx, ry) = (nx, ny)

print_grid(grid)
print(rx, ry, c)    

print(sum_of_coordinates(grid))

    