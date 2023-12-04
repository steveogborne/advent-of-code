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

#test
print(schematic[0])
