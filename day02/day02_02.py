def check(report):
    safe = True
    increase = (report[0] < report[1])
    for i in range(len(report) - 1):
        if report[i] == report[i+1]:
            return i + 1
        if increase != (report[i] < report[i+1]):
            return i + 1
        if abs(report[i] - report[i+1]) > 3:
            return i + 1
    return -1

infile = open('input2.txt')
count = 0

for line in infile:
    report = [int(i) for i in line.split()]
    res = check(report)
    if res != -1:
        tmp = report[:]
        tmp.pop(res)
        res = check(tmp)
    if res != -1:
        tmp = report[1:]
        res = check(tmp)
    if res != -1:
        tmp = report[:]
        tmp.pop(1)
        res = check(tmp)
    if res == -1:
        count += 1

print(count)