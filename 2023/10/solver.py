# Problem scope
'''
Input is a 2D image. Each pixel is a pipe segment or background.
The image contains connected loops of pipes and also unconnected pieces and background.
Pipes are straight pieces: | and -, and bends: J F, 7, L
There is also a squirrel in one of the loops marked by S
Find the loop the squirrel is in and find the farthest point in the loop from the squirrel.
Puzzle answer is the number of steps around the loop the farthest opint is
'''

# Solution sketch
'''
Input shouldn't need any processing
Run a search to find the squirrel and return it's coordinates
Write a function that takes the starting coordinate and finds the two connecting pipes. (Do manually?)
Write a function that takes a current location, a previous location and calculates the next position based on the symbol
Write a function that steps around the loop keeping track of location and steps take
Write a function that runs both stepping functions in opposite directions simoultaneously until they meet at teh same coordinate.
Return the steps taken as teh answer.
'''

# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()



# Functions
def find_start(input):
    # scan for S retrun coordinates



# Main code
def main():
    answer = "Undefined"
    print("The solution is:",answer)

main()
