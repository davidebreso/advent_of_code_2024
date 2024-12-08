def antinodes(antennas, width, height):
    if len(antennas) <= 1:
        return set()
    nodes = set()
    (x1, y1) = antennas.pop()
    for (x2, y2) in antennas:
        if 0 <= (2*x1 - x2) < width:
            if 0 <= (2*y1 - y2) < height:
                nodes.add((2*x1 - x2, 2*y1 - y2))
        if 0 <= (2*x2 - x1) < width:
            if 0 <= (2*y2 - y1) < height:
                nodes.add((2*x2 - x1, 2*y2 - y1))
    nodes |= antinodes(antennas, width, height)
    return nodes

def resonant_antinodes(antennas, width, height):
    if len(antennas) <= 1:
        return set()
    nodes = set()
    (x1, y1) = antennas.pop()
    nodes.add((x1, y1))
    for (x2, y2) in antennas:
        nodes.add((x2, y2))
        for i in range(1, min(width, height)):
            x3 = (i+1)*x1 - i*x2
            y3 = (i+1)*y1 - i*y2            
            if (0 <= x3 < width) and (0 <= y3 < height):
                nodes.add((x3, y3))
            x3 = (i+1)*x2 - i*x1
            y3 = (i+1)*y2 - i*y1            
            if (0 <= x3 < width) and (0 <= y3 < height):
                nodes.add((x3, y3))
    nodes |= resonant_antinodes(antennas, width, height)
    return nodes

infile = open("input.txt")

height = 0
width = 0
freqs = dict()
for line in infile:
    line = line.strip()
    width = max(width, len(line))
    for x in range(len(line)):
        c = line[x]
        if c != '.':
            freqs[c] = freqs.get(c, set()).union({(x, height)})
    height += 1

nodes = set()
for f in freqs:
    nodes |= resonant_antinodes(freqs[f], width, height)

print(len(nodes))    