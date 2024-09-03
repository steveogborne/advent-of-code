# Problem scope
'''
Step countingGardener starts at S in grid
Grid has rocks # and garden plots .
Gardner can walk to any adjacent garden plot with one step.
How many plots can gardener walk to in exactly 64 steps

Part two:
Steps are actually hugely larger (what a surprise!)
The map repeats infinitely
'''

# Solution sketch
'''
Create a set of cells for "current location after x steps"
For all cells in current set, find and evaluate neighbours.
Add valid neighbours to next step set if they don't already exist
Keep going until step count reached then count valid cells

Part 2:
Can reuse code if I can handle infinite grids. Modulo on map lookup for validity.
Set use will keep on top of not repeating cells
Can see how slow this is...

For optimisation:
Most cells will cycle on off. It's only the frontier that will add new cells.
Once a map cell "fills up" it will cycle between two different states which can just be calculated by knowing if step count is even or odd.
Presumably you could calculate how many steps before a cell is filled up.
Keeping track of
'''
# Variables
with open("test_input.txt") as file:
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
    if data[(r-1) % height][c % width] != "#": neighbours.append((r-1, c))
    # East
    if data[r % height][(c+1) % width] != "#": neighbours.append((r, c+1))
    # South
    if data[(r+1) % height][c % width] != "#": neighbours.append((r+1, c))
    # West
    if data[r % height][(c-1) % width] != "#": neighbours.append((r, c-1))
    return neighbours

# Main code
def main():
    desired_steps = 1000
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

    # for position in current_positions:
    #     print(position)

    answer = positions
    print("The solution is:",answer)

main()
