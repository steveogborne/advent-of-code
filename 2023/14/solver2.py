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
def shift_rocks(image):
    for l_index, line in enumerate(image):
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
        line_count = line.count("O")
        weight = max_weight - l_index
        total_weight += weight*line_count
    return(total_weight)


def output_platform_image(image_matrix):
        image_str = ["".join(line) for line in image_matrix]
        with open("platform_output.txt", "w") as file2:
            for line in image_str:
                file2.write(line+"\n")

def spin_cycle(platform):
    N_shifted_platform = shift_rocks(platform)
    W_oriented_platform = rotate_platform(N_shifted_platform)
    W_shifted_platform = shift_rocks(W_oriented_platform)
    S_oriented_platform = rotate_platform(W_shifted_platform)
    S_shifted_platform = shift_rocks(S_oriented_platform)
    E_oriented_platform = rotate_platform(S_shifted_platform)
    E_shifted_platform = shift_rocks(E_oriented_platform)
    N_oriented_platform = rotate_platform(E_shifted_platform)
    return(N_oriented_platform)

def check_difference(image1, image2):
    differences = 0
    for l_index, line in enumerate(image1):
        for c_index, char in enumerate(line):
            if char != image2[l_index][c_index]:
                differences += 1
    return(differences)

# Main code
def main():
    new_platform = platform.copy()
    for x in range(10000):
        new_new_platform = spin_cycle(new_platform)
        weight = calculate_weight(new_new_platform)
        if x%100 == 0:
            diff = check_difference(new_new_platform, new_platform)
            print("Spin",x,"differences",diff, "weight", weight)
        new_platform = new_new_platform



    # Spin cycle takes 0.015s to complete one cycle
    # Shift platform takes 0.0017
    # Rotate platform takes 0.0013
    # Therefore don't run 1,000,000,000 iterations!

    # load = calculate_weight(platform_spun_once)
    output_platform_image(new_platform)

    #answer = diff
    #print("The solution is:",answer)
start = time.time()
main()
end = time.time()
print("Time elapsed for 100,000 cycles:",end-start)
