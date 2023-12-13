# Problem scope
'''
Input is a map of the sky: . is space and # is galaxy
Need to find sum of shortest distance between every pair
Pair distance = sum of index differences in x and y direction
But space has expanded
Every empty row and column needs to double

Part 2: Rather than doubling the empty rows and columns they should be x1,000,000
Calculate the new total distance
'''

# Solution sketch
'''
Scan for empty rows and columns, record their indexes /
Insert new empty rows and columns at every empty row and column /
Produce a list of every galaxy coordinate /
For every entry in the list, sum the distance to every other entry in THE REST OF the list
IN THE REST OF to avoid counting pairs twice
Sum of sums should be the answer

Part 2: Ok we're definitely not going to physically add in the spaces.
Remove the code that does this and replace it with:
Return the indexes of the empty rows
When calculating the pair distances look up how many empty rows and columns there are in between and add 1m for each
'''
# Variables
with open("puzzle_input.txt") as file:
    sky = file.read().splitlines()

def transpose_image(image):
    image_t = [col for col in image[0]] # initiate all lines in transposed img
    # print(sky_t)
    for index_l, line in enumerate(image):
        if index_l > 0: # don't repeat the first line
            for index_c, char in enumerate(line):
                image_t[index_c] +=char
    return(image_t)

# Functions
def find_empty_lines(image):
    empty_line_indexes = []
    for index, line in enumerate(image):
        if line.find("#") < 0:
            empty_line_indexes.append(index)
    return(empty_line_indexes)

def output_image(image):
    with open("expanded_sky.txt", "w") as file:
        for line in image:
            file.write(line+"\n")
    return

# Calculate number of empty lines between point A and B
def get_empty_lines(A, B, line_indexes, column_indexes):
    empty_lines_passed = 0
    line_refs = sorted([A[0], B[0]])
    col_refs = sorted([A[1], B[1]])
    for l_index in range(line_refs[0],line_refs[1]):
        if l_index in line_indexes:
            empty_lines_passed +=1
    for c_index in range(col_refs[0],col_refs[1]):
        if c_index in column_indexes:
            empty_lines_passed +=1
    empty_lines_passed *= 999999
    return(empty_lines_passed)

# Main code
def main():
    # Expand image
    empty_line_indexes = find_empty_lines(sky)
    sky_t = transpose_image(sky)
    empty_column_indexes = find_empty_lines(sky_t)

    # Catalogue galaxies
    galaxy_list = []
    for l_index, line in enumerate(sky):
        for c_index, col in enumerate(line):
            if col == "#": galaxy_list.append([l_index,c_index])
            else: continue

    # Calculate shortest distances
    total_shortest_distance = 0
    for index, galaxy1 in enumerate(galaxy_list):
        for galaxy2 in galaxy_list[index+1::]:
            shortest_distance = abs(galaxy2[1] - galaxy1[1]) + abs(galaxy2[0] - galaxy1[0]) + get_empty_lines(galaxy1, galaxy2, empty_line_indexes, empty_column_indexes)
            total_shortest_distance += shortest_distance

    answer = total_shortest_distance
    print("The solution is:",answer)

main()
