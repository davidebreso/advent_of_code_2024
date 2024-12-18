import sys
import re
from collections import deque 

directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}

def shortest_path(size, obstacles):
    queue = deque()
    queue.append((0, 0, 0))
    visited = set()
    while len(queue) > 0:
        c, x, y = queue.popleft()
        if (x, y) == (size-1, size-1):
            return c
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for (dx, dy) in directions:
            if (x + dx, y + dy) not in obstacles:
                queue.append((c +1, x + dx, y + dy))
    return -1
    
def path_to_exit(x, y, size, obstacles, visited):
    if (x, y) == (size-1, size-1):
        return [(x,y)]
    if (x, y) in visited:
        return [ ]
    visited.add((x, y))
    for (dx, dy) in directions:
        if (x + dx, y + dy) not in obstacles:
            path = path_to_exit(x + dx, y + dy, size, obstacles, visited)
            if len(path) > 0:
                return [(x, y)] + path
    return [ ]

def print_map(size, obstacles, path):
    for y in range(-1, size+1):
        for x in range(-1, size + 1):
            if (x, y) in obstacles:
                print("#", end="")
            elif (x, y) in path:
                print("O", end="")
            else:
                print(".", end="")
        print()

if len(sys.argv) != 4:
    print("Usage:", sys.argv[0], "nomefile size obstacles")
    sys.exit(1)
    
infile = open(sys.argv[1])
size = int(sys.argv[2])
num_obstacles = int(sys.argv[3])

obstacles = set()
for _ in range(num_obstacles):
    obstacles.add(tuple(int(s) for s in re.split(",| |\t|\n", infile.readline().strip())))
# Add a border around the map
for i in range(-1, size + 1):
    obstacles |= {(-1, i), (i, -1), (size, i), (i, size)}
print_map(size, obstacles, set())
print(shortest_path(size, obstacles))

path = path_to_exit(0, 0, size, obstacles, set())
#print(path)
while len(path) > 0:
    (x, y) = tuple(int(s) for s in re.split(",| |\t|\n", infile.readline().strip()))
    #print("New obstacle at", (x, y))
    obstacles.add((x, y))
    try:
        pos = path.index((x, y))
        path = path[:pos]
        newpath = []
        if pos > 0:
            (sx, sy) = path[pos - 1]
            #print("Restarting search from", (sx, sy))
            newpath = path_to_exit(sx, sy, size, obstacles, set())
            #print(newpath)
        if len(newpath) == 0:
            print("Obstacle at", (x, y), "blocks exit!")
            break
        path = path + newpath
    except ValueError:
        pass
    

