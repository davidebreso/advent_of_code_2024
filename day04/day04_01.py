## Advent of code 2024 - Day 4 - Problem 1

def doSearch(a, i, j, text, di, dj):
    if len(text) == 0:
        return 1
    if a[i][j] != text[0]:
        return 0
    return doSearch(a, i + di, j + dj, text[1:], di, dj)

def startSearch(a, i, j, text):
    if a[i][j] != text[0]:
        return 0
    count = 0
    text = text[1:]
    # Search right
    if j < len(a[i]) - len(text):
        count += doSearch(a, i, j + 1, text, 0, 1)
        # Search right up
        if i < len(a) - len(text):
            count += doSearch(a, i + 1, j + 1, text, 1, 1)
        # Search right down
        if i >= len(text):
            count += doSearch(a, i - 1, j + 1, text, -1, 1)
    # Search left
    if j >= len(text):
        count += doSearch(a, i, j - 1, text, 0, -1)
        # Search left up
        if i < len(a) - len(text):
            count += doSearch(a, i + 1, j - 1, text, 1, -1)
        # Search left down
        if i >= len(text):
            count += doSearch(a, i - 1, j - 1, text, -1, -1)
    # Search up
    if i < len(a) - len(text):
        count += doSearch(a, i + 1, j, text, 1, 0)
    # Search left
    if i >= len(text):
        count += doSearch(a, i - 1, j, text, -1, 0)
    
    return count
    
# infile = open("test.txt")
infile = open("input.txt")

a = [row.strip() for row in infile]
n = len(a)
m = len(a[0])

for row in a:
    print(row)

count = 0   
for i in range(n):
    for j in range(m):
        count += startSearch(a, i, j, "XMAS")
        
print(count)