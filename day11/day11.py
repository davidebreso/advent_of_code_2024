infile = open("input.txt")

def blink(stones):
    res = []
    for stone in stones:
        if stone == 0:
            res.append(1)
            continue
        sstone = str(stone)
        l = len(sstone)
        if l % 2 == 0:
            h = l // 2
            res.append(int(sstone[:h]))
            res.append(int(sstone[h:]))
        else:
            res.append(stone*2024)
    return res

stones = map(int, infile.read().split())

for i in range(25):
    #print(stones)
    stones = blink(stones)

#print(stones)
print(len(stones))

print("more blinking")
for i in range(50):
    #print(stones)
    print(i)
    stones = blink(stones)

print(len(stones))
    