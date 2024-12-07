# Problem scope
'''
Part 1: Guard patrol
Puzzle input is a map
. is space, # is obstacle, [^>v<] is the guard depending on the faced direction
Guard takes a step, if it hits an obstacle it rotates 90d CW
Count how many squares are in teh guards path
'''

# Solution sketch
'''
Part 1:
Rotate function
Step function
Colour in function
Stop when the guard leaves the map. (What if it doesn't???)
'''
# Variables
with open("puzzle_input.txt") as file:
    map = [list(line) for line in file.read().splitlines()]

# Functions
def rotate(dir: str) -> str:
    index = "^>v<".index(dir)
    index = (index + 1) % 4
    return "^>v<"[index]

def colour(r, c) -> None:
    map[r][c] = "X"

def step(r, c, dir):
    match dir:
        case "^":
            try:
                if map[r-1][c] == "#": return (r, c, rotate(dir), True)
                else:
                    colour(r, c)
                    return (r-1, c, dir, True)
            except:
                colour(r, c)
                return (r, c, dir, False)
        case ">":
            try:
                if map[r][c+1] == "#": return (r, c, rotate(dir), True)
                else:
                    colour(r, c)
                    return (r, c+1, dir, True)
            except:
                colour(r, c)
                return (r, c, dir, False)
        case "v":
            try:
                if map[r+1][c] == "#": return (r, c, rotate(dir), True)
                else:
                    colour(r, c)
                    return (r+1, c, dir, True)
            except:
                colour(r, c)
                return (r, c, dir, False)
        case "<":
            try:
                if map[r][c-1] == "#": return (r, c, rotate(dir), True)
                else:
                    colour(r, c)
                    return (r, c-1, dir, True)
            except:
                colour(r, c)
                return (r, c, dir, False)

def count_x() -> int:
    count = 0
    for row in map:
        for cell in row:
            if cell == "X": count +=1
    return count

def initialise_guard() -> int:
    for r, row in enumerate(map):
        for c, cell in enumerate(row):
            if cell == "^":
                return r, c

# Main code
def main():
    dir = "^"
    inbounds = True
    r, c = initialise_guard()
    while inbounds:
        r, c, dir, inbounds = step(r, c, dir)

    for line in map: print("".join(line))
    answer = count_x()
    print("The solution is:",answer)

main()
