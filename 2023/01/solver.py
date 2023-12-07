#! python3

# Read input text from puzzle_input

input_file = open("puzzle_input.txt", "r")
line_list = input_file.readlines()
input_file.close()

#for line in file.readlines():
#    print(line)

# For each line extract the first and last digit and combine into a 2-digit number
# Turn this into a function that can be called over the whole list

def findlinecode(line):
    split_line = []
    for letter in line:
        if letter.isdecimal():
            split_line.append(letter)
    code = int(split_line[0]+split_line[-1])
    return(code)

# Sum all line numbers into a total

code_total = 0
for line in line_list:
    code_total += findlinecode(line)
# print(code_total)


# Have a go a wirting it again but more compact:
with open("puzzle_input.txt") as file:
    total = 0
    for line in file:
        list = [x for x in line if x.isdecimal()]
        total += int(list[0]+list[-1])
print(total)
