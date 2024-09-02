from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

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


# input = array (list of lists or list of strings? only reading so perhaps list of strings)
# frontier = priorityqueue of cells to be evaluated
# cell has p: priority r: row, c: col, l: lastmove, m: momentum
# or (priority, data): data.r, .c, .last, .m
# Last move and momentum help determine next valid cells to inspect

# Variables
th = 2         # Test finds optimum at th = 11, puzzle 1174 at 8

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

class Thing:
    def __init__(self, r: int, c: int, d: int, p: str = "", p2: str = "", p3: str = "", m: int = 1) -> None:
        self.r = r
        self.c = c
        self.d = d
        self.p = p
        self.p2 = p2
        self.p3 = p3
        self.m = m

    def __str__(self) -> str:
        return f"r: {self.r}, c: {self.c}, d: {self.d}, p: {self.p}, p2: {self.p2}, m: {self.m}"

    def priority(self) -> int:
        # end = grid[self.r][self.c].endDist
        end = width - 1 - self.c + height - 1 - self.r
        return self.d + end # test finds optimum at 4*end

    '''
    Constraints:
    Cant return to previous cell
    Cant keep going if m > 2
    No point turning back on self after only one turn
    '''

    '''
    Improvements
    Match case on previous direction
    Only go up or left once, never double back

    '''


    def lookRight(self):
        rightBestDist = grid[self.r][self.c+1].bestDist
        rightDist = self.d + grid[self.r][self.c+1].heat
        if rightDist < rightBestDist: rightBestDist = grid[self.r][self.c+1].bestDist = rightDist
        if rightDist < rightBestDist + th:
            right: Thing = Thing(self.r, self.c+1, rightDist, ">", self.p, self.p2, self.m + 1 if self.p == ">" else 1)
            return [PrioritizedItem(right.priority(), right)]
        else:
            return []

    def lookDown(self):
        downBestDist = grid[self.r+1][self.c].bestDist
        downDist = self.d + grid[self.r+1][self.c].heat
        if downDist < downBestDist: downBestDist = grid[self.r+1][self.c].bestDist = downDist
        if downDist < downBestDist + th:
            down: Thing = Thing(self.r+1, self.c, downDist, "v", self.p, self.p2, self.m + 1 if self.p == "v" else 1)
            return [PrioritizedItem(down.priority(), down)]
        else:
            return []

    def lookLeft(self):
        leftBestDist = grid[self.r][self.c-1].bestDist
        leftDist = self.d + grid[self.r][self.c-1].heat
        if leftDist < leftBestDist: leftBestDist = grid[self.r][self.c-1].bestDist = leftDist
        if leftDist < leftBestDist + th:
            left: Thing = Thing(self.r, self.c-1, leftDist, "<", self.p, self.p2, self.m + 1 if self.p == "<" else 1)
            return [PrioritizedItem(left.priority(), left)]
        else:
            return []

    def lookUp(self):
        upBestDist = grid[self.r-1][self.c].bestDist
        upDist = self.d + grid[self.r-1][self.c].heat
        if upDist < upBestDist: upBestDist = grid[self.r-1][self.c].bestDist = upDist
        if upDist < upBestDist + th:
            up: Thing = Thing(self.r-1, self.c, upDist, "^", self.p, self.p2, self.m + 1 if self.p == "^" else 1)
            return [PrioritizedItem(up.priority(), up)]
        else:
            return []

    def getNeighbours(self) -> list:
        # urdl = 0b1000, 0b0100, 0b0010, 0b0001
        # u, r, d, l = 0b00, 0b01, 0b11, 0b10
        # opposite = u ^ 0b11
        # go = 0b1111
        # if self.p == 0b0001: go &= 0b1110 # if left don't loop back up
        # if self.p == 0b1000: go &= 0b0111 # if up don't loop back left
        # if self.m == 1: nogo.append(opposite[self.p2]) # don't double back
        # if self.m > 2: nogo.append(self.p) # momentum constraint
        # up go if go ^ 0b1000

        neighbours = []

        match self.p:
            case ">":
                match self.p2:
                    case ">":
                        if self.p3 != ">" and self.c < width - 1: neighbours += self.lookRight() # > > >
                        if self.r > 0: neighbours += self.lookUp() # > > ^
                        if self.r < height - 1: neighbours += self.lookDown() # > > v
                        return neighbours
                    case "v":
                        if self.c < width - 1: neighbours += self.lookRight() # v > >
                        if self.r < height - 1: neighbours += self.lookDown() # v > v
                        return neighbours
                    case "^":
                        if self.r > 0: neighbours += self.lookUp() # ^ > ^ delete to optimise
                        if self.c < width - 1: neighbours += self.lookRight() # ^ > >
                        return neighbours
                    case "":
                        # Second cells
                        neighbours += self.lookRight() # > >
                        neighbours += self.lookDown() # > v
                        return neighbours
            case "v":
                match self.p2:
                    case ">":
                        if self.p3 != "<" and self.c < width - 1: neighbours += self.lookRight() # > v >
                        if self.r < height - 1: neighbours += self.lookDown() # > v v
                        return neighbours
                    case "v":
                        if self.p3 != "v" and self.r < height - 1: neighbours += self.lookDown() # v v v
                        if self.c > 0: neighbours += self.lookLeft() # v v <
                        if self.c < width - 1: neighbours += self.lookRight() # v v >
                        return neighbours
                    case "<":
                        if self.c > 0: neighbours += self.lookLeft() # < v < delete to optimise
                        if self.r < height - 1: neighbours += self.lookDown() # < v v
                        return neighbours
                    case "":
                        # Second cells
                        neighbours += self.lookRight() # v >
                        neighbours += self.lookDown() # v v
                        return neighbours
            case "^":
                # If up, just go right
                if self.c < width-1: return self.lookRight()
                else: return []
            case "<":
                # If left just go down
                if self.r < height-1: return self.lookDown()
                else: return []
            case "":
                # First cell
                neighbours += self.lookRight() # v >
                neighbours += self.lookDown() # v v
                return neighbours

        '''
        opposite = {"":"","v":"^", "^":"v", "<":">", ">":"<"}
        nogo = [opposite[self.p]] # don't reverse
        if self.p == "<": nogo.append("^") # don't loop back
        if self.p == "^": nogo.append("<") # don't loop back
        if self.m == 1: nogo.append(opposite[self.p2]) # don't double back
        if self.m > 2: nogo.append(self.p) # momentum constraint
        if self.r > 0 and "^" not in nogo:
            upBestDist = grid[self.r-1][self.c].bestDist
            upDist = self.d + grid[self.r-1][self.c].heat
            if upDist < upBestDist: upBestDist = grid[self.r-1][self.c].bestDist = upDist
            if upDist < upBestDist + th:
                up: Thing = Thing(self.r-1, self.c, upDist, "^", self.p, self.m + 1 if self.p == "^" else 1)
                neighbours.append(PrioritizedItem(up.priority(), up))
        if self.r < height-1 and "v" not in nogo:
            downBestDist = grid[self.r-1][self.c].bestDist
            downDist = self.d + grid[self.r+1][self.c].heat
            if downDist < downBestDist: downBestDist = grid[self.r+1][self.c].bestDist = downDist
            if downDist < downBestDist + th:
                down: Thing = Thing(self.r+1, self.c, downDist, "v", self.p, self.m + 1 if self.p == "v" else 1)
                neighbours.append(PrioritizedItem(down.priority(), down))
        if self.c > 0 and "<" not in nogo:
            leftBestDist = grid[self.r-1][self.c].bestDist
            leftDist = self.d + grid[self.r][self.c-1].heat
            if leftDist < leftBestDist: leftBestDist = grid[self.r][self.c-1].bestDist = leftDist
            if leftDist < leftBestDist + th:
                left: Thing = Thing(self.r, self.c-1, leftDist, "<", self.p, self.m + 1 if self.p == "<" else 1)
                neighbours.append(PrioritizedItem(left.priority(), left))
        if self.c < width-1 and ">" not in nogo:
            rightBestDist = grid[self.r-1][self.c].bestDist
            rightDist = self.d + grid[self.r][self.c+1].heat
            if rightDist < rightBestDist: rightBestDist = grid[self.r][self.c+1].bestDist = rightDist
            if rightDist < rightBestDist + th:
                right: Thing = Thing(self.r, self.c+1, rightDist, ">", self.p, self.m + 1 if self.p == ">" else 1)
                neighbours.append(PrioritizedItem(right.priority(), right))
        return neighbours
        '''

