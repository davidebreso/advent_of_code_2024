import pynusmv
import sys
import math

def spec_to_bdd(model, spec):
    bddspec = pynusmv.mc.eval_ctl_spec(model, spec)
    return bddspec

def reachable(model, spec):
    bddspec = spec_to_bdd(model, spec)
    reach = model.init
    new = model.init
    steps = 0
    while new.isnot_false():
        conj = new & bddspec
        if conj.isnot_false(): 
            return steps
        new = model.post(new) - reach
        reach = reach | new
        steps += 1
    return math.inf

def build_trace(model, frontiers, last):
    # print(len(frontiers), "elements in frontier")
    # print("last state:", last.get_str_values())
    if not frontiers:
        return [last.get_str_values()]
    front = frontiers.pop()
    pred = model.pre(last)
    state = model.pick_one_state(front & pred)
    inputs = model.get_inputs_between_states(state, last)
    input = model.pick_one_inputs(inputs)
    trace = build_trace(model, frontiers, state)
    trace.append(input.get_str_values())
    trace.append(last.get_str_values())
    return trace

def explain_reachable(model, spec):
    bddspec = spec_to_bdd(model, spec)
    reach = model.init
    new = model.init
    frontiers = list()
    while new.isnot_false():
        conj = new & bddspec
        if conj.isnot_false():
            # print("Property reached, building trace")            
            last = model.pick_one_state(conj)
            trace = build_trace(model, frontiers, last)
            return (True, trace)
        frontiers.append(new)
        new = model.post(new) - reach
        reach = reach | new
    return (False, [])

def check_code(code, robotemplate):
    robot = robotemplate.replace('##E1##', code[0])
    robot = robot.replace('##E2##', code[1])
    robot = robot.replace('##E3##', code[2])
    
    pynusmv.init.reset_nusmv()  
    pynusmv.glob.load(robot)
    pynusmv.glob.compute_model()
    model = pynusmv.glob.prop_database().master.bddFsm
    invtype = pynusmv.prop.propTypes['Invariant']
    for prop in pynusmv.glob.prop_database():
        spec = pynusmv.prop.not_(prop.expr)
        if prop.type == invtype:
            res = reachable(model, spec)
            if res == math.inf:
                print("Impossible code", code)
            else:
                print("Code", code, "can be typed in", res, "steps")
        else:
            print("Property", spec, "is not an INVARSPEC, skipped.")
    return res * int(code[:-1])

pynusmv.init.init_nusmv()
robofile = open("robotemplate.smv")
robotemplate = robofile.read()
codefile = open(sys.argv[1])
complexity = 0
for code in codefile:
    complexity += check_code(code.strip(), robotemplate)
print("Sum of complexities:", complexity)

pynusmv.init.deinit_nusmv()
