from collections import defaultdict

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
input = "puzzle_input.txt"
with open(input) as file:
    data = file.read().splitlines()

width = len(data[0])
height = len(data)

match input:
    case "puzzle_input.txt": full_count = (7717, 7693)
    case "test_input.txt": full_count = (42, 39)

# Find start location
for r, line in enumerate(data):
    for c, char in enumerate(line):
        if char == "S":
            start = (r, c)

Location = tuple[int, int]

class mapCell:
    def __init__(self, vis_pos = None, cur_pos = None, new_pos = None, modified = False) -> None:
        self.vis_pos = vis_pos if vis_pos is not None else set(())
        self.cur_pos = cur_pos if cur_pos is not None else set(())
        self.new_pos = new_pos if new_pos is not None else set(())
        self.modified = modified
        self.buffer = 0

    def __str__(self) -> str:
        return f"{len(self.vis_pos) + len(self.cur_pos)} positions"

    def count(self) -> int:
        return len(self.vis_pos) + len(self.cur_pos)

    def full(self) -> bool:
        if len(self.vis_pos) in full_count:
            self.buffer +=1
        return self.buffer >2

class mapCell2:
    def __init__(self, vis_pos = None, cur_pos = None, new_pos = None) -> None:
        self.vis_pos = vis_pos if vis_pos is not None else set(())
        self.cur_pos = cur_pos if cur_pos is not None else set(())
        self.new_pos = new_pos if new_pos is not None else set(())
        #self.buffer = 0

    def __str__(self) -> str:
        return f"{len(self.vis_pos)} positions"

    def count(self) -> int:
        return len(self.vis_pos)

    def full(self) -> bool:
        # if len(self.vis_pos) in full_count:
        #     self.buffer +=1
        # return self.buffer >3
        return len(self.vis_pos) in full_count

# Functions
def getValidNeighbours(location: Location) -> list[Location]:
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

def getVNN(location):
    (r, c) = location
    neighbours = set(())
    # North
    if data[(r-1) % height][c % width] != "#":
        if data[(r-2) % height][c % width] != "#": neighbours.add((r-2, c)) # North
        if data[(r-1) % height][(c+1) % width] != "#": neighbours.add((r-1, c+1)) # East
        if data[(r-1) % height][(c-1) % width] != "#": neighbours.add((r-1, c-1)) # West
    # East
    if data[r % height][(c+1) % width] != "#":
        if data[(r-1) % height][(c+1) % width] != "#": neighbours.add((r-1, c+1)) # North
        if data[r % height][(c+2) % width] != "#": neighbours.add((r, c+2)) # East
        if data[(r+1) % height][(c+1) % width] != "#": neighbours.add((r+1, c+1)) # South
    # South
    if data[(r+1) % height][c % width] != "#":
        if data[(r+1) % height][(c+1) % width] != "#": neighbours.add((r+1, c+1)) # East
        if data[(r+2) % height][c % width] != "#": neighbours.add((r+2, c)) # South
        if data[(r+1) % height][(c-1) % width] != "#": neighbours.add((r+1, c-1)) # West
    # West
    if data[r % height][(c-1) % width] != "#":
        if data[(r-1) % height][(c-1) % width] != "#": neighbours.add((r-1, c-1)) # North
        if data[(r+1) % height][(c-1) % width] != "#": neighbours.add((r+1, c-1)) # South
        if data[r % height][(c-2) % width] != "#": neighbours.add((r, c-2)) # West
    return neighbours


def totalCount(map: dict) -> int:
    count = 0
    for cell in map.values():
        count += len(cell.vis_pos)
        count += len(cell.cur_pos)
    return count

