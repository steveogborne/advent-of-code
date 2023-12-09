# Desert ghost network navigator

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

#### SETUP ####
import time
# globals
direction_list = []
loop_l = 0
network = {}

# Fill dictionary "network" with node to LR next steps
# network[ABC] -> ('DEF','GHI')
with open("puzzle_input.txt") as file:
    input = file.read().split("\n\n")
    direction_list = input[0]
    loop_l = len(direction_list)
    raw_network = input[1].splitlines()
    for line in raw_network:
        network[line.split(" = (")[0]] = [line.split(" = (")[1].split(", ")[0], line.split(" = ")[1].split(", ")[1][:-1:]]

# print("Loop length =", loop_l)

# Create a function that traverses the list of directions to find the end-of-loop node location for a given start node
def map_network_loop(start_node):
    temp_node = start_node
    indexes = []
    for count, d in enumerate(direction_list):
        start = temp_node
        if temp_node[2] == "Z":
            indexes.append(count)
            # print("Z found at", start)
        match d:
            case "R": temp_node = network[temp_node][1]
            case "L": temp_node = network[temp_node][0]
        # print(start, "moves", d, "to", temp_node)
    return(temp_node, indexes)

# Iterate over the netowrk map and add a third node reference which is the node you reach at the end of one loop of directions
for key in network.keys():
    new_loop_node, z_index_list = map_network_loop(key)
    network[key].append(new_loop_node)
    network[key].append(z_index_list)
# So now network[ABC] -> ('DEF','GHI','XYZ')

# for key, value in network.items(): # test
#     print(key,"->",value)          # test

# key_list = network.keys()
# for key, value in network.items():
#     if value[3]: print(key, ":", value)

# DISCOVERY! The only times we find "xxZ" in a loop is at the beginning! It never appears half way through a loop!
# Therefore just iterate the search over loops only!

# Output:
# Z found at HTZ
# Z found at ZZZ
# Z found at XDZ
# Z found at LLZ
# Z found at XGZ
# Z found at TMZ
# HTZ : ['DXG', 'XTB', 'XFX', [0]]
# ZZZ : ['XCG', 'MCS', 'CRR', [0]]
# XDZ : ['LHB', 'FLJ', 'FSN', [0]]
# LLZ : ['RRK', 'GLG', 'GVP', [0]]
# XGZ : ['CNF', 'BVF', 'QHQ', [0]]
# TMZ : ['RTR', 'FML', 'TPN', [0]]

# look up xxA nodes to find start positions of ghosts. ['STA', 'AAA', 'GPA', 'LKA', 'DFA', 'KKA'] ftr
def initialise_ghosts():
    ghosts_list = [[key, 0] for key in network.keys() if key[2] == "A"]
    return(ghosts_list)

# Alternative main program. OKOKOK new theory. Loops for ONE ghost(n) to reach an end node = Ln.
# Loops for ALL ghosts to line up is lowest common multiple of all Ln.
def new_main():
    start = time.time()
    ghosts_list = initialise_ghosts()
    not_at_end = True
    steps = 0
    loop_length = loop_l

    # count number of loops to reach a final node for each ghost
    for index, ghost in enumerate(ghosts_list):
        loop_counter = 0
        ghost_node = ghost[0]
        while ghost_node[2] != "Z":
            ghost_node = network[ghost_node][2]
            loop_counter += 1
        ghosts_list[index][1] = loop_counter

    # Calculate lowest common multiple of all ghost loop counts:
    LCM = 1
    for ghost in ghosts_list:
        LCM *= ghost[1]

    steps = LCM*loop_l

    #     # timer
    #     if steps%(loop_length*10000000) == 0:
    #         time_now = time.time()
    #         print(f'{steps:,}', "steps down after", time_now-start, "seconds")
    print("Steps:", steps)
    return(ghosts_list)

# Run it, time it
start = time.time()
print(new_main())
end = time.time()
print(end - start)


# Main program stakes a starting list of ghost locations and moves them simoultaneously forward one loop at a time.
# Each loop it checks if the ghosts are all at finishing nodes. If yes, end the loop and return step count. If no, continue searching
# def main():
#     start = time.time()
#     ghosts_list = initialise_ghosts()
#     not_at_end = True
#     steps = 0
#     loop_length = loop_l
#     while not_at_end:
#         # update location of all ghosts 1 loop and step count
#         for index, ghost in enumerate(ghosts_list):
#             ghosts_list[index] = network[ghost][2]
#         steps += loop_length

#         # check if any ghosts are not at a final node
#         for ghost in ghosts_list:
#             if ghost[2] != "Z":
#                 break
#             not_at_end = False

#         # timer
#         if steps%(loop_length*10000000) == 0:
#             time_now = time.time()
#             print(f'{steps:,}', "steps down after", time_now-start, "seconds")
#     print("Steps:", steps)
#     return(ghosts_list, steps)

# # Run it, time it
# start = time.time()
# print(main())
# end = time.time()
# print(end - start)
# # 1,000,000 loops = 1 second... ~1 hour for 1,000,000,000,000 steps
