
def check(update, rules):
    fixed = False
    i = 0
    while i < len(update) - 1:
        x = update[i]
        if x not in rules:
            i += 1
            continue
        for j in range(i+1, len(update)):
            if update[j] in rules[x]:
                fixed = True
                update[i] = update[j]
                update[j] = x
                i -= 1
                break
        i += 1
    if fixed:
        return update[len(update) // 2]
    else:
        return 0
    
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