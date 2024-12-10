from collections import deque

def bfs(map, i, j, n, m):
    # print("Start: ", i, j, map[i][j])
    if map[i][j] != 0:
        return (0, 0)
    trails = set()
    count = 0
    q = deque()
    q.append((i,j))
    while len(q) > 0:
        #print(q)
        (x,y) = q.popleft()
        h = map[x][y]
        # print("Pop: ", x, y, h, q)
        if h == 9:
            trails.add((x, y))
            count += 1
            continue
        if x + 1 < n and map[x + 1][y] == h + 1:
            q.append((x + 1,y))
        if x > 0 and map[x - 1][y] == h + 1:
            q.append((x - 1,y))
        if y + 1 < n and map[x][y + 1] == h + 1:
            q.append((x,y + 1))
        if y > 0 and map[x][y - 1] == h + 1:
            q.append((x,y - 1))
    return len(trails), count
        
infile = open("input.txt")

map = [ [int(c) for c in row.strip()] for row in infile]

n = len(map)
m = len(map[0])

p1 = 0
p2 = 0
for i in range(n):
    for j in range(m):
        c1, c2 = bfs(map, i, j, n, m)
        p1 += c1
        p2 += c2

print(p1, p2)