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

# Variables
class Cell:
    def __init__(self, r: int, c: int, heat: int, path: list = None, endDist: int = 9999) -> None:
        self.r = r
        self.c = c
        self.heat = heat
        self.endDist = endDist

    def __str__(self) -> str:
        return f"({self.r}, {self.c}) heat: {self.heat}, shortest path: {self.path}, shortest distance: {self.dist}"

class Node:
    def __init__(self, cell: Cell, parent: Cell, children: list = None, dist: int = 9999, hist: list = [".",".","."]) -> None:
        self.cell = cell
        self.parent = parent
        self.children = children if children is not None else []
        self.dist = dist
        self.hist = hist

# Functions
def findBaseline(grid, startR, startC) -> int:
    height = len(grid)
    width = len(grid[0])
    if startC < width:
        r = startR
        rcount = 0
        c = startC + 1
        ccount = 1
    else:
        r = startR + 1
        rcount = 1
        c = startC
        ccount = 0
    baseline = 0
    while r < height and c < width:
        baseline += grid[r][c].heat
        if r == c :
            c += 1
            ccount += 1
            rcount = 0
        elif r > c:
            if ccount < 3:
                c += 1
                ccount +=1
                rcount = 0
            elif r < height:
                r += 1
                ccount = 0
                rcount +=1
            else: # r = height
                r -= 1
                ccount = rcount = 0
        else: # r < c
            if rcount < 3:
                r += 1
                rcount += 1
                ccount = 0
            elif c < width:
                c += 1
                ccount += 1
                rcount = 0
            else: # c = width
                c -= 1
                ccount = rcount = 0
    return baseline

def initialise() -> list:
    # Parse input and create array of cell objects
    with open("test_input.txt") as file:
        input = [[Cell(r, c, int(char)) for c, char in enumerate(line)] for r, line in enumerate(file.read().splitlines())]

    # For all cells: Find and update baseline distance from cell to end
    for row in input:
        for cell in row:
            cell.endDist = findBaseline(input, cell.r, cell.c)

def displayPath(path):
    pass

# Main code
def main2():
    # Create city grid (array of cell objects) from puzzle input
    input = initialise()

    # Create start node from start cell
    pathNodes = []
    pathNodes.append(Node(input[0][0], None))
    pathNodes[0].dist = 0

    # Create queues and add start node
    currentQueue = []
    nextQueue = []
    currentQueue.append(pathNodes[0])

    # Test boundaries and movement constraints to establish children (MVP: down, right)
    # Calc running distance for node
    # Add children to queue
    height = len(input)
    width = len(input[0])
    while len(currentQueue) > 0:
        for node in currentQueue:
            noGo = "."
            if node.hist[0] == node.hist[1] and node.hist[1] == node.hist[2]:
                noGo = node.hist[2]
            children = []
            if node.cell.c < width-1 and noGo != ">":
                right: Node = Node(input[node.cell.r][node.cell.c + 1], node)
                right.dist = node.dist + right.cell.heat
                right.hist = node.hist[1:] + [">"]
                children.append(right)
            if node.cell.r < height-1 and noGo != "v":
                down: Node = Node(input[node.cell.r + 1][node.cell.c], node)
                down.dist = node.dist + down.cell.heat
                down.hist = node.hist[1:] + ["v"]
                children.append(down)
            # if node.cell.c > 0:
            #   left: Node = Node(input[node.cell.r][node.cell.c - 1], node)
            #   left.dist = node.dist + left.cell.heat
            #   children.append(left)
            # if node.cell.r > 0
            #   up: Node = Node(input[node.cell.r - 1][node.cell.c], node)
            #   up.dist = node.dist + up.cell.heat
            #   children.append(up)
            for child in children:
                nextQueue.append(child)
                pathNodes.append(child)
            children.clear()
        currentQueue.clear()
        currentQueue.extend(nextQueue)
        nextQueue.clear()

    # Find shortest path
    bestEnd = None
    endNodeCount = 0
    for node in pathNodes:
        if node.cell == input[-1][-1]:
            endNodeCount += 1
            # print(f"End node found with distance {node.dist}")
            if bestEnd == None or node.dist < bestEnd.dist:
                bestEnd = node

    print(f"Shortest of {endNodeCount} paths has distance: {bestEnd.dist}")


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
                        # print(f"Can't go {cant_go} from {cell.r}, {cell.c}")

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

    # for line in input:
    #     for cell in line:
    #         print(f"cell (row {cell.r}, col{cell.c}): dist {cell.dist}")

    for line in input:
        print(([str(cell.dist) for cell in line]))

    print(f"The solution is: {input[height-1][width-1].dist}")

def main3():
    input = initialise()
main3()
