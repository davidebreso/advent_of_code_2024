import sys

## Compute valuation of all variables given list of gates
def evaluate_circuit(gates, valuation):
    result = valuation.copy()
    change = True
    while change:
        change = False
        for out in gates:
            in1, op, in2 = gates[out]
            if out in result:
                continue
            if (in1 in result) and (in2 in result):
                change = True
                if op == 'AND':
                    result[out] = (result[in1] and result[in2])
                elif op == 'OR':
                    result[out] = (result[in1] or result[in2])
                elif op == 'XOR':
                    result[out] = (result[in1] != result[in2])
    return result

## Compute decimal value from list of variables
def bits_to_decimal(valuation):
    result = 0
    for var in sorted(valuation, reverse = True):
        result = (result << 1)
        if valuation[var]:
            result |= 1
    return result
    
## Compute list of variable from decimal value
def decimal_to_bits(number, bits, letter):
    valuation = dict()
    for digit in range(bits):
        number, val = divmod(number, 2)
        val = (val == 1)
        var = letter + "{:02d}".format(digit)
        valuation[var] = val
    return valuation

## Compute parent variables
def parent_variables(var, gates):
    in1, _, in2 = gates[var]
    parents = set({in1, in2})
    change = True
    while change:
        change = False
        for out in gates:
            in1, op, in2 = gates[out]
            if in1 in parents and in2 in parents:
                continue
            if out in parents:
                parents.add(in1)
                parents.add(in2)
                change = True
    return parents
    
## Compute expression for variable, given limited depth
def expression(var, gates, depth):
    if depth == 0:
        return var
    if var not in gates:
        return var
    in1, op, in2 = gates[var]
    exp1 = expression(in1, gates, depth - 1)
    exp2 = expression(in2, gates, depth - 1)
    return op+"("+exp1+", "+exp2+")"

## Rename internal variables to significant names
def find_bad_vars(gates, last_z):
    bad_vars = set()
    for out, (in1, op, in2) in gates.items():
        if op == 'XOR':
            if out == 'z00':
                if in1 != 'x00' or in2 != 'y00':
                    print("1. Bad expression:", out, "=", in1, op, in2)
                    bad_vars.add(out) 
            elif out[0] != 'z':
                if in1[0] != 'x' or in2[0] != 'y':
                    print("2. Bad expression:", out, "=", in1, op, in2)
                    bad_vars.add(out)
            elif in1[0] in ('x', 'y') or in2[0] in ('x', 'y'):
                print("3. Bad expression:", out, "=", in1, op, in2)
                bad_vars.add(out)
        elif op == 'AND':
            if out[0] == 'z':
                print("4. Bad expression:", out, "=", in1, op, in2)
                bad_vars.add(out)
            elif in1 != 'x00' and in2 != 'y00':
                for subout, (subin1, subop, subin2) in gates.items():
                    if subop != 'OR' and (subin1 == out or subin2 == out):
                        print("5. Bad expression:", out, "=", in1, op, in2)
                        bad_vars.add(out)
        else:   # op == 'OR'
            if in1[0] in ('x', 'y') or in2[0] in ('x', 'y'):
                print("6. Bad expression:", out, "=", in1, op, in2)
                bad_vars.add(out)
            elif out[0] == 'z' and out != last_z:
                print("7. Bad expression:", out, "=", in1, op, in2)
                bad_vars.add(out)
            subin1, subop, subin2 = gates[in1]
            if subop != 'AND':
                print("8. Bad expression:", in1, "=", subin1, subop, subin2)
                bad_vars.add(in1)
            subin1, subop, subin2 = gates[in2]
            if subop != 'AND':
                print("9. Bad expression:", in2, "=", subin1, subop, subin2)
                bad_vars.add(in2)
                                
    return bad_vars
        

cache = dict()

def find_swaps(gates, xyvals, zvals, bad_vars, depth):
    if depth == 0:
        return set()
    if (depth, frozenset(bad_vars)) in cache:
        return cache[depth, frozenset(bad_vars)]
    print((4-depth)*'+',"Checking", bad_vars)
    tail = bad_vars.copy()
    for var1 in bad_vars:
        tail.remove(var1)
        for var2 in tail:
            ## Swap the wires
            gate1 = gates[var1]
            gate2 = gates[var2]
            gates[var2] = gate1
            gates[var1] = gate2
            if depth == 1:
                valuation = evaluate_circuit(gates, xyvals)
                if sum(1 for var in zvals if zvals[var] != valuation.get(var, None)) == 0:
                    print("Found swap for", depth, bad_vars)
                    cache[depth, frozenset(bad_vars)] = { var1, var2 }
                    gates[var1] = gate1
                    gates[var2] = gate2
                    return { var1, var2 }
            else:   
                swaps = find_swaps(gates, xyvals, zvals, tail - {var2}, depth - 1)
                if len(swaps) > 0:
                    ## Swap found
                    print("Found swap for", depth, bad_vars)
                    cache[depth, frozenset(bad_vars)] = swaps | { var1, var2 }
                    gates[var1] = gate1
                    gates[var2] = gate2
                    return swaps | { var1, var2 }
            ## Undo swap and continue
            gates[var1] = gate1
            gates[var2] = gate2
    print((4-depth)*'+',"No solution found")
    print("Adding", depth, bad_vars)
    cache[depth, frozenset(bad_vars)] = set()
    return set()
    
## Open input file
infile = open(sys.argv[1])

## Read input values
xyvals = dict()
for line in infile:
    if len(line) <= 1:
        break
    var, value = line.strip().split(": ")
    value = (value == '1')
    xyvals[var] = value
# print(valuation)

xvars = { var: xyvals[var] for var in xyvals if var[0] == 'x' }
yvars = { var: xyvals[var] for var in xyvals if var[0] == 'y' }
xval = bits_to_decimal(xvars)
yval = bits_to_decimal(yvars)
zval = xval + yval
print(xval, "+", yval, '=', zval)

## Read gates
gates = dict()
for line in infile:
    in1, op, in2, _, out = line.strip().split()
    if in2 < in1:
        (in1, in2) = (in2, in1)
    gates[out] = (in1, op, in2)
# print(gates)

valuation = evaluate_circuit(gates, xyvals)

## Compute decimal output
outputs = { var: valuation[var] for var in valuation if var[0] == 'z' }
print("Final output is:", bits_to_decimal(outputs))
zvals = decimal_to_bits(zval, len(outputs), 'z')
bad_vars = find_bad_vars(gates, "z{:02d}".format(len(zvals) - 1))
print(",".join(sorted(bad_vars)))
