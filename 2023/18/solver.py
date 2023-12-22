# Problem scope
'''
Digging a lagoon
Each line in puzzle input is a dig instruction with direction, distance and side wall colour
Create a map of the dig site. "." is level ground. "#" is a dug hole
Start with the outline as specified by the dig instructions
Fill in the outline with dug holes
Count the dug holes
'''

# Solution sketch
'''
Use the directions and distances to calculate canvas size
Create canvas
Output to file
Trace outline by following instructions
Fill inside using fill algorithm from chasing metal squirrels or something else
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()

# Functions



# Main code
def main():
    answer = "Undefined"
    print("The solution is:",answer)

main()
