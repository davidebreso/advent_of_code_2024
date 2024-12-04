## Advent of code 2024 - Day 4 - Problem 2

def doSearch(a, i, j):
    if a[i][j] != 'A':
        return 0
    # print(i, j)
    if a[i-1][j-1] not in ['M', 'S']:
        return 0
    if a[i+1][j+1] not in ['M', 'S']:
        return 0
    if a[i+1][j-1] not in ['M', 'S']:
        return 0
    if a[i-1][j+1] not in ['M', 'S']:
        return 0
    if a[i-1][j-1] == a[i+1][j+1]:
        return 0
    if a[i+1][j-1] == a[i-1][j+1]:
        return 0
    return 1        

#infile = open("test.txt")
infile = open("input.txt")

a = [row.strip() for row in infile]
n = len(a)
m = len(a[0])

#for row in a:
#    print(row)

count = 0   
for i in range(1,n-1):
    for j in range(1,m-1):
        count += doSearch(a, i, j)
        
print(count)