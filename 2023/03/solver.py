# puzzle_input is a text based "image"
# Step 1 loacate all the symbols (2D coordinates)
# Step 2 identify all numbers that "touch" the symbol (vert, horiz and diag) (coord +/-1)
# Step 3 sum all numbers
# Inspecting the puzzle_input the symbols are: [+,-,=,/,*,#,$,%,@,&]
# Can check the above by removing all . and numbers if necessary

# step 0 import file data
input = open("puzzle_input.txt")
schematic = input.readlines()
input.close()

symbols = ['+', '-', '=', '/', '*', '#', '$', '%', '@', '&']

import re
from string import digits

def reduce_to_symbol(thing):
    reduced_schematic = []
    remove_digits = str.maketrans('', '', digits)
    for line in thing:
        new_line = line.replace(".","")
        new_line = new_line.translate(remove_digits)
        reduced_schematic.append(new_line)
    return(reduced_schematic)

snippet = reduce_to_symbol(schematic)
snippet_out = ""
for i in snippet:
    snippet_out += i -"/n"
print(snippet_out)

# test_line = schematic[0]
# line_coordinate = index
