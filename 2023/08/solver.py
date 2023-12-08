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
with open("puzzle_input.txt") as file:
    input = file.read().split("\n\n")
    dir = input[0]
    raw_network = input[1].splitlines()
    network = {"node":[],"left":[],"right":[]}
    for line in raw_network:
        network["node"].append(line.split(" = (")[0])
        network["left"].append(line.split(" = (")[1].split(", ")[0])
        network["right"].append(line.split(" = ")[1].split(", ")[1][:-1:])

# pos = "AAA"

def move_node(d, p):
    index = network["node"].index(p)
    match d:
        case "R": return network["right"][index]
        case "L": return network["left"][index]

    return 0

def nav_network(pos, steps):
    temp_pos = pos
    temp_steps = steps
    for char in dir:
        temp_pos = move_node(char, temp_pos)
        temp_steps += 1
    return(temp_pos, temp_steps)

def main():
    pos = "AAA"
    steps = 0
    while pos != "ZZZ":
        temp_pos = pos
        pos = nav_network(temp_pos, steps)[0]
        steps = nav_network(temp_pos, steps)[1]
        print(pos)
    print("Steps:", steps)
main()
