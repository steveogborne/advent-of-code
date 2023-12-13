# Problem scope
'''
Hidden mirrors
Input is a sequence of rectangular patterns
In each pattern is hidden a (some?) mirrors either vertical or horizontal
Find the mirror line
Output score is number of columns to the left of a vertical miror line (col index) or 100* number of rows above a mirror line
Sum all scores to get the result
'''

# Solution sketch
'''
Process input into lists of patterns
Write a function that scans lines to check equivalency. Once equivalency is found check that equivalency matches other lines above and below
Write a way to do the above with a transposed pattern
Write the score tracker
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
