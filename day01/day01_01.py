infile = open("input1.txt")
l1 = []
l2 = []
for row in infile:
    (a, b) = row.split()
    l1.append(int(a))
    l2.append(int(b))
l1.sort()
l2.sort()
dist = 0
for i in range(len(l1)):
    dist += abs(l1[i] - l2[i])
print(dist)
