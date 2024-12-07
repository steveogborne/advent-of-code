# Problem scope
'''
Part 1: Reactor Reports
Input is a list of reports. Reports are a list of numbers.
Reports are safe if numbers gradually increase or decrease.
Gradual = increment between 1 and 3
'''

# Solution sketch
'''
Iterate through report
Logic to check two fail states
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
            if log: print("Unsafe\n")
            return False

    if log: print("Safe\n")
    return True


# Main code
def main():
    count = 0
    for report in input:
        if report_is_safe(report): count +=1

    answer = count
    print("The solution is:",answer)

main()
