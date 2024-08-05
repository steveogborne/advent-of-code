# Problem scope
'''
Parts need sorting
Parts have 4 ratings: x,m,a,s. A list of parts to sort is the second half of puzzle input
Parts get sorted through workflows. A list of workflows is the first half of puzzle input
Workflows have rules corresponding to the part ratings and either:
> send the part to another workflow, accept or reject the part.
All parts that are accepted are given a rating which is the sum of their individual ratings
The answer is the sum of all the total ratings of all accpeted parts

Part 2:
Each of the four ratings can have a value 1<=v<=4000
How many distinct combinations of ratings will be accepted by the workflows?
'''

# Solution sketch
'''
Part 2:
No longer need parts list.
Solution is a tree of nodes. At each conditional, the tree splits.
The branches are either a new function or A or R.
Note: X,m,a,s values can have mulitple ranges (is this true? not sure, each clause cuts range in two mutually excl. ranges and tree has no loops)
We want to find all combinations that reach an A terminus

Setup:
Process input file to make workflows parsable for this new solution
Setup a queue to traverse the tree
Write a function that:
    Takes a node workflow and part range input
    Establishes the output ranges that either
        Get accepted or
        Passed to a new workflow (node)
Create a dataclass that stores the part ranges (min, max for x, m, a, s)

Solve
Start at the base of the tree ("in"):
Process the node
Add the accepted range to the accepted ranges (or calculate the range product as we go?)
Add the children to the queue

Create a dictionary with keys as the line code and values as
'''

# Globals
with open("puzzle_input.txt") as file:
    input = file.read().split("\n\n")
    workflow_list = input[0].splitlines()

# Turn the input into something more useful:
node_clauses = {}
for line in workflow_list:
    name = line.split("{")[0]
    clauses = line[:-1].split("{")[1].split(",")
    node_clauses[name] = clauses

xmas_0 = {"x": {"min": 1, "max": 4000},
           "m": {"min": 1, "max": 4000},
           "a": {"min": 1, "max": 4000},
           "s": {"min": 1, "max": 4000}}

# Functions
def get_new_ranges(xmas_in: dict, conditional: str) -> dict:
    param = conditional[0]          # x, m, a or s
    ineq = conditional[1]           # < or >
    value = int(conditional[2:])    # node name eg. xx or abc
    valid_range = xmas_in.copy()
    invalid_range = xmas_in.copy()
    match ineq:
        case "<":
            if value < xmas_in[param]["min"]:
                valid_range[param]["min"] = 0
                valid_range[param]["max"] = 0
            else:
                new_valid_max = min(value - 1, xmas_in[param]["max"])
                valid_range[param]["max"] = new_valid_max
                invalid_range[param]["min"] = new_valid_max + 1
        case ">":
            if value > xmas_in[param]["max"]:
                valid_range[param]["min"] = 0
                valid_range[param]["max"] = 0
            else:
                new_valid_min = max(value + 1, xmas_in[param]["min"])
                valid_range[param]["min"] = new_valid_min
                invalid_range[param]["max"] = new_valid_min - 1
    return valid_range, invalid_range

def get_range_product(xmas: dict) -> int:
    product = 1
    for range in xmas.values():
        product *= range["max"] - range["min"] + 1
    return product

def process_node(xmas_in: dict, clauses: list):
    # A function to take an input part xmas range, a workflow list of clauses
    # That updates the accepted ranges and adds child nodes with input part ranges to the queue
    working_range = xmas_in
    accepted = 0
    children = []
    for clause in clauses:
        split_clause = clause.split(":")
        if len(split_clause) == 2:
            conditional, target = split_clause
            valid_range, invalid_range = get_new_ranges(working_range, conditional)
            match target:
                case "A":
                    accepted += get_range_product(valid_range)
                case "R":
                    pass
                case _:
                    children.append((target, valid_range))
            working_range = invalid_range.copy()
        else:
            target = split_clause[0]
            match target:
                case "A":
                    accepted += get_range_product(working_range)
                case "R":
                    pass
                case _:
                    children.append((target, working_range))
    return accepted, children

def display_children(child):
    return f"{child[0]}: {child[1]['x']['min']}<x<{child[1]['x']['max']}, {child[1]['m']['min']}<m<{child[1]['m']['max']}, {child[1]['a']['min']}<a<{child[1]['a']['max']}, {child[1]['s']['min']}<s<{child[1]['s']['max']}"

# Two steps: 1)

# At node: if A: append combinations tracker with xmas
# If R: apply reverse clause to next term
# For each clause add clause_to_xmas(parent, clause) and clause_to_xmas(parent, opposite_clause(clause))

# Example line px{a<2006:qkq,m>2090:A,rfg}
# Turn into node: px: children = [qkq, rfg]

# Main code
def main():
    # Initialise tree queue with xmas_0
    queue = [("in", xmas_0)]
    # Tracker for accepted parts
    accepted_parts = 0
    nodes_processed = 0
    count_max = 1

    # While there are nodes in the queue left to process, process them
    # adding their accepted ranges to the list and new children to the queue
    while len(queue) > 0 and nodes_processed < count_max:
        nodes_processed += 1
        node_name, node_input = queue.pop(0)
        newly_accepted, new_children = process_node(node_input, node_clauses[node_name])
        accepted_parts += newly_accepted
        queue += new_children
        print(f"\"{node_name}\" accepted {newly_accepted} new parts and created:")
        for child in new_children:
            print(display_children(child))


    print(f"Processed {nodes_processed} nodes. The solution is: {accepted_parts}")

main()


# Create a tree which is a list of nodes.
# Each node stores a list of child nodes.
# We know it's not a cylic tree if the generate code terminates.

# For each node we can calculate the minimum and maximum parameter that reaches the node
# Need to stor 8 parameters and calculate them

# For every A we should be abale to add up all the ranges that reached there.
# Go through list of nodes:
# No A leaves? Delete
# A leaves? Add their range product to the total. Delete node
# When all nodes accounted for done.