class Cell:
    def __init__(self, r: int, c: int, heat: int, bestDist: int = 9999, endDist: int = 9999) -> None:
        self.r = r
        self.c = c
        self.heat = heat
        self.bestDist = bestDist
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
        self.last = "."
        self.momentum = 0

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
    with open("puzzle_input.txt") as file:
        input = [[Cell(r, c, int(char)) for c, char in enumerate(line)] for r, line in enumerate(file.read().splitlines())]

    # For all cells: Find and update baseline distance from cell to end
    for row in input:
        for cell in row:
            cell.endDist = findBaseline(input, cell.r, cell.c)

    return input

# Main code
grid = initialise()

with open("puzzle_input.txt") as file:
    heatMap = file.read().splitlines()

height = len(grid)
width = len(grid[0])

def getHeuristic(vertex):
    (r, c) = vertex[0]
    return abs(height-1-r) + abs(width-1-c)

def getNeighbours(vertex):
    (r,c) = vertex[0]
    movement = vertex[1]
    m = vertex[2]
    neighbours = []
    match movement:
        case "^":
            if r > 0 and m < 3: neighbours.append(((r-1,c), "^", m+1)) # up
            if c > 0: neighbours.append(((r,c-1), "<", 1)) #left
            if c < width -1: neighbours.append(((r,c+1), ">", 1)) #right
        case ">":
            if r > 0: neighbours.append(((r-1,c), "^", 1)) # up
            if c < width -1 and m < 3: neighbours.append(((r,c+1), ">", m+1)) # right
            if r < height -1: neighbours.append(((r+1,c), "v", 1))# down
        case "v":
            if c < width -1: neighbours.append(((r,c+1), ">", 1)) # right
            if r < height -1 and m < 3: neighbours.append(((r+1,c), "v", m+1)) # down
            if c > 0: neighbours.append(((r,c-1), "<", 1)) # left
        case "<":
            if r < height -1: neighbours.append(((r+1,c), "v", 1)) # down
            if c > 0 and m < 3: neighbours.append(((r,c-1), "<", m+1)) # left
            if r > 0: neighbours.append(((r-1,c), "^", 1)) # up
        case "":
            neighbours.append(((r,c+1), ">", 1)) # right
            neighbours.append(((r+1,c), "v", 1)) # down
    return neighbours

