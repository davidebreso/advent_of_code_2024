def check(update, rules):
    for i in range(len(update) - 1):
        x = update[i]
        if x not in rules:
            continue
        for j in range(i+1, len(update)):
            if update[j] in rules[x]:
                return 0
    return update[len(update) // 2]
    
infile = open("input.txt")

rules = dict()

for row in infile:
    row = row.strip()
    if len(row) == 0:
        break
    low, high = (int(n) for n in row.split("|"))
    if high in rules:
        rules[high].add(low)
    else:
        rules[high] = {low}

sum = 0
for row in infile:
    update = [int(n) for n in row.strip().split(",")]
    sum += check(update, rules)
    
print(sum)