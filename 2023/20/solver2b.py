from time import time

# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()

# Sanitise input file into modules: {name: [type, [inputs], [outputs]]}
modules = {}

for line in input:
    name = line.split(" -> ")[0][1:3]
    inputs = []
    type = line.split(" -> ")[0][0]
    outputs = list("".join(line.split(" -> ")[1].split(" ")).split(","))
    modules[name] = [type, inputs, outputs]

for module in modules:
    for output in modules[module][2]:
        if output != "rx":
            modules[output][1].append(module)

# Split modules into broadcaster, flipflops and conjunctions
bcr = []
ffs = {}
cons = {}

for module in modules.items():
    match module[1][0]:
        case "b": bcr = (module[1][2])
        case "%": ffs[module[0]] = [module[1][1], module[1][2]]
        case "&": cons[module[0]] = [module[1][1], module[1][2]]
        case _: print("Uh oh")

# Find major conjunctions at end of flipflop chains and preload flipflop chains
major_cons = {}
for ff in ffs:
    inputs = ffs[ff][0]
    if "ro" in inputs:
        for input in inputs:
            if input != "ro": major_cons[input] = {"chain": [ff]}

# Remove "tapped conjunctions" from flipflop outputs
for ff in ffs:
    outputs = ffs[ff][1]
    if len(outputs) == 2:
        for op in outputs:
            if op in major_cons:
                ffs[ff][1].remove(op)

# Fill out flipflop chains
for mc in major_cons:
    go = True
    while go:
        next_ff = ffs[major_cons[mc]["chain"][-1]][1][0]
        if next_ff in major_cons: go = False
        else: major_cons[mc]["chain"].append(next_ff)

# Find major conjunctions input and output indexes of ff chains
for mc in major_cons:
    output_indexes = []
    for output in cons[mc][0]:
        output_indexes.append(major_cons[mc]["chain"].index(output))
    output_indexes.sort()
    check = 0b0
    for i in output_indexes:
        check += 2**i
    major_cons[mc]["check"] = check

    input_indexes = []
    for input in cons[mc][1]:
        try: input_indexes.append(major_cons[mc]["chain"].index(input))
        except: pass
    input_indexes.sort()
    reset = 0b0
    for i in input_indexes:
        reset += 2**i
    major_cons[mc]["reset"] = reset

# Establish flipflop counters:
for mc in major_cons:
    major_cons[mc]["counter"] = 0b0

for mc in major_cons.items(): print(*mc)

count = 0
tstart = time()
count_limit = 10000
go = True
while go and count < count_limit:
    count +=2
    qt = (count - 3797) % 3498
    dq = (count - 3881) % 3666
    nl = (count - 3823) % 3550
    vt = (count - 4003) % 3910

    check = qt + dq + nl + vt

    if check == 0:
        print(f"Finished at {count}")

t = time() - tstart
print(f"Test 1 complete in {t}")

# ???
count = 0
tstart = time()
go = True
while go and count < count_limit:
    count += 1
    chains_active = 0
    for chain in major_cons:
        major_cons[chain]["counter"] += 1
        if major_cons[chain]["counter"] == major_cons[chain]["check"]:
            major_cons[chain]["counter"] = major_cons[chain]["reset"]
            print(f"{chain} reset at press {count}")
            chains_active += 1
    # if chains_active > 1:
    #     print(f"At press {count}, chains active: {chains_active}")
    if chains_active == 4:
        print(f"Holy shit! Stop the clock and {count}")
        go = False

t = time() - tstart
print(f"Test 2 complete in {t}")

print(3797*3881*3823*4003)
