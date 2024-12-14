import re
import sys

def fastest_sp(xa, ya, xb, yb, xp, yp):
    nb = (xa * yp - ya * xp)
    db = (xa * yb - xb * ya)
    (b, q) = divmod(nb, db)
    if q != 0:
        return 0
    na = (xb * yp - yb * xp)
    da = (xb * ya - xa * yb)
    (a, q) = divmod(na, da)
    if q != 0:
        return 0
    return 3*a + b

infile = open(sys.argv[1])

tokens = 0
while row := infile.readline():
    xa, ya = (int(s) for s in re.split("\+|=|,| |\t|\n", row) if s.isdigit() )
    row = infile.readline()
    xb, yb = (int(s) for s in re.split("\+|=|,| |\t|\n", row) if s.isdigit() )
    row = infile.readline()
    xp, yp = (int(s) for s in re.split("\+|=|,| |\t|\n", row) if s.isdigit() )
    ofs = 10000000000000
    tokens += fastest_sp(xa, ya, xb, yb, xp + ofs, yp + ofs)
    row = infile.readline()
print(tokens)