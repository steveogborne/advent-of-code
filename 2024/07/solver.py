# Problem scope
'''
Input lines are of the format X: a b c ...
X is the output of the calculation. a, b, c etc are input values
The operators + and * can be used in the calculation in any order.
Output is calculated by computing in order (not using precedence)
For each line that has a solution add the output to a running total. The solution is the final sum.
'''

# Solution sketch
'''
Parse input to give list of inputs and an output
Write a function to take a list of inputs, a list of operators and calculates an output
Write a recursive binary tree traversal algorithm to explore all the possible sums and halt when one that matches the out put is true
Write an iterator that loops over the lines an adds up the final answer
'''
# Variables
with open("test_input.txt") as file:
    input = file.read().splitlines()

# Functions
def solveCalculation(input: list, operators: list) -> int:
    ...
    return 0

def parseLine(line: str) -> tuple[int, list]:
    test_value = int(line.split(":")[0])
    numbers = [int(number) for number in (line.split(":")[1].split(" "))]
    return test_value, numbers

# Main code
def main():
    for line in input:
        test_value, numbers = parseLine(line)
        print(f"{test_value}: {numbers}")
    answer = "Undefined"
    print("The solution is:",answer)

main()
