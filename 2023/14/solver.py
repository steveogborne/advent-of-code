# Problem scope
'''
Puzzle input is an image. . is empty, O are rocks, # are cubes
Rocks can roll and will roll as far as possible until they hit an edge or a cube if the platform is tilted
Rocks add weight to the platform.
The weight is proportional to the distance away from the opposite edge for each rock.
The platform is tilted north. What is the weight on the north support edge
'''

# Solution sketch
'''
Need a function that shifts rocks as far as possible
> Start from the top left, roll rocks until index = 0, or index + 1 has O or #, repeat
Need a function that calculates weight. Weight is a function of line index and each rock can be calculated individually so:
> Iterate over all rocks, add their index_max - index value to a counter
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()
    platform = [[x for x in l] for l in input]

# Functions
def shift_rocks(image, direction):
    if direction == "N":
        for l_index, line in enumerate(image):
            for c_index, char in enumerate(line):
                if char == "O":
                    search_char=0
                    if l_index > 0: search_char=image[l_index -1][c_index]
                    shift_index = 0
                    # print("rock found")
                    while search_char == "." and l_index - shift_index > 0:
                        # print("looking for a space...", shift_index)
                        shift_index += 1
                        search_char = image[l_index-1-shift_index][c_index]
                    # update image O -> . and .-> O
                    if shift_index > 0:
                        image[l_index][c_index] = "."
                        image[l_index - shift_index][c_index] = "O"
    return(image)

def output_platform_image(image_matrix):
        image_str = ["".join(line) for line in image_matrix]
        with open("platform_output.txt", "w") as file2:
            for line in image_str:
                file2.write(line+"\n")


# Main code
def main():
    shifted_platform = shift_rocks(platform, "N")
    output_platform_image(shifted_platform)

    answer = "in the output image for inspection"
    print("The solution is:",answer)

main()
