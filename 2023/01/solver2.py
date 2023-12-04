#! python3

# Read input text from puzzle_input

input_file = open("puzzle_input.txt", "r")
line_list = input_file.readlines()
input_file.close()
test_line = line_list[0]

#for line in file.readlines():
#    print(line)

# NEW FEATURE

# Numbers can be spelled out
# Need a way to detect spelled out numbers
# Then convert spelled out numbers to digits
# Then can reuse code

# numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
# Note: no zeroes found in puzzle_input so will omit for now
# Note for later: keeping zero in this list means the list indexes match the numbers!

# Create a list of indexes for each of the numbers found in the line
# line_number_index = []
# for number in numbers:
#     line_number_index.append(test_line.find(number))
# print(line_number_index)

# Find the lowest index
# number_index = -1
# for index in line_number_index:
#     if index == -1:
#         continue
#     elif number_index == -1:
#         number_index = index
#     elif number_index < index:
#         continue
#     else:
#         number_index = index
# print(number_index)

# This feels unweildy, I'm going to change tack

# OPTIMISATION
# If I change to a first in search I can avoid needing to convert all spelled out numbers and converting all lines to digits

def first_digit(line):
    numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for count, character in enumerate(line):
        if character.isdecimal():
            return int(character)
        else:
            for value, number in enumerate(numbers):
                if line.find(number) == count:
                    return value

def last_digit(line):
    rev_line = line[::-1] # Slice string
    rev_numbers = ["orez", "eno", "owt", "eerht", "ruof", "evif", "xis", "neves", "thgie", "enin"]
    for count, character in enumerate(rev_line):
        if character.isdecimal():
            return int(character)
        else:
            for value, rev_number in enumerate(rev_numbers):
                if rev_line.find(rev_number) == count:
                    return value

total = 0
for count, line in enumerate(line_list):
    total += (int(str(first_digit(line))+str(last_digit(line))))

print(total)
