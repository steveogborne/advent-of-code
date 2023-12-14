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
add functions for tilting w, s, e.
Because the code is set up for tilting north because of the way arrays are indexed...
It probably makes more sense to rotate the image rather than have different code for tilting in each direction.
Run a spin cycle and time it. How long to calculate 1bn cycles?
If possible, run it. If not then I'll need to think about how to solve this differently...
Perhaps some rocks get stuck in a loop and always end up where they started after one spin cycle.
If this were the case, we only need to run the code on rocks that are in a different position to last time.
Run a check to compare old position to new. Store coordinates of all mobile rocks and calculate just them?
'''
# Variables
import time

with open("puzzle_input.txt") as file:
    input = file.read().splitlines()
    platform = [[x for x in l] for l in input]

# Functions
def shift_rocks(image, compass_direction):
    match compass_direction:
        case "N":
            for l_index, line in enumerate(image[::1]):
                for c_index, char in enumerate(line):
                    if char == "O":
                        # print("rock found")
                        shift_index = 0
                        while l_index > shift_index and image[l_index -1 -shift_index][c_index] == "." :
                            # while "not looking over the edge" and "there's a gap": "look at the next row"
                            shift_index += 1 #shift index is shift -1
                        if shift_index > 0:
                            # if "there's a gap at least one away" update image O -> . and .-> O
                            image[l_index][c_index] = "."
                            image[l_index - shift_index ][c_index] = "O"

        case "S":
            for l_index, line in enumerate(image[::-1]):
                for c_index, char in enumerate(line):
                    if char == "O":
                        # print("rock found")
                        shift_index = 0
                        while l_index > shift_index and image[98-l_index+shift_index][c_index] == "." :
                            # while "not looking over the edge" and "there's a gap": "look at the next row"
                            shift_index += 1
                        if shift_index > 0:
                            # if "there's a gap at least one away" update image O -> . and .-> O
                            image[99-l_index][c_index] = "."
                            image[99-l_index+shift_index][c_index] = "O"

    return(image)

def rotate_platform(image):
    # We need to rotate the platform CW if we are to simulate tilting in an ACW order
    # Starting from the bottom line, put that line into the first column... repeat
    new_image = [[] for char in image[0]]
    for line in image[::-1]:
        for c_index, char in enumerate(line):
            new_image[c_index].append(char)
    return(new_image)

def calculate_weight(image):
    total_weight = 0
    max_weight = len(image)
    for l_index, line in enumerate(image):
        for char in (line):
            if char == "O":
                weight = max_weight - l_index
                total_weight += weight
    return(total_weight)


def output_platform_image(image_matrix):
        image_str = ["".join(line) for line in image_matrix]
        with open("platform_output.txt", "w") as file2:
            for line in image_str:
                file2.write(line+"\n")

def spin_cycle(platform):
    start = time.time()
    N_shifted_platform = shift_rocks(platform)
    end = time.time()
    print("Shift platform time is:", end-start)
    start = time.time()
    W_oriented_platform = rotate_platform(N_shifted_platform)
    end = time.time()
    print("Rotate platform time is:", end-start)
    W_shifted_platform = shift_rocks(W_oriented_platform)
    S_oriented_platform = rotate_platform(W_shifted_platform)
    S_shifted_platform = shift_rocks(S_oriented_platform)
    E_oriented_platform = rotate_platform(S_shifted_platform)
    E_shifted_platform = shift_rocks(E_oriented_platform)
    N_oriented_platform = rotate_platform(E_shifted_platform)
    return(N_oriented_platform)

# Main code
def main():
    # platform_spun_once = spin_cycle(platform)
    # Spin cycle takes 0.015s to complete one cycle
    # Shift platform takes 0.0017
    # Rotate platform takes 0.0013

    s_platform = shift_rocks(platform, "S")
    load = calculate_weight(s_platform)
    output_platform_image(s_platform)

    answer = load
    print("The solution is:",answer)

main()
