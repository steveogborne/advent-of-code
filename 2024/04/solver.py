# Problem scope
'''
Part 1: Crossword
Search the grid for XMAS. It can go up, down, left right and diagonal.
'''

# Solution sketch
'''
For every cell check 8 compass points for xmas
Don't search for samx to avoid duplicates
Include precautions for out of bounds
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()

# Functions
def search_at(r: int, c:int, log = None) -> int:
    count = 0

    # Up
    try:
        if r > 2 and input[r-1][c] + input[r-2][c] + input[r-3][c] == "MAS":
            count +=1
            if log: print(f"Up at ({r},{c}): X{input[r-1][c] + input[r-2][c] + input[r-3][c]}")
    except: pass

    # Up-Right
    try:
        if r > 2 and c < len(input[0]) - 3 and input[r-1][c+1] + input[r-2][c+2] + input[r-3][c+3] == "MAS":
            count +=1
            if log: print(f"Up-Right at ({r},{c}): X{input[r-1][c+1] + input[r-2][c+2] + input[r-3][c+3]}")
    except: pass

    # Right
    try:
        if c < len(input[0]) - 3 and input[r][c+1] + input[r][c+2] + input[r][c+3] == "MAS":
            count +=1
            if log: print(f"Right at ({r},{c}): X{input[r][c+1] + input[r][c+2] + input[r][c+3]}")
    except: pass

    # Down-Right
    try:
        if r < len(input) - 3 and c < len(input[0]) - 3 and input[r+1][c+1] + input[r+2][c+2] + input[r+3][c+3] == "MAS":
            count +=1
            if log: print(f"Down-Right at ({r},{c}): X{input[r+1][c+1] + input[r+2][c+2] + input[r+3][c+3]}")
    except: pass

    # Down
    try:
        if r < len(input) - 2 and input[r+1][c] + input[r+2][c] + input[r+3][c] == "MAS":
            count +=1
            if log: print(f"Down at ({r},{c}): X{input[r+1][c] + input[r+2][c] + input[r+3][c]}")
    except: pass

    # Down-Left
    try:
        if r < len(input) - 3 and c > 2 and input[r+1][c-1] + input[r+2][c-2] + input[r+3][c-3] == "MAS":
            count +=1
            if log: print(f"Down-Left at ({r},{c}): X{input[r+1][c-1] + input[r+2][c-2] + input[r+3][c-3]}")
    except: pass

    # Left
    try:
        if c > 2 and input[r][c-1] + input[r][c-2] + input[r][c-3] == "MAS":
            count +=1
            if log: print(f"Left at ({r},{c}): X{input[r][c-1] + input[r][c-2] + input[r][c-3]}")
    except: pass

    # Up-Left
    try:
        if r > 2 and c > 2 and input[r-1][c-1] + input[r-2][c-2] + input[r-3][c-3] == "MAS":
            count +=1
            if log: print(f"Up-Left at ({r},{c}): X{input[r-1][c-1] + input[r-2][c-2] + input[r-3][c-3]}")
    except: pass
    return count


# Main code
def main():
    total = 0
    for r, line in enumerate(input):
        for c, char in enumerate(line):
            if char == "X":
                total += search_at(r, c)
    print("The solution is:",total)

main()
