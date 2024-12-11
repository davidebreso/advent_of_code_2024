from itertools import repeat

infile = open("input.txt")

memo = dict()

def blink(stone, n):
    if n == 0:
        return 1
    if (stone, n) in memo:
        return memo[stone, n]
    if stone == 0:
        res = blink(1, n - 1)
    else: 
        sstone = str(stone)
        l = len(sstone)
        if l % 2 == 0:
            h = l // 2
            res = blink(int(sstone[:h]), n - 1) + blink(int(sstone[h:]), n - 1)
        else:
            res = blink(stone*2024, n - 1)
    memo[stone, n] = res
    return res

stones = list(map(int, infile.read().split()))

result = sum(map(blink, stones, repeat(25)))
print("Part 1:", result)

result = sum(map(blink, stones, repeat(75)))
print("Part 2:", result)

    