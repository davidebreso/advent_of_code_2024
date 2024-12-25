import sys

def read_tuple(infile):
    key = list()
    row = infile.readline().strip()
    for c in row:
        if c == '.':
            key.append(0)
        else:
            key.append(1)
    height = 1
    row = infile.readline().strip()
    while row != "":
        height += 1
        for i in range(len(row)):
            if row[i] == '#':
                key[i] += 1
        row = infile.readline().strip()
    return (height, key)

infile = open(sys.argv[1])

keys = list()
locks = list()

for row in infile:
    if row[0] == '.':
        locks.append(read_tuple(infile))
    elif row[0] == '#':
        keys.append(read_tuple(infile))

pairs = len(locks) * len(keys)
for height, lock in locks:
    for _, key in keys:
        for i in range(len(lock)):
            if key[i] + lock[i] > height:
                pairs -= 1
                break
print(pairs, "unique lock/key pairs fit together without overlapping")


