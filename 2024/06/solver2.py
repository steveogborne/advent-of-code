# Problem scope
'''
Part 1: Guard patrol
Puzzle input is a map
. is space, # is obstacle, [^>v<] is the guard depending on the faced direction
Guard takes a step, if it hits an obstacle it rotates 90d CW
Count how many squares are in teh guards path

Part 2: Looper
Add one obstacle to make a loop.
How many positions can you add an obstacle to make a loop?
'''

# Solution sketch
'''
Part 1:
Rotate function
Step function
Colour in function
Stop when the guard leaves the map. (What if it doesn't???)

Part 2:
Add functionality to check for loops. Perhaps store position in map cells and check for repeats
Brute force check all positions to see if loops created. Save time by only searching on original path
'''
# Variables
with open("puzzle_input.txt") as file:
    startMap = [list(line) for line in file.read().splitlines()]
    tracker = [[[] for cell in row] for row in startMap]

# Functions
def rotate(dir: str) -> str:
    index = "^>v<".index(dir)
    index = (index + 1) % 4
    return "^>v<"[index]

def colour(map, r, c) -> list:
    map[r][c] = "X"
    return map

def step(map, r, c, dir):
    match dir:
        case "^":
            try:
                if map[r-1][c] == "#":
                    return (map, r, c, rotate(dir), True)
                else:
                    map = colour(map, r, c)
                    return (map, r-1, c, dir, True)
            except:
                map = colour(map, r, c)
                return (map, r, c, dir, False)
        case ">":
            try:
                if map[r][c+1] == "#": return (map, r, c, rotate(dir), True)
                else:
                    map = colour(map, r, c)
                    return (map, r, c+1, dir, True)
            except:
                map = colour(map, r, c)
                return (map, r, c, dir, False)
        case "v":
            try:
                if map[r+1][c] == "#": return (map, r, c, rotate(dir), True)
                else:
                    map = colour(map, r, c)
                    return (map, r+1, c, dir, True)
            except:
                map = colour(map, r, c)
                return (map, r, c, dir, False)
        case "<":
            try:
                if map[r][c-1] == "#": return (map, r, c, rotate(dir), True)
                else:
                    map = colour(map, r, c)
                    return (map, r, c-1, dir, True)
            except:
                map = colour(map, r, c)
                return (map, r, c, dir, False)

def initialise_guard() -> int:
    for r, row in enumerate(startMap):
        for c, cell in enumerate(row):
            if cell == "^":
                tracker[r][c].append((r,c,"^"))
                return r, c, "^", True

def loop_found(tracker, r,c,dir) -> bool:
    return (r,c,dir) in tracker[r][c]

def initialise_map(r, c, dir, inbounds):
    originalMap = [line.copy() for line in startMap]
    while inbounds:
        originalMap, r, c, dir, inbounds = step(originalMap, r, c, dir)
    return originalMap

def initialise_path_list(map, rstart, cstart) -> list:
    pathList = []
    for r, row in enumerate(map):
        for c, cell in enumerate(row):
            if cell == "X": pathList.append((r,c))
    pathList.remove((rstart, cstart))
    return pathList

def resetTracker(rstart, cstart):
    for r, line in enumerate(tracker):
        for c, cell in enumerate(line):
            if r == rstart and c == cstart:
                tracker[r][c] = [(rstart, cstart, "^")]
            else: tracker[r][c] = []

# Main code
def main():
    loops = 0
    rStart, cStart, dirStart, inbounds = initialise_guard()
    pathList = initialise_path_list(initialise_map(rStart, cStart, dirStart, inbounds), rStart, cStart)

    # for line in startMap: print(line)

    for cell in pathList:
        r, c, dir, inbounds = rStart, cStart, dirStart, True
        # print(cell)
        newMap = [line.copy() for line in startMap]
        newMap[cell[0]][cell[1]] = "#"
        while inbounds:
            newMap, r, c, dir, inbounds = step(newMap, r, c, dir)
            if inbounds and loop_found(tracker, r, c, dir):
                loops +=1
                inbounds = False
                # for line in newMap: print(line)
            else: tracker[r][c].append((r,c,dir))
        resetTracker(rStart, cStart)

    print("The solution is:",loops)

main()
