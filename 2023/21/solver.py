# Problem scope
'''
Step countingGardener starts at S in grid
Grid has rocks # and garden plots .
Gardner can walk to any adjacent garden plot with one step.
How many plots can gardener walk to in exactly 64 steps
'''

# Solution sketch
'''
Create a set of cells for "current location after x steps"
For all cells in current set, find and evaluate neighbours.
Add valid neighbours to next step set if they don't already exist
Keep going until step count reached then count valid cells
'''
# Variables
with open("puzzle_input.txt") as file:
    data = file.read().splitlines()

width = len(data[0])
height = len(data)

# Find start location
for r, line in enumerate(data):
    for c, char in enumerate(line):
        if char == "S":
            start = (r, c)



Location = tuple[int, int]

# Functions
def getValidNeighbours(location) -> set[Location]:
    (r, c) = location
    neighbours = []
    # North
    if r > 0 and data[r-1][c] != "#": neighbours.append((r-1, c))
    # East
    if c < width-1 and data[r][c+1] != "#": neighbours.append((r, c+1))
    # South
    if r < height-1 and data[r+1][c] != "#": neighbours.append((r+1, c))
    # West
    if c > 0 and data[r][c-1] != "#": neighbours.append((r, c-1))
    return neighbours

# Main code
def main():
    desired_steps = 64
    steps = 0
    # Initialise set of current positions
    current_positions = {start}
    next_positions = set(())
    while steps < desired_steps:
        for cell in current_positions:
            next_positions.update(getValidNeighbours(cell))
        current_positions.clear()
        current_positions.update(next_positions)
        next_positions.clear()
        steps +=1
    positions = len(current_positions)

    answer = positions
    print("The solution is:",answer)

main()