def distance(vertex):
    (r,c) = vertex[0]
    movement = vertex[1]
    match movement:
        case "^":
            return distance
            pass
        case ">":
            pass
        case "v":
            pass
        case "<":
            pass
        case "":
            pass


def main4():

    visited = {} # vertices that have been evaluated; {vertex: distance}
    frontier = PriorityQueue() # next vertices to be evaluated PrioritisedItem(priority, vertex)

    origin = ((0,0),"",0) # first vertex
    visited[origin] = 0 # update visited with first vertex and distance
    frontier.put(PrioritizedItem(0, origin))
    searching = True

    while searching:
        nextPI = frontier.get()
        next = nextPI.item
        distance_so_far = visited[next]
        if next[0] == (width-1, height-1):
            print(f"Destination reached with total heat: {visited[next]}")
            print(next)
            searching = False
        else:
            neighbours = getNeighbours(next)
            for neighbour in neighbours:
                # get distance for neighbour
                (r,c) = neighbour[0]
                heat = int(heatMap[r][c])
                distance = distance_so_far + heat
                # if not in visited: add to visited, update best distance and add to frontier queue
                if neighbour not in visited.keys():
                    visited[neighbour] = distance
                    heuristic = abs(height-r) + abs(width-c)
                    frontier.put(PrioritizedItem(distance + heuristic, neighbour))
                elif distance < visited[neighbour]:
                    visited[neighbour] = distance
                    heuristic = abs(height-r) + abs(width-c)
                    frontier.put(PrioritizedItem(distance + heuristic, neighbour))
                else:
                    pass


                # if in visited, compare best distance and update if best distance is less

    top = 10
    topCount = 0
    print(f"Top {top}:")
    while not frontier.empty():
        topCount +=1
        vertex = frontier.get()
        if topCount < top:
            print(vertex.priority, vertex.item, visited[vertex.item])
    print(f"of {topCount} remaining frontiers")


