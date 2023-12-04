# puzzle_input is a text based "image"
# Step 1 loacate all the symbols (2D coordinates)
# Step 2 identify all numbers that "touch" the symbol (vert, horiz and diag) (coord +/-1)
# Step 3 sum all numbers
# Inspecting the puzzle_input the symbols are: [+,-,=,/,*,#,$,%,@,&]
# Can check the above by removing all . and numbers if necessary

# step 0 import file data
with open("puzzle_input.txt") as input:
    schematic = input.read().splitlines()

# step 0B create snippet for testing with
snippet = []
for i in range(10):
    snippet.append(schematic[i])

# List of symbols in case it will be useful...

symbols = ['+', '-', '=', '/', '*', '#', '$', '%', '@', '&']

import re
from string import digits

# Distraction... Test function to strip file down to symbols to check symbols used

def reduce_to_symbol(thing):
    reduced_schematic = []
    remove_digits = str.maketrans('', '', digits)
    for line in thing:
        new_line = line.replace(".","")
        new_line = new_line.translate(remove_digits)
        reduced_schematic.append(new_line)
    return(reduced_schematic)

# Step 1 locate symbol coordinates
# Step 1A for each coordinate (line, index) check if symbol
# Perhaps check for symbol is easier if check not "." and not "digit"?
# Ok scrap 1A

symbol_coords = [] # empty list to fill with coordinates
for line_coord, line in enumerate(snippet):
    for char_coord, char in enumerate(line):
        if char == "." or char.isdecimal():
            continue
        else:
            symbol_coords.append([line_coord, char_coord])

print(symbol_coords)
# check
print(snippet[1][4])
print(snippet[symbol_coords[0][0]][symbol_coords[0][1]])

# test_line = schematic[0]
# line_coordinate = index
