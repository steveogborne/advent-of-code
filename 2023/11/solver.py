# Problem scope
'''
Input is a map of the sky: . is space and # is galaxy
Need to find sum of shortest distance between every pair
Pair distance = sum of index differences in x and y direction
But space has expanded
Every empty row and column needs to double
'''

# Solution sketch
'''
Scan for empty rows and columns, record their indexes
Insert new empty rows and columns at every empty row and column
Produce a list of every galaxy coordinate
For every entry in the list, sum the distance to every other entry in THE REST OF the list
IN THE REST OF to avoid counting pairs twice
Sum of sums should be the answer
'''
# Variables
with open("puzzle_input.txt") as file:
    sky = file.read().splitlines()

    sky_t = [col for col in sky[0]] # initiate all lines in transposed img
    # print(sky_t)
    for index_l, line in enumerate(sky):
        if index_l > 0: # don't repeat the first line
            for index_c, char in enumerate(line):
                sky_t[index_c] +=char


# Functions
def find_empty_lines(image):
    empty_line_indexes = []
    for index, line in enumerate(image):
        if line.find("#") < 0:
            empty_line_indexes.append(index)
    return(empty_line_indexes)

# Main code
def main():
    line_indexes = find_empty_lines(sky)
    column_indexes = find_empty_lines(sky_t)
    answer = [line_indexes, column_indexes]
    print("The solution is:",answer)

main()
