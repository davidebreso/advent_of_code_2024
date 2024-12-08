def check_one(test, equation):
    if len(equation) == 1:
        return test == equation[0]
    one = equation[0]
    two = equation[1]
    tail = equation[2:]
    res = check_one(test, [one * two] + tail)
    return res or check_one(test, [one + two] + tail)

def check_two(test, equation):
    if len(equation) == 1:
        return test == equation[0]
    one = equation[0]
    two = equation[1]
    tail = equation[2:]
    res = check_two(test, [one * two] + tail)
    res = res or check_two(test, [one + two] + tail)
    return res or check_two(test, [int(str(one)+str(two))] + tail)

infile = open("input.txt")

result_one = 0
result_two = 0
for row in infile:
    test, equation = row.strip().split(":")
    test = int(test)
    equation = [int(n) for n in equation.split()]
    if check_one(test, equation):
        result_one += test
    if check_two(test, equation):
        result_two += test
    
print(result_one)
print(result_two)
