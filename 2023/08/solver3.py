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
prescan a loop for final node and store this node in the network map
prescan a loop for presence of finish nodes and store their indexes in the network map
now for every loop, we don't need to scan the nodes, we know where the final nodes will be met.
for multiple ghosts, they both find a final node at the same time if they share a final node index within this loop
store a list of ghost nodes
for the next loop, look up the final node indexes that each ghost will meet and store as lists
a union of these lists of final node indexes will tell us how many ghotss meet in this loop
if not 6 then progress to the next loop using the loop end node short cut
if this is slow then precompute a final node index list and next node reference for n loops
'''


import timeit
#### SETUP ####
# globals
direction_list = []
loop_l = len(direction_list)
network = {}

# Fill dictionary "network" with node to LR next steps
# network[ABC] -> ('DEF','GHI')
with open("puzzle_input.txt") as file:
    input = file.read().split("\n\n")
    direction_list = input[0]
    raw_network = input[1].splitlines()
    for line in raw_network:
        network[line.split(" = (")[0]] = [line.split(" = (")[1].split(", ")[0], line.split(" = ")[1].split(", ")[1][:-1:]]

# Add to this dictionary's values a third node reference which is the node you reach at the end of one loop of directions
# So now network[ABC] -> ('DEF','GHI','XYZ')
def map_network_loop(start_node):
    temp_node = start_node
    for d in direction_list:
        match d:
            case "R": temp_node = network[temp_node][1]
            case "L": temp_node = network[temp_node][0]
    return(temp_node)
for key in network.keys():
    network[key].append(map_network_loop(key))
# for key, value in network.items():
#     print(key,"->",value)

# look up xxA nodes to find start positions of ghosts. ['STA', 'AAA', 'GPA', 'LKA', 'DFA', 'KKA'] ftr
def initialise_ghosts():
    start_vector = [key for key in network.keys() if key[2] == "A"]
    ghosts_init = {}
    for x in range(len(start_vector)):
        ghosts_init[x] = [start_vector[x], 0, 0] # ghost[x] -> [start_node, 0 loops, 0 steps]
    return(ghosts_init)

#### CALCULATOR ####

# function to step one ghost through the network, one direction step at a time.
# Returns if a xxZ node is found with incremented step and loop counter since initiation.
def step_network(start_node, start_step):
    this_node = start_node
    this_step = start_step
    new_loops = 0
    # print("ghost exploring...")
    while True:
        match direction_list[this_step]:
            case "L": this_node = network[this_node][0]
            case "R": this_node = network[this_node][1]
        this_step += 1 ######################################## CHECK for +/-1 error
        if this_step == len(direction_list):
            new_loops += 1
            this_step = 0
        if this_node[2] == "Z" :
            # print("Z found")
            return(this_node, this_step, new_loops)

# function to step one ghost within one loop from start step to end step. DOES NOT SUPPORT end step < start step
def loop_to_point(start_node, start_step, end_step):
    this_node = start_node
    this_step = start_step
    while this_step <= end_step:
        match direction_list[this_step]:
            case "L": this_node = network[this_node][0]
            case "R": this_node = network[this_node][1]
        this_step += 1 ######################################## CHECK for +/-1 error
    return(this_node)

#function to quickly take one ghost from one node: step position to target step position
def catchup(step_target, loop_target, this_ghost_node, this_ghost_loop, this_ghost_step):
    # print("ghost preparing to catch up...")
    loops_to_catch_up = loop_target - this_ghost_loop
    # finish any incomplete loops
    if this_ghost_step > 0:
        while this_ghost_step <= loop_l:
            match direction_list[this_ghost_step]:
                case "L": this_ghost_node = network[this_ghost_node][0]
                case "R": this_ghost_node = network[this_ghost_node][1]
            this_ghost_step += 1
        this_ghost_step = 0
        loops_to_catch_up -= 1
    # print("incomplete loop finshed")
    # race through loops to catch up
    # print("ghost needs to catch up ", loops_to_catch_up, "loops")
    while loops_to_catch_up > 0:
        this_ghost_node = network[this_ghost_node][2]
        loops_to_catch_up -= 1
    # print("ghost has complete looping with", loops_to_catch_up, "loops left")
    # catch up last partial loop
    # print("starting at step", this_ghost_step, "we want to reach", step_target)
    while this_ghost_step < step_target:
        match direction_list[this_ghost_step]:
            case "L": this_ghost_node = network[this_ghost_node][0]
            case "R": this_ghost_node = network[this_ghost_node][1]
    # print("final steps caught up")
    this_ghost_node = loop_to_point(this_ghost_node, 0, step_target)
    # print("ghost has caught up")
    return(this_ghost_node)

### STATE MACHINE:
# n = number of ghosts at potential finish positions. At n=6 all ghosts are at finish
# While n<6:
# If n= 0: lead ghost: ghost0 is exploring - call step network with ghost0. When z is found n = 1
# If n>0: ghost n+1 is catching up, where n = number of ghosts at lead ghost position
#          call catchup on ghost n,
#           call compare ghosts up to n
#           if all z = n+1,
#           else n=0
# Excape means n = 6 and final steps = loops * loop length + steps for any ghost

def main():
    ghosts = initialise_ghosts()
    # send first ghost ahead, one step at a time, updating
    ghost_state = 0 # state machine. n=6 is the finish
    # initialise lead ghost values
    #ghost0_n = ghosts[0][0] # node
    #ghost0_l = ghosts[0][1] # loops
    #ghost0_s = ghosts[0][2] # steps (within loop, not global)
    # state machine
    while ghost_state < 6:
        if ghost_state == 0:
            # lead ghost explores until a "Z" is found then returns and updates it's location
            ghosts[0][0], ghosts[0][2], new_loops = step_network(ghosts[0][0], ghosts[0][2])
            ghosts[0][1] += new_loops
            ghost_state += 1
            if ghosts[0][1]%10000 == 0: print("another 10000 loops searched")
        # next ghost catches up
        if ghost_state > 0:
            # print("ghost", ghost_state, "catching up")
            ghosts[ghost_state][0] = catchup(ghosts[0][2],
                                             ghosts[0][1],
                                             ghosts[ghost_state][0],
                                             ghosts[ghost_state][1],
                                             ghosts[ghost_state][2])
            ghosts[ghost_state][1] = ghosts[0][1]
            ghosts[ghost_state][2] = ghosts[0][2]
            if ghost_state ==2:
                print("Two ghosts met at", ghosts[0][0], "and", ghosts[ghost_state][0])

            # lead ghost and ghost to catch up compare finish values
            if ghosts[0][0][2] == ghosts[ghost_state][0][2]: # it's a match, catch the next ghost up to check again
                print("another ghost found a matching finish node")
                ghost_state += 1
            else:
                ghost_state = 0 # it's not a match send the lead ghost to search again
                # print("better get back to searching")

    #if we get here n = 6
    final_steps = loop_l*ghosts[0][1] + ghosts[0][2]
    print(ghost_state, "ghosts are in the same place")
    print("at location: ", [ghosts[key][0] for key in ghosts])
    print("after", final_steps, "fucking steps")

main()

# function to step a vector of ghosts through the network, one direction at a time.
# Returns at the end of the loop or if a xxZ node is found.
# Don't know if I need this
# def step_network_vec(pos_vec, step):
#     temp_pos = pos_vec
#     new_steps = step
#     for d in dir:
#         match d:
#             case "R": temp_pos = [network[x][1] for x in temp_pos]
#             case "L": temp_pos = [network[x][0] for x in temp_pos]
#         new_steps += 1
#         if temp_pos == 0: return(temp_pos, new_steps) ################################# UPDATE ME
#     return(temp_pos, new_steps)

# function to fastforward a vector of ghosts through a loop if we know it doesn't need to stop
# Don't know if I need this
# def loop_network_vec(pos_vec):
#     return [network[x][3] for x in pos_vec]

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

# def old_main():
#     pos = find_start_vector()
#     not_at_end = True
#     steps = 0
#     while not_at_end:
#         temp_pos = pos
#         # pos_steps = ghost_network(temp_pos, steps, end)
#         for d in direction_list:
#             match d:
#                 case "R": temp_pos = [network[x][1] for x in temp_pos]
#                 case "L": temp_pos = [network[x][0] for x in temp_pos]
#             steps += 1
#             # print(temp_pos, steps)
#             # if steps == 10: break
#             if temp_pos[0][2] == "Z":
#                 if temp_pos[1][2] == "Z":
#                     # print("Found 2 Z! at step", steps)
#                     if temp_pos[2][2] == "Z":
#                         print("Found 3 Z! at step", steps)
#                         if temp_pos[3][2] == "Z":
#                             print("Found 4 Z! at step", steps)
#                             if temp_pos[4][2] == "Z":
#                                 print("Found 5 Z! at step", steps)
#                                 if temp_pos[4][2] == "Z":
#                                     print("Found 6 Z! at step", steps)
#                                     not_at_end = False
#             else:
#                 continue
#         pos = temp_pos
#         # if steps == 10: break
#     print("Steps:", steps)
# old_main()

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
