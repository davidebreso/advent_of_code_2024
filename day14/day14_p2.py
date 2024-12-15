import re

def ints(row):
    l = []
    for s in re.split("=|,| |\t|\n", row):
        try:
            l.append(int(s))
        except ValueError:
            pass
    return l

def update_robot(robot, time, xsize, ysize):
    # robot is [ x, y, vx, vy ]
    vx = robot[2]
    vy = robot[3]
    robot[0] = (robot[0] + vx * time) % xsize
    robot[1] = (robot[1] + vy * time) % ysize

def safety_factor(robots, xsize, ysize):
    ur = ul = dr = dl = 0
    midx = xsize // 2
    midy = ysize // 2
    for robot in robots:
        (x, y) = (robot[0], robot[1])
        if x < midx:
            if y < midy:
                ul += 1
            elif y > midy:
                dl += 1
        if x > midx:
            if y < midy:
                ur += 1
            elif y > midy:
                dr += 1
    return ur * ul * dr * dl
    
def print_robots(robots, xsize, ysize):
    grid = [ [ '.' for x in range(xsize) ] for y in range(ysize) ]
    for robot in robots:
        if grid[robot[1]][robot[0]] == '.':
            grid[robot[1]][robot[0]] = '1'
        else:
            grid[robot[1]][robot[0]] =chr(ord(grid[robot[1]][robot[0]]) + 1)        
    for row in grid:
        print(''.join(row))

def check_tree(robots, xsize, ysize):
    points = set()
    for robot in robots:
        points.add((robot[0],robot[1]))
    numrobots = len(robots)
    maxtree = 1
    for (x, y) in points:
        tree = {(x,y)}
        for i in range(1, 5):
            tree.add((x - i, y + i))
            tree.add((x + i, y + i))
        if tree <= points:
            print(sorted(tree))
            return True
    #print(maxtree, "robots on a tree")
    return False


infile = open("test1.txt")
xsize = 11
ysize = 7

infile = open("input.txt")
xsize = 101
ysize = 103

robots = []
for row in infile:
    robots.append(ints(row))

i = 0
for i in range(1, 100000):
    for robot in robots:
        update_robot(robot, 1, xsize, ysize)
    # print_robots(robots, xsize, ysize)
    if check_tree(robots, xsize, ysize):
        print("Trovato!")
        break
    #print(i)
    #input()

print_robots(robots, xsize, ysize)
print(i)

    