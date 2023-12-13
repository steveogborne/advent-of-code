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
Scan for empty rows and columns, record their indexes /
Insert new empty rows and columns at every empty row and column
Produce a list of every galaxy coordinate
For every entry in the list, sum the distance to every other entry in THE REST OF the list
IN THE REST OF to avoid counting pairs twice
Sum of sums should be the answer
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
            print("empty line found")
            empty_line_indexes.append(index)
    for index in reversed(empty_line_indexes):
        new_image.insert(index, image[index])
        print("line inserted")
    return(new_image)

def output_image(image):
    with open("expanded_sky.txt", "w") as file:
        for line in image:
            file.write(line+"\n")
    return

# Main code
def main():
    print("Expanding height...")
    sky_expanded_height = expand_empty_lines(sky)
    print("transposing_image...")
    sky_expanded_height_t = transpose_image(sky_expanded_height)
    print("Expanding height...")
    sky_expanded_width = expand_empty_lines(sky_expanded_height_t)
    print("transposing_image...")
    sky_expanded = transpose_image(sky_expanded_width)
    print("outputting file...")
    output_image(sky_expanded)
    answer = 0
    print("The solution is:",answer)

main()