def main3():
    frontier = PriorityQueue()
    origin: Thing = Thing(0,0,0)
    frontier.put(PrioritizedItem(origin.priority(), origin))
    searching = True
    # count = 0
    while searching: #  and count < 10000000:
        cell: Thing = frontier.get().item
        if cell.r == height -1 and cell.c == width-1:
            print(f"Destination reached with total heat: {cell.d}")
            print(cell)
            searching = False
        else:
            # count +=1
            neighbours: list[Thing] = cell.getNeighbours()
            for neighbour in neighbours:
                frontier.put(neighbour)

        if frontier.empty():
            print("Ran out of nodes")
            searching = False

    count10 = 0
    print("Top 10:")
    while not frontier.empty():
        count10 +=1
        cell = frontier.get()
        if count10 < 10:
            print(cell.priority, cell.item, "e:", (cell.item.priority()-cell.item.d)//2)
    print(f"of {count10} frontiers")

def main2():
    # Create city grid (array of cell objects) from puzzle input
    input = initialise()
    height = len(input)
    width = len(input[0])

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
    heuristic = input[0][0].endDist
    print("Evaluating paths")
    while len(currentQueue) > 0:
        for node in currentQueue:
            noGo = "."
            if node.hist[0] == node.hist[1] and node.hist[1] == node.hist[2]:
                noGo = node.hist[2]
            children = []
            if node.cell.c < width-1 and noGo != ">":
                rightHeuristic = input[node.cell.r][node.cell.c + 1].endDist + node.dist <= heuristic
                if rightHeuristic:
                    right: Node = Node(input[node.cell.r][node.cell.c + 1], node)
                    right.dist = node.dist + right.cell.heat
                    right.hist = node.hist[1:] + [">"]
                    children.append(right)
            if node.cell.r < height-1 and noGo != "v":
                downHeuristic = input[node.cell.r + 1][node.cell.c].endDist + node.dist <= heuristic
                if downHeuristic:
                    down: Node = Node(input[node.cell.r + 1][node.cell.c], node)
                    down.dist = node.dist + down.cell.heat
                    down.hist = node.hist[1:] + ["v"]
                    children.append(down)
            if node.cell.c > 0 and noGo != "<":
                rightHeuristic = input[node.cell.r][node.cell.c - 1].endDist + node.dist <= heuristic
                if rightHeuristic:
                    left: Node = Node(input[node.cell.r][node.cell.c - 1], node)
                    left.dist = node.dist + left.cell.heat
                    left.hist = node.hist[1:] + ["<"]
                    children.append(left)
            if node.cell.r > 0 and noGo != "^":
                upHeuristic = input[node.cell.r - 1][node.cell.c].endDist + node.dist <= heuristic
                if upHeuristic:
                    up: Node = Node(input[node.cell.r - 1][node.cell.c], node)
                    up.dist = node.dist + up.cell.heat
                    up.hist = node.hist[1:] + ["^"]
                    children.append(up)

            for child in children:
                nextQueue.append(child)
                pathNodes.append(child)
            children.clear()
        currentQueue.clear()
        currentQueue.extend(nextQueue)
        nextQueue.clear()

    # Find shortest path
    print("Finding shortest path")
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

main4()
