def check(report):
    safe = True
    increase = (report[0] < report[1])
    for i in range(len(report) - 1):
        if report[i] == report[i+1]:
            return False
        if increase != (report[i] < report[i+1]):
            return False
        if abs(report[i] - report[i+1]) > 3:
            return False
    return True

infile = open('input2.txt')
count = 0

for line in infile:
    report = [int(i) for i in line.split()]
    if check(report):
        count += 1

print(count)