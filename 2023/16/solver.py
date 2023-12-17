# Problem scope
'''
Laser mirrors
Input is an image. . is empty tile, \ and / are 90-degree reflecting mirrors and | and - are splitters.
Beam enters top left going left
A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it
How many tiles are being energised
'''

# Solution sketch
'''
Get input
Need a function to step through the beam's path(s) depending on what is on a particular tile.
> Perhaps a vector so we can count all split beams as we go.
Need a function that updates an image of energised tiles (or otherwise tracks energised tiles)
Need a function that counts energised tiles
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
