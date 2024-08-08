# Problem scope
'''
Get your "lava crucible" from the lava pool to the factory losing the least amount of heat
Input is a city map. Each tile is a city block and the number in the tile is the "heat lost" on that tile
The crucible can move at most 3 steps in one direction before it needs to turn left or right
Crucible can never turn back on left, right or straight on.
It loses heat when it enters a tile therefore does not lose heat on the first tile unless it is entered again
What is the minimum heat loss?
'''

# Solution sketch
'''
Ok, having seen a few videos on djiksras and a* search algorithms I have a better idea of how to solve a problem like this.
But the 3 limit streight line limit sounds hard.
I think I can solve the length limit constraint by storing the shortest path to each point as well as it's overall length.
This way I can invalidate too long paths and disqualify them.

Note! The heat loss from the first block is not included

'''
# Variables
class Cell:
    def __init__(self, r: int, c: int, heat: int, path: list = [], dist: int = 9999) -> None:
        self.r = r
        self.c = c
        self.heat = heat
        self.path = path
        self.dist = dist

    def __str__(self) -> str:
        return f"({self.r}, {self.c}) heat: {self.heat}, shortest path: {self.path}, shortest distance: {self.dist}"

with open("test_input.txt") as file:
    input = [[Cell(r, c, int(char)) for c, char in enumerate(line)] for r, line in enumerate(file.read().splitlines())]

input[0][0].dist = 0 # starting square has zero distance from start

# for line in input:
#     for col in line:
#         print(col)

example = '''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''
example_min_path = '''
2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
'''

# Functions

# Main code
def main():
    # Create an array to store
    #   Input cell values (heats), done
    #   Shortest distance from start (default high, update as we go)
    #   Shortest path to this point
    #   Possibly a heuristic for distance to end (if using A* method for optimising)

    # Start top left and evaluate next diagonal row of adjacent cells
    height = len(input)
    width = len(input[0])
    queue = []
    queue.append(input[0][0])
    next_queue = []
    rerun = True # If needed can use this to trigger a complete rescan of the map
    run_count = 0
    # input[0][0][2] = ["v", ">", "^", "<"]
    while rerun:
        rerun = False
        run_count +=1
        while len(queue)>0:
            for cell in queue:
                # Is movement restricted?
                last_3 = ["a", "b", "c"]
                cant_go = None
                if cell.path and len(cell.path) > 2:
                    last_3 = cell.path[-3:]
                    if last_3[0] == last_3[1] and last_3[1] == last_3[2]:
                        cant_go = last_3[0]

                # if adjacent cell is valid considering edges and movement restrictions:
                #   if new shortest distance < current distance:
                #       Update distance; update path; add new cell to next queue
                if cell.r > 0 and cant_go != "^":
                    up: Cell = input[cell.r - 1][cell.c]
                    if cell.dist + up.heat < up.dist:
                        up.dist = cell.dist + up.heat
                        up.path = cell.path + ['^']
                        next_queue.append(up)
                        rerun = True
                if cell.r < height-1 and cant_go != "v":
                    down: Cell = input[cell.r + 1][cell.c]
                    if cell.dist + down.heat < down.dist:
                        down.dist = cell.dist + down.heat
                        down.path = cell.path + ['v']
                        next_queue.append(down)
                        rerun = True
                if cell.c > 0 and cant_go != "<":
                    left: Cell = input[cell.r][cell.c - 1]
                    if cell.dist + left.heat < left.dist:
                        left.dist = cell.dist + left.heat
                        left.path = cell.path + ['<']
                        next_queue.append(left)
                        rerun = True
                if cell.c < width-1 and cant_go != ">":
                    right: Cell = input[cell.r][cell.c + 1]
                    if cell.dist + right.heat < right.dist:
                        right.dist = cell.dist + right.heat
                        right.path = cell.path + ['>']
                        next_queue.append(right)
                        rerun = True

                # for item in next_queue: print(item)
            queue.clear()
            queue.extend(next_queue)
            next_queue.clear()
        print(f"run {run_count}, shortest path: {input[height-1][width-1].path}, distance: {input[height-1][width-1].dist}")

    for line in input:
        for cell in line:
            print(f"cell (row {cell.r}, col{cell.c}): dist {cell.dist}")
    print(f"The solution is: {input[height-1][width-1].dist}")


main()
