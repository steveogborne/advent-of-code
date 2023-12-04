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
    # This way max count = 2 and gear when count = 2. Actually not true :(

    search_coords = []
    if r != 0 and c != 0: search_coords.append([r_min,c_min]) # top left
    if r != 0 and c != len(schematic[0])-1: search_coords.append([r_min,c_max]) # top right
    if c != 0: search_coords.append([r,c_min]) # mid left
    if c != len(schematic[0])-1: search_coords.append([r,c_max]) # mid right
    if r != len(schematic)-1 and c != 0: search_coords.append([r_max,c_min]) # bottom left
    if r != len(schematic)-1 and c != len(schematic[0])-1: search_coords.append([r_max,c_max]) # bottom right

    # print(search_coords)
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
    # print(number_coords)

    # Return logic depending
    if count >= 2: return(True, number_coords)
    else: return(False, 0)

# Step 2 locate * coordinates
# Haha! Can half resuse unused code. Procrastination win!
# Step 2B build in logic to test if * is gear
#If yes, pass through coordinates associated with part numbers

def gear_search(schematic):
    part_number_coords = [] # empty list to fill with coordinates
    for line_coord, line in enumerate(schematic):
        for char_coord, char in enumerate(line):
            if char == "*":
                gear = touch_numbers([line_coord, char_coord], schematic)
                # print(gear)
                if gear[0] == True:
                    # print("Gear found at: "+str(line_coord)+", "+str(char_coord)) # test
                    part_number_coords.append(gear[1])
                else:
                    # print("Star found at: "+str(line_coord)+", "+str(char_coord)+" but not a gear") # test
                    continue
    return(part_number_coords)

# Reuse extract numbers code to find numbers
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

# Step 3 Function to match part_number_clue to numbers to extract part_number_value

def find_part_number(part_number_clue, numbers):
    for number in numbers:
        if number[1] == part_number_clue[0]:
            if part_number_clue[1] in number[2]:
                return(number[0])

# Step 4 Get clues from gear_search
# Iterate over coordinate clues to find_part_numbers from numbers and return gear ratio
# Deal with corner case of 3 coordinate clues
# Sum ratios to get final answer

part_number_clues = gear_search(schematic)
numbers = extract_numbers(schematic)
ratios = []
ratio_sum = 0
uhohs = 0
for clue_pair in part_number_clues:
    if len(clue_pair) == 2:
        number1 = find_part_number(clue_pair[0], numbers)
        number2 = find_part_number(clue_pair[1], numbers)
        # if number1 == number2: print("Fuck: "+str(clue_pair))
        ratio = int(number1) * int(number2)
        # print("Gear: "+str(clue_pair)+", Gear pair: "+str(number1)+", "+str(number2)+", "+str(ratio))
        if number1 != number2:
            ratios.append(ratio)
            ratio_sum += ratio
        else: print("Dodged that one")
    elif len(clue_pair) >2 :
        number1 = find_part_number(clue_pair[0], numbers)
        number2 = find_part_number(clue_pair[-1], numbers)
        ratio = int(number1) * int(number2)
        #print("Gear: "+str(clue_pair)+", Gear pair: "+str(number1)+", "+str(number2)+", "+str(ratio))
        ratios.append(ratio)
        ratio_sum += ratio
    else:
        uhohs += 1
        print("Uh Oh")

print("Uh Oh's = "+str(uhohs))
print(len(ratios))
print("Ratio Sum is: "+str(ratio_sum))

star_count = 0
for line in schematic:
    for char in line:
        if char == "*": star_count += 1
print(star_count)
