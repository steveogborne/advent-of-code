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

# Functions



# Main code
def main():
    answer = "Undefined"
    print("The solution is:",answer)

main()
