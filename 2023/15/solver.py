# Problem scope
'''
Input is a list of commands
Run the HASH algorithm on the each command
Sum the results to get the answer

HASH:
Determine the ASCII code for the current character of the string.
Increase the current value by the ASCII code you just determined.
Set the current value to itself multiplied by 17.
Set the current value to the remainder of dividing itself by 256.
'''

# Solution sketch
'''
Do what the problem says...
Get input
Split by comma
For each instruction iterate through characters
Convert to ASCII
Maths
Sum
Repeat
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
