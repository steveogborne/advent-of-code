# Problem scope
'''
Part 1: "Focus the reflector"
Puzzle input is an image. . is empty, O are rocks, # are cubes
Rocks can roll and will roll as far as possible until they hit an edge or a cube if the platform is tilted
Rocks add weight to the platform.
The weight is proportional to the distance away from the opposite edge for each rock.
The platform is tilted north. What is the weight on the north support edge

Part 2: "Spin cycle"
The platform is tilted north, west, south, east. This is one spin cycle.
Run the spin cycle 1,000,000,000 times
What is the load on the north support beam?
'''

# Solution sketch
'''
Need a function that shifts rocks as far as possible
> Start from the top left, roll rocks until index = 0, or index + 1 has O or #, repeat
Need a function that calculates weight. Weight is a function of line index and each rock can be calculated individually so:
> Iterate over all rocks, add their index_max - index value to a counter

Part 2:
add functions for tilting w, s, e. Run a spin cycle and time it. How long to calculate 1bn cycles?
If possible, run it. If not then I'll need to think about how to solve this differently...
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

def calculate_weight(image, direction):
    total_weight = 0
    if direction == "N":
        max_weight = len(image)
        for l_index, line in enumerate(image):
            for c_index, char in enumerate(line):
                if char == "O":
                    weight = max_weight - l_index
                    total_weight += weight
    return(total_weight)


def output_platform_image(image_matrix):
        image_str = ["".join(line) for line in image_matrix]
        with open("platform_output.txt", "w") as file2:
            for line in image_str:
                file2.write(line+"\n")


# Main code
def main():
    shifted_platform = shift_rocks(platform, "N")
    # output_platform_image(shifted_platform)
    load = calculate_weight(shifted_platform, "N")

    answer = load
    print("The solution is:",answer)

main()
