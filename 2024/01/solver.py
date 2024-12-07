# Problem scope
'''
Input is a text file with two lists side by side.
With both lists sorted what is the sum of the sequential differences of the list entries?
'''

# Solution sketch
'''
Store entries in lists.
Sort lists
Iterate differences and sum. (zip?)
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()

# Functions
def diff(a: int, b: int) -> int:
    return abs(a-b)


# Main code
def main():
    llist = [int(line.split("   ")[0]) for line in input]
    rlist = [int(line.split("   ")[1]) for line in input]

    llist.sort()
    rlist.sort()

    # dlist = list(map(diff, llist, rlist))
    dsum = sum(map(diff, llist, rlist))
    #print(llist)
    #print(rlist)
    #print(dlist)
    #print(dsum)

    answer = dsum
    print("The solution is:",answer)

main()