# Main code
def main2():
    desired_steps = 5000
    steps = 0

    next = set(())
    new = set(())
    prev = set(())
    # pprev = set(())

    plots = 0

    next.add(start)


    # Find neighbours to recent next cells
    while steps < desired_steps:
        for pos in next:
            new.update(getValidNeighbours(pos))

        new -= next # new cells not duplicating cells just come from
        new -= prev # new cells not in those last checked
        # new -= pprev # new cells not in those checked the time before

        if steps % 2 == 0: plots += len(next)
        # pprev.clear()
        # pprev.update(prev)
        prev.clear()
        prev.update(next)
        next.clear()
        next.update(new)
        new.clear()


        steps+=1
        # print(steps, len(next), len(prev), plots)

    final_plot_count = plots  + len(next) # + len(pprev)

    print(f"Total plots: {final_plot_count}")


def main():
    desired_steps = 327 # the steps walked after 2.5 maps cells crossed
    steps = 0
    # Initialise cell and positions tracker depending on if target is odd or even
    map_cells = defaultdict(mapCell)
    if desired_steps % 2 == 0:
        map_cells[(0,0)].cur_pos.add(start)
    else:
        map_cells[(0,0)].cur_pos.update(getValidNeighbours(start))
        steps +=1

    next_pos = set(())
    positions = 0

    while steps < desired_steps:
        # Find neighbours to recent new positions
        cell_list = [value for value in map_cells.values()]
        for map_cell in cell_list:
            for pos in map_cell.cur_pos:
                next_pos.update(getVNN(pos))

            # Add potential new neighbours to map cells
            for pos in next_pos:
                (r, c) = pos
                map_cell = (r//height, c//width)
                map_cells[map_cell].new_pos.add(pos)
            next_pos.clear()

        # If new neighbours are actually new shift them into the current positions
        for ms in map_cells.values():
            ms.new_pos -= ms.vis_pos
            ms.new_pos -= ms.cur_pos
            ms.vis_pos.update(ms.cur_pos)
            ms.cur_pos.clear()
            ms.cur_pos.update(ms.new_pos)
            ms.new_pos.clear()



        steps +=2
        # for k, v in map_cells.items(): print(steps, k, v)

    # grid cells walked after initial in 26501365 steps is 202300 (s - half width of first cell: 65 / width of cell: 131)
    # There is a clear path from centre to edges of starting map so new map cells will always start at the centre of an edge.
    #  .^.
    # ./#\.
    # <#@#>
    # '\#/'
    #  'v'
    # ^^ After two map cell walks.
    # From puzzling it out on paper the formula for total plots should be:
    # (n-1)^2 * count(0,0) + [diamond of even-step map cells]
    # n^2 * count(0,1) + [diamond of odd-step map cells]
    # 4(n-1) * (count(1,1) + count(1,-1) + count(-1,1) + count(-1,-1)) +
    # 4n * (count(1,2)+ count(-1,2) + count(-1,-2) + count(1,-2)) +
    # (count(0,2) + count(0,-2) + count(2,0) + count(-2,0)) [^, >, V, < tips of diamond]

    n= 202300
    total = (
        (n-1)**2 * map_cells[(0,0)].count() +
        n**2 * map_cells[(0,1)].count() +
        (n-1) * (map_cells[(1,1)].count() + map_cells[(1,-1)].count() + map_cells[(-1,1)].count() + map_cells[(-1,-1)].count()) +
        n * (map_cells[(1,2)].count()+ map_cells[(-1,2)].count() + map_cells[(-1,-2)].count() + map_cells[(1,-2)].count()) +
        (map_cells[(0,2)].count() + map_cells[(0,-2)].count() + map_cells[(2,0)].count() + map_cells[(-2,0)].count())
    )

    print(f"The formula gives: {total} positions")
    # for k, v in map_cells.items(): print(f"{k}: {v}")

    # Count all visited cells to check formula works for n = 2
    print(f"{len(map_cells)} map cells")
    for k,v in map_cells.items():
        print(f"{k}, {v}")
    positions += totalCount(map_cells)

    # for k, v in map_cells.items():
    #     print(k, v)

    answer = positions
    print("The solution is:",answer)

main()
