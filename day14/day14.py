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

# robot = [2, 4, 2, -3]
# 
# print(robot)
# for i in range(5):
#     update_robot(robot, 1, 11, 7)
#     print(robot)

infile = open("input.txt")
xsize = 101
ysize = 103

robots = []
for row in infile:
    robots.append(ints(row))

for robot in robots:
    update_robot(robot, 100, xsize, ysize)

print(safety_factor(robots, xsize, ysize))
    