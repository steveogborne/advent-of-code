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
for i in range(3):
    snippet.append(schematic[i])

# List of symbols in case it will be useful...

symbols = ['+', '-', '=', '/', '*', '#', '$', '%', '@', '&'] # Not needed in the end

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

def extract_symbols(schematic):
    symbol_coords = [] # empty list to fill with coordinates
    for line_coord, line in enumerate(snippet):
        for char_coord, char in enumerate(line):
            if char == "." or char.isdecimal():
                continue
            else:
                symbol_coords.append([line_coord, char_coord])
# Not needed in end

# Step 2A List all numbers with their coordinates.
# number object has data structure [value, row_index, column_indexes]
# solumn_indexes will have multiple values according to digits in the number

def extract_numbers(schematic):
    numbers = [] # initialise
    flag = 0 # initialise a flag to keep track of if "inside number"
    for line_coord, line in enumerate(schematic):
        for char_coord, char in enumerate(line):
            if char.isdecimal():
                if flag == 0:
                    numbers.append([char, line_coord, [char_coord]])
                    flag = 1
                elif flag == 1:
                    numbers[-1][0] += char
                    numbers[-1][2].append(char_coord)
            else:
                flag = 0 # OMG took me ages to spot == error
    return(numbers)

# Step 2B Write a function to check if number touches a symbol
# I'll give it the number to search around and the schematic to search in
def touch_symbol(number, schematic):
    value = int(number[0]) # to return if touching, 0 if not
    touching = False # unless shown otherwise
    r = number[1] # row coordinate for search +/-1
    cs = number[2] # columns coordinates for search +/-1

    # set lower and upper bounds of search box to take into account edges
    if r == 0: r_min = 0
    else: r_min = r-1
    # print("R_min is: "+str(r_min))
    if r == len(schematic)-1: r_max = len(schematic)-1
    else: r_max = r+1
    # print("R_max is: "+str(r_max))
    if cs[0] == 0: c_min = 0
    else: c_min = cs[0]-1
    # print("C_min is: "+str(c_min))
    if cs[-1] == [len(schematic[0])-1]: c_max = len(schematic[0]-1)
    else: c_max = cs[-1]+1
    # print("C_max is: "+str(c_max))

    # Create a list of characters surrounding the number "search_box"
    rowA = schematic[r_min][c_min:c_max+1] # row of characters above number (or through if top)
    rowB = schematic[r][c_min:c_max+1] # row of characters though number
    rowC = schematic[r_max][c_min:c_max+1] # row of characters under number (or through if bottom)
    search_box = rowA + rowB + rowC
    # print(search_box)

    #inspect search box to see if there is an adjacent number
    for char in search_box:
        if char == "." or char.isdecimal():
            continue
        else:
            touching = True
            return(touching, value)

    value = 0 # If this part of the loop is reached, no symbol is touching, value is 0
    return(touching, value)

numbers = extract_numbers(schematic)
# print(len(schematic)) # test
# print(len(schematic[0])) # test
# print(numbers[-1]) # test
# print(touch_symbol(numbers[-1], schematic)) # test

# Step 2B Iterate to identify all numbers that touch all symbols
# For all numbers, if touching, add to total

total = 0 # initialise
for number in numbers:
    value = int(number[0])
    if touch_symbol(number, schematic)[0] == True:
        total += value
    else: continue

print(total)

# Note: corner case what about numbers shared by symbols? Visual inspection I can't see overlap

# test_line = schematic[0]
# line_coordinate = index
