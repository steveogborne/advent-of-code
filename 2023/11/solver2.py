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
def expand_empty_lines(image):
    empty_line_indexes = []
    new_image = image
    for index, line in enumerate(image):
        if line.find("#") < 0:
            empty_line_indexes.append(index)
    for index in reversed(empty_line_indexes):
        new_image.insert(index, image[index])
    return(new_image)

def output_image(image):
    with open("expanded_sky.txt", "w") as file:
        for line in image:
            file.write(line+"\n")
    return

# Main code
def main():
    # Expand image
    sky_expanded_height = expand_empty_lines(sky)
    sky_expanded_height_t = transpose_image(sky_expanded_height)
    sky_expanded_width = expand_empty_lines(sky_expanded_height_t)
    sky_expanded = transpose_image(sky_expanded_width)
    output_image(sky_expanded)

    # Catalogue galaxies
    galaxy_list = []
    for l_index, line in enumerate(sky_expanded):
        for c_index, col in enumerate(line):
            if col == "#": galaxy_list.append([l_index,c_index])
            else: continue

    # Calculate shortest distances
    total_shortest_distance = 0
    for index, galaxy1 in enumerate(galaxy_list):
        for galaxy2 in galaxy_list[index+1::]:
            shortest_distance = abs(galaxy2[1] - galaxy1[1]) + abs(galaxy2[0] - galaxy1[0])
            total_shortest_distance += shortest_distance

    answer = total_shortest_distance
    print("The solution is:",answer)

main()
