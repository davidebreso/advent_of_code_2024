import sys

cache = { "": 1 }

def design_match(design, towels):
    if design in cache:
        return cache[design]
    design_count = 0
    for towel in towels:
        if design.startswith(towel):
            design_count += design_match(design[len(towel):], towels)
    cache[design] = design_count
    return design_count

if len(sys.argv) == 2:
    infile = open(sys.argv[1])
else:
    infile = open("test1.txt")
    
towels = infile.readline().strip().split(", ")
infile.readline()

possible_designs = 0
for design in infile:
    design = design.strip()
    possible_designs += design_match(design, towels)
print(possible_designs)