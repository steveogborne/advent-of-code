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
    rocks = [[li, ci] for li, ln in enumerate(platform) for ci, ch in enumerate(ln) if ch == "O"]
    [rocks[index].append(index) for index in range(len(rocks))]
    cubes_in_rows = [[[li,ci] for ci,ch in enumerate(ln) if ch=="#"] for li,ln in enumerate(platform)]
    # for x in cubes_in_rows: print(x)


# Functions
def shift_rocks_NS(image, direction):
    match direction:
        case "N":
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
        case "S":
            for l_index, line in enumerate(reversed(image)):
                for c_index, char in enumerate(line):
                    if char == "O":
                        # print("rock found")
                        shift_index = 0
                        while l_index > shift_index and image[len(image) -l_index+shift_index][c_index] == "." :
                            # while "not looking over the edge" and "there's a gap": "look at the next row"
                            shift_index += 1 #shift index is shift -1
                        if shift_index > 0:
                            # if "there's a gap at least one away" update image O -> . and .-> O
                            image[len(image)-1 - l_index][c_index] = "."
                            image[len(image)-1 - l_index + shift_index ][c_index] = "O"
    return(image)
    # Shift rocks NS takes 0.0017

def shift_rocks_EW(image, direction):
    match direction:
        case "E": return [list("#".join([string.count(".")*"."+string.count("O")*"O" for string in str(line).split("#")])) for line in image ]
        case "W": return [list("#".join([string.count("O")*"O"+string.count(".")*"." for string in str(line).split("#")])) for line in image]
    # Runs in < 0.001s -- faster than matrix manipulation but only ~x2 faster
    # Much more compact though!


def rotate_platform(image):
    # We need to rotate the platform CW if we are to simulate tilting in an ACW order
    # Starting from the bottom line, put that line into the first column... repeat
    new_image = [[] for char in image[0]]
    for line in reversed(image):
        for c_index, char in enumerate(line):
            new_image[c_index].append(char)
    return(new_image)

def rotate_platform_str(image):
    new_image = ["" for char in image[0]]
    for line in image[::-1]:
        for c_index, char in enumerate(line):
            new_image[c_index]+=char
    return(new_image)

def calculate_weight(image):
    total_weight = 0
    max_weight = len(image)
    for l_index, line in enumerate(image):
        line_count = line.count("O")
        weight = max_weight - l_index
        total_weight += weight*line_count
    return(total_weight)


def output_platform_image(image_matrix, dir):
        image_str = ["".join(line) for line in image_matrix]
        with open(dir, "w") as file2:
            for line in image_str:
                file2.write(line+"\n")

def spin_cycle_A(platform):
    N_shifted_platform = shift_rocks_NS(platform, "N")
    W_oriented_platform = rotate_platform(N_shifted_platform)
    W_shifted_platform = shift_rocks_NS(W_oriented_platform, "N")
    S_oriented_platform = rotate_platform(W_shifted_platform)
    S_shifted_platform = shift_rocks_NS(S_oriented_platform, "N")
    E_oriented_platform = rotate_platform(S_shifted_platform)
    E_shifted_platform = shift_rocks_NS(E_oriented_platform, "N")
    N_oriented_platform = rotate_platform(E_shifted_platform)
    return(N_oriented_platform)
    # Spin cycle 1 takes 0.015s to complete one cycle
    # Spin cycle A now takes 0.97s for 100 cycles
    # Load after 100 cycles 100680

def spin_cycle_B(platform):
    N_platform = shift_rocks_NS(platform, "N")
    W_platform = shift_rocks_EW(N_platform, "W")
    S_platform = shift_rocks_NS(W_platform, "S")
    E_platform = shift_rocks_EW(S_platform, "E")
    return(E_platform)
    # Spin cycle B takes 0.70s for 100 cycles
    # Load after 100 cycles 100680

def spin_cycle_C(platform):
    # Shift North
    for l_index, line in enumerate(platform):
        for c_index, char in enumerate(line):
            if char == "O":
                # print("rock found")
                shift_index = 0
                while l_index > shift_index and platform[l_index -1 -shift_index][c_index] == "." :
                    # while "not looking over the edge" and "there's a gap": "look at the next row"
                    shift_index += 1 #shift index is shift -1
                if shift_index > 0:
                    # if "there's a gap at least one away" update platform O -> . and .-> O
                    platform[l_index][c_index] = "."
                    platform[l_index - shift_index ][c_index] = "O"
    # Shift West
    platform = [list("#".join([string.count("O")*"O"+string.count(".")*"." for string in "".join(line).split("#")])) for line in platform]
    # Shift South
    for l_index, line in enumerate(reversed(platform)):
        for c_index, char in enumerate(line):
            if char == "O":
                # print("rock found")
                shift_index = 0
                while l_index > shift_index and platform[len(platform) -l_index +shift_index][c_index] == "." :
                    # while "not looking over the edge" and "there's a gap": "look at the next row"
                    shift_index += 1 #shift index is shift -1
                if shift_index > 0:
                    # if "there's a gap at least one away" update platform O -> . and .-> O
                    platform[len(platform) -1 -l_index][c_index] = "."
                    platform[len(platform) -1 -l_index +shift_index ][c_index] = "O"
    # Shift East
    return [list("#".join([string.count(".")*"."+string.count("O")*"O" for string in "".join(line).split("#")])) for line in platform]
    # 0.61s for 100 cycles
    # Load after 100 cycles is 100680

def spin_cycle_D(platform):
    platform_rW = rotate_platform_str(platform)
    platform_sN = ["#".join([string.count(".")*"."+string.count("O")*"O" for string in line.split("#")]) for line in platform_rW]
    platform_rS = rotate_platform_str(platform_sN)
    platform_sW = ["#".join([string.count(".")*"."+string.count("O")*"O" for string in line.split("#")]) for line in platform_rS]
    platform_rE = rotate_platform_str(platform_sW)
    platform_sS = ["#".join([string.count(".")*"."+string.count("O")*"O" for string in line.split("#")]) for line in platform_rE]
    platform_rN = rotate_platform_str(platform_sS)
    platform_sE = ["#".join([string.count(".")*"."+string.count("O")*"O" for string in line.split("#")]) for line in platform_rN]
    return platform_sE
    # 0.72s for 100 cycles
    # Load after 100 cycles 100680

def check_difference(prev_image, cur_image):
    differences = 0
    diff_image = cur_image.copy()
    for l_index, line in enumerate(prev_image):
        for c_index, char in enumerate(line):
            if char != cur_image[l_index][c_index]:
                differences += 1
                diff_image[l_index][c_index] = "X"
    return(differences, diff_image)

def find_all(line, char):
    start = 0
    while True:
        start = line.find(char, start)
        if start == -1: return
        yield start
        start += 1

# Main code
def main():
    new_platform = platform.copy()
    y=100
    for x in range(y):
        new_new_platform = spin_cycle_D(new_platform)
        # weight = calculate_weight(new_new_platform)
        # if x>0 and x%(y-1) == 0:
        #     diff = check_difference(new_platform, new_new_platform)
        #     output_platform_image(diff[1], "diff_platform_output.txt")
        #     print("Spin",x,"differences",diff[0], "weight", weight)
        new_platform = new_new_platform

    # Rotate platform takes 0.0013
    # Therefore don't run 1,000,000,000 iterations!

    load = calculate_weight(new_platform)
    output_platform_image(new_platform, "platform_output_D.txt")

    answer = load
    print("The solution is:",answer)
start = time.time()
main()
end = time.time()
print("Time elapsed for 100 cycles:",end-start)
