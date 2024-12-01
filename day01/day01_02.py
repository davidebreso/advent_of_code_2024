infile = open("input1.txt")
left = []
right = []
for row in infile:
    (a, b) = row.split()
    left.append(int(a))
    right.append(int(b))
# create dictionary with frequencies for right list
freq = dict()
for n in right:
    freq[n] = freq.get(n, 0) + 1
# compute similarity score
score = 0
for n in left:
    score += n * freq.get(n, 0)
print(score)
