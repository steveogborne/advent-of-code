# Problem scope
'''
Part 1: Crossword
Search the grid for XMAS. It can go up, down, left right and diagonal.

Part 2: X-MAS
Not XMAS, an X made from MASes lol.
'''

# Solution sketch
'''
For every cell check 8 compass points for xmas
Don't search for samx to avoid duplicates
Include precautions for out of bounds

Part 2:
Instead of X search for A.
Instead of searching in star, check 4 diagonals and look for Ms and Ses
Watch out for MAM SAS
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()

# Functions
def check_at(r: int, c:int, log = None) -> int:

    ur = input[r-1][c+1]
    if ur == "A" or ur == "X": return 0

    dr = input[r+1][c+1]
    if dr == "A" or dr == "X": return 0

    dl = input[r+1][c-1]
    if dl == "A" or dl == "X" or dl == ur: return 0

    ul = input[r-1][c-1]
    if ul == "A" or ul == "X" or ul == dr: return 0

    if log: print(f"X-MAS found at {r, c}")
    return 1



# Main code
def main():
    total = 0
    for r, line in enumerate(input[1:-1]):
        for c, char in enumerate(line[1:-1]):
            if char == "A":
                total += check_at(r+1, c+1)
    print("The solution is:",total)

main()
