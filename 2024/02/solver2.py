# Problem scope
'''
Part 1: Reactor Reports
Input is a list of reports. Reports are a list of numbers (levels).
Reports are safe if numbers gradually increase or decrease.
Gradual = increment between 1 and 3

Part 2: Problem Damper
Reports can tolerate one bad level.
If that one bad level can be removed to create a safe report then it's a pass.
'''

# Solution sketch
'''
Iterate through report
Logic to check two fail states

Part 2:
Either at finding first fail, remove and check.
Or store list of incrememtns and define new logic based on list of increments - didn't work
Or if fail, generate all list of alternatives until a pass is found
'''
# Variables
with open("puzzle_input.txt") as file:
    input = [[int(x) for x in line.split(" ")] for line in file.read().splitlines()]
    # print(input)

# Functions
def report_is_safe(report: list[int], log: bool = None) -> bool:
    if log: print(f"Report {report}")

    if report[0] == report [1]: return False

    increasing = 1
    if report[1] < report [0]: increasing = -1
    if log: print(f"Increasing? {increasing}")

    for index, item in enumerate(report[:-1]):
        inc = increasing*(report[index + 1] - item)
        if log: print(f"Increment at index {index}: {inc}")
        if  inc < 1 or inc > 3:
            if log: print("Potentially unsafe")
            return False

    if log: print("Safe\n")
    return True

def short_report_is_safe(report: list[int], log: bool = None) -> bool:
    for index in range(len(report)):
        short_report = report[:index] + report[index+1:]
        if log: print(f"Short report: {short_report}")
        if report_is_safe(short_report):
            if log: print("Safe short report found\n")
            return True
        if log: print("Unsafe short report")
    if log: print("No safe short report found: Safe\n")
    return False

# Main code
def main():
    count = 0
    for report in input:
        if report_is_safe(report): count +=1
        elif short_report_is_safe(report): count +=1

    answer = count
    print("The solution is:",answer)

main()
