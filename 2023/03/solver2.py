# puzzle_input is a text based "image"
# Step 1 loacate the coordinates of all *
# Step 2 identify * that are gears (touch two numbers)
# Step 3 identify both numbers
# Step 4 calculate and sum "ratios"

# step 0 import file data
with open("puzzle_input.txt") as input:
    schematic = input.read().splitlines()

# step 0B create snippet for testing with
snippet = []
for i in range(3):
    snippet.append(schematic[i])

import re
from string import digits

# Step 1 modify touch function for symbols
# Create touch_number function by modifying touch_symbol function to help with logic in poss_gear_cords
# Touch number will take one signle coordinate (phew! simpler) and check for TWO numbers

def touch_numbers(coordinate, schematic):
    touching = False # unless shown otherwise
    r = coordinate[0] # row coordinate for search +/-1
    c = coordinate[1] # columns coordinates for search +/-1

    # set lower and upper bounds of search box to take into account edges
    r_min = r-1
    r_max = r+1
    c_min = c-1
    c_max = c+1

    # Create a list of coordinates surrounding the gear
    # To avoid duplicates from same number only search in the bounding columns.
    # To avoid duplicates from repeating lines at edges change logic to only include bounding box elements if valid
    # This way max count = 2 and gear when count = 2

    search_coords = []
    if r != 0 and c != 0: search_coords.append([r_min,c_min]) # top left
    if r != 0 and c != len(schematic[0])-1: search_coords.append([r_min,c_max]) # top right
    if c != 0: search_coords.append([r,c_min]) # mid left
    if c != len(schematic[0])-1: search_coords.append([r,c_max]) # mid right
    if r != len(schematic)-1 and c != 0: search_coords.append([r_max,c_min]) # bottom left
    if r != len(schematic)-1 and c != len(schematic[0])-1: search_coords.append([r_max,c_max]) # bottom right

    print(search_coords)
    # Inspect coordinates to see if there are two adjacent numbers
    count = 0
    number_coords = []
    for char in search_coords:
        row = char[0]
        column = char[1]
        symbol = schematic[row][column]
        if symbol.isdecimal():
            number_coords.append([row,column])
            count += 1
        else:
            continue
    print(number_coords)

    power_ratio = 1 # initialise
    # Return logic depending
    if count == 2: return(True, power_ratio)
    else: return(False, 0)

# Step 2 locate * coordinates
# Haha! Can half resuse unused code. Procrastination win!
# Step 2B build in logic to test if * is gear

def gear_search(schematic):
    gear_coords = [] # empty list to fill with coordinates
    power_ratios = [] # empty list to fill with power ratios
    for line_coord, line in enumerate(schematic):
        for char_coord, char in enumerate(line):
            if char == "*":
                gear = touch_numbers([line_coord, char_coord], schematic)
                print(gear)
                if gear[0] == True:
                    print("Gear found at: "+str(line_coord)+", "+str(char_coord)) # test
                    power_ratios.append(gear[1])
                    gear_coords.append([line_coord, char_coord])
                else:
                    print("Star found at: "+str(line_coord)+", "+str(char_coord)+" but not a gear") # test
                    continue
    return(gear_coords, power_ratios)

gears = gear_search(snippet) # test
print(gears)

# Step 3 Identify numbers
# Reference gear coordinate
# Can I use coordinates in extracted numbers to cross reference against coordinates in touch_numbers?
# Brute force it with fresh search?


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

# total = 0 # initialise
# for number in numbers:
#     value = int(number[0])
#     if touch_symbol(number, schematic)[0] == True:
#         total += value
#     else: continue

# print(total)

# Note: corner case what about numbers shared by symbols? Visual inspection I can't see overlap

# test_line = schematic[0]
# line_coordinate = index
