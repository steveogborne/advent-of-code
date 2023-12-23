# Problem scope
'''
Parts need sorting
Parts have 4 ratings: x,m,a,s. A list of parts to sort is the second half of puzzle input
Parts get sorted through workflows. A list of workflows is the first half of puzzle input
Workflows have rules corresponding to the part ratings and either:
> send the part to another workflow, accept or reject the part.
All parts that are accepted are given a rating which is the sum of their individual ratings
The answer is the sum of all the total ratings of all accpeted parts
'''

# Solution sketch
'''
Turn parts list into list of dictionaries or lists
Turn works flows into list of dictionaries or functions??
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
