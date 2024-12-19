import sys

def design_match(design, towels):
    if len(design) == 0:
        return True
    for towel in towels:
        if design.startswith(towel) and design_match(design[len(towel):], towels):
            return True
    return False

if len(sys.argv) == 2:
    infile = open(sys.argv[1])
else:
    infile = open("test1.txt")
    
towels = infile.readline().strip().split(", ")
infile.readline()
print("Towels:", towels)

possible_designs = 0
for design in infile:
    design = design.strip()
    if design_match(design, towels):
        print("Design", design, "is possible")
        possible_designs += 1
    else:
        print("Design", design, "is not possible")
print(possible_designs)