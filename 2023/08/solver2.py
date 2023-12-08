# Problem scope
'''

Maps: left/rigth: network nodes
make camel follow instructions
get from AAA to ZZZ
This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Dir: RL
Strat at AAA
At AAA, R = CCC
At CCC, L = ZZZ
Fin in 2 steps

If no ZZZ, repeat dir. ie RLRLRL e.g:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
'''

# Solution sketch
'''
get dir
read letter
keep track of node: XXX
lookup node with dir and return new node
repeat
'''

# Functions


# Variables


# Main code
import timeit

# create one big dictionary of node to LR next steps
# network[ABC] -> ('DEF','GHI')
with open("puzzle_input.txt") as file:
    input = file.read().split("\n\n")
    dir = input[0]
    raw_network = input[1].splitlines()
    network = {}
    for line in raw_network:
        network[line.split(" = (")[0]] = [line.split(" = (")[1].split(", ")[0], line.split(" = ")[1].split(", ")[1][:-1:]]

# create nested dictionary of node to LR next steps nested by char in node
# network[A][B][C] -> ('DEF','GHI')
# with open("puzzle_input.txt") as file:
#     input = file.read().split("\n\n")
#     dir = input[0]
#     raw_network = input[1].splitlines()
#     nested_network = {}
#     # count = 0
#     for line in raw_network:
#         input_pos = line.split(" = (")[0]
#         d1 = input_pos[0]
#         d2 = input_pos[1]
#         d3 = input_pos[2]
#         # print(d1,d2,d3, count)
#         output_pos = [line.split(" = (")[1].split(", ")[0], line.split(" = ")[1].split(", ")[1][:-1:]]
#         if d1 in nested_network.keys():
#             if d2 in nested_network[d1].keys():
#                 nested_network[d1][d2][d3] = output_pos
#             else:
#                 nested_network[d1][d2] = {d3: output_pos}
#         else: nested_network[d1] = {d2: {d3: output_pos}}
        # count+=1
# print(nested_network.items())
# pos = "AAA"
# for keys in nested_network.keys():
#     print(nested_network[keys].keys(), len(nested_network[keys]))

# #compare access speeds of dictionaries: network and nested_network
# lookup = "SJJ"
# result = network[lookup]
# result_n = nested_network[lookup[0]][lookup[1]][lookup[2]]
# print(timeit.timeit("network[lookup]", globals=globals())) # 0.05
# print(timeit.timeit("nested_network[lookup[0]][lookup[1]][lookup[2]]", globals=globals())) # 0.13
# nested dictionary is approximately 2.6x slower than normal dict!

# def move_node(d, p):
#     match d:
#         case "R": return [network[x][1] for x in p]
#         case "L": return [network[x][0] for x in p]

# def nav_network(pos, steps):
#     temp_pos = pos
#     temp_steps = steps
#     for char in dir:
#         temp_pos = move_node(char, temp_pos)
#         temp_steps += 1
#     return(temp_pos, temp_steps)

def map_network_loop(pos):
    temp_pos = pos
    for d in dir:
        match d:
            case "R": temp_pos = network[temp_pos][1]
            case "L": temp_pos = network[temp_pos][0]
    return(temp_pos)

for key in network.keys():
    network[key].append(map_network_loop(key))
# for key in network.keys():
#     network[key].append(map_network_loop(key))

for key, value in network.items():
    print(key,"->",value)
    # print(value[1]==value[2])

def step_network(pos):
    temp_pos = pos
    new_steps = 0
    for d in dir:
        match d:
            case "R": temp_pos = network[temp_pos][1]
            case "L": temp_pos = network[temp_pos][0]
        new_steps += 1
        if temp_pos[2] == "Z" : return(temp_pos, new_steps)
    return(temp_pos, new_steps)

def step_network_vec(pos_vec):
    temp_pos = pos_vec
    new_steps = 0
    for d in dir:
        match d:
            case "R": temp_pos = [network[x][1] for x in temp_pos]
            case "L": temp_pos = [network[x][0] for x in temp_pos]
        new_steps += 1
        if temp_pos == end: return(temp_pos, new_steps)
    return(temp_pos, new_steps)

def loop_network(pos):
    return network[pos][3]

def loop_network_vec(pos_vec):
    return [network[x][3] for x in pos_vec]

def find_start_vector():
    start_vector = [k for k, v in network.items() if k[2] == "A"]
    return(start_vector)

# def find_end_vector():
#     end_vector = [k for k, v in network.items() if k[2] == "Z"]
#     return(end_vector)

# run individually on one start node until ABC = xxZ
# catch up on second start node to see if DEF = xxZ
# if not, resume running one node progress until next xxZ and repeat
# this only works faster if catch up is faster so:
# pre-calculate the mapping from all start nodes, to all end nodes for every cycle of direction path and append to network lookup
# keep track of dir_loop_count globally and dir_count within direction loop
# steps = dir_loop_count * loop_length + dir_count
# for catch up, skip through loop mapping for dir_loop_count, then scan in dir loop normally.



def main():
    pos = find_start_vector()
    not_at_end = True
    steps = 0
    while not_at_end:
        temp_pos = pos
        # pos_steps = ghost_network(temp_pos, steps, end)
        for d in dir:
            match d:
                case "R": temp_pos = [network[x][1] for x in temp_pos]
                case "L": temp_pos = [network[x][0] for x in temp_pos]
            steps += 1
            # print(temp_pos, steps)
            # if steps == 10: break
            if temp_pos[0][2] == "Z":
                if temp_pos[1][2] == "Z":
                    # print("Found 2 Z! at step", steps)
                    if temp_pos[2][2] == "Z":
                        print("Found 3 Z! at step", steps)
                        if temp_pos[3][2] == "Z":
                            print("Found 4 Z! at step", steps)
                            if temp_pos[4][2] == "Z":
                                print("Found 5 Z! at step", steps)
                                if temp_pos[4][2] == "Z":
                                    print("Found 6 Z! at step", steps)
                                    not_at_end = False
            else:
                continue
        pos = temp_pos
        # if steps == 10: break
    print("Steps:", steps)
# main()

# pos = find_start_vector()
# end = (find_end_vector())
# end_test = []
# for x in pos:
#     end_test.append("A")
#     # end.append("Z")

# temp_pos = sorted(["SJJ", "AAA", "ZZZ", "RNF", "GBR", "CCF"])
# temp_pos2 = ['HTZ', 'LLZ', 'TMZ', 'XDZ', 'XGZ', 'ZZZ']
# print(end)

# # check for end condition version 1: (sum of two ops)
# print(timeit.timeit("[x[2] for x in temp_pos]", number = 1000000, globals=globals())) # 0.39
# print(timeit.timeit("if temp_pos == end_test: 1", number = 1000000, globals=globals())) # 0.05
# print(timeit.timeit("if temp_pos == end: 1", number = 1000000, globals=globals())) # 0.05
# print(timeit.timeit("if temp_pos == sorted(end): 1", number = 1000000, globals=globals())) # 0.285
# print(timeit.timeit("if temp_pos2 == end: 1", number = 1000000, globals=globals())) # 0.12 for exact match
# print(".")
# # check for end condition version2: ()
# print(timeit.timeit("if temp_pos[0][2] == 'Z': 1", number = 1000000, globals=globals())) # 0.065
# print(timeit.timeit("if temp_pos[0][2] != 'Z': 1", number = 1000000, globals=globals())) # 0.065

# print(timeit.timeit("nested_network[lookup[0]][lookup[1]][lookup[2]]", globals=globals())) # 0.13
