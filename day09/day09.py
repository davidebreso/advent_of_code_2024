from collections import deque

def unpack_map(densemap):
    res = []
    for i in range(len(densemap) // 2):
        res.append((i, densemap[2*i]))
        res.append(('.', densemap[2*i + 1]))
    res.append((len(densemap) // 2, densemap[-1]))
    return res
    
def compact_map(map):
    i = 0
    j = len(map) - 1
    while i < j:
        fid, fsize = map[i]
        lid, lsize = map[j]
        if fid != '.':
            i += 1
        elif lid == '.':
            j -= 1
        elif fsize < lsize:
            map[i] = (lid, fsize)
            map[j] = (lid, lsize - fsize)
            i += 1
        elif fsize == lsize:
            del map[j]
            map[i] = (lid, fsize)
            i += 1
            j -= 1
        else:
            del map[j] 
            map[i] = (lid, lsize)
            i += 1
            map.insert(i, (fid, fsize - lsize))
            
def checksum(map):
    sum = 0
    i = 0
    for (a, n) in map:
        if a != '.':
            sum += a * (n * i + n * (n - 1) // 2)
        i += n
    return sum

def defrag_map(map):
    j = len(map) - 1
    while j > 0:
        lid, lsize = map[j]
        if lid == '.':
            j -= 1
            continue
        for i in range(j):
            fid, fsize = map[i]
            if fid == '.' and fsize >= lsize:
                map[j] = ('.', lsize)
                map[i] = (lid, lsize)
                if fsize > lsize:
                    map.insert(i + 1, (fid, fsize - lsize))
                    j += 1
                break
        j -= 1

# text = "12345"
# text = "2333133121414131402"
infile = open("input.txt")
text = infile.read().strip()
densemap = [int(c) for c in text]
map = unpack_map(densemap)
compact_map(map)
print(checksum(map))
map = unpack_map(densemap)
defrag_map(map)
print(checksum(map))



