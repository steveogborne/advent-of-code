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

class mapCell:
    def __init__(self, cur_pos = None, full = False) -> None:
        self.cur_pos = cur_pos if cur_pos is not None else set(())
        self.full = full

    def __str__(self) -> str:
        return f"{len(self.cur_pos)} positions"

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

def totalCount(map: dict):
    count = 0
    for cell in map.values():
        count += len(cell.cur_pos)
    return count
# Main code
def main():
    desired_steps = 100
    steps = 0
    # Initialise set of current positions
    map_cells = {(0,0):mapCell()}
    map_cells[(0,0)].cur_pos.add(start)
    next_pos = set(())

    while steps < desired_steps:
        for map_cell in map_cells.values():
            if not map_cell.full:
                for pos in map_cell.cur_pos:
                    next_pos.update(getValidNeighbours(pos))
                map_cell.cur_pos.clear()
        for new_pos in next_pos:
            (r, c) = new_pos
            map_cell = (r//height, c//width)
            if map_cell in map_cells:
                map_cells[map_cell].cur_pos.add(new_pos)
            else:
                map_cells[map_cell] = mapCell()
                map_cells[map_cell].cur_pos.add(new_pos)
        next_pos.clear()
        steps +=1

    # for k, v in map_cells.items(): print(f"{k}: {v}")
    positions = totalCount(map_cells)

    # for position in cur_pos:
    #     print(position)

    answer = positions
    print("The solution is:",answer)

main()
