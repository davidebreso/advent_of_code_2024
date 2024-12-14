import heapq
import re

def shortest_path(xa, ya, xb, yb, xp, yp):
    heap = [(0, 0, 0, 'A')]
    heapq.heapify(heap)
    while len(heap) > 0:
        cost, x, y, btn = heapq.heappop(heap)
        #print("Popped", cost, x, y, btn)
        if x > xp or y > yp:
            continue
        if x == xp and y == yp:
            return cost
        # Press button A only if button is not B
        if btn == 'A':
            heapq.heappush(heap, (cost + 3, x + xa, y + ya, 'A'))
        # Press button B
        heapq.heappush(heap, (cost + 1, x + xb, y + yb, 'B'))
    return 0

infile = open("input.txt")

tokens = 0
while row := infile.readline():
    xa, ya = (int(s) for s in re.split("\+|=|,| |\t|\n", row) if s.isdigit() )
    row = infile.readline()
    xb, yb = (int(s) for s in re.split("\+|=|,| |\t|\n", row) if s.isdigit() )
    row = infile.readline()
    xp, yp = (int(s) for s in re.split("\+|=|,| |\t|\n", row) if s.isdigit() )
    tokens += shortest_path(xa, ya, xb, yb, xp, yp)
    row = infile.readline()   
print(tokens)