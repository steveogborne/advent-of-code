# Problem scope
'''
Part 1: Difference Score
Input is a text file with two lists side by side.
With both lists sorted what is the sum of the sequential differences of the list entries?

Part 2: Similarity Score
For each number in left list how many times is it in teh right list?
Multiply left number by count to get score.
Sum scores to get total
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

def similarity(a: int, b: list) -> int:
    count = 0
    for item in b:
        if item == a: count +=1
    return a*count


# Main code
def main():
    llist = [int(line.split("   ")[0]) for line in input]
    rlist = [int(line.split("   ")[1]) for line in input]

    #llist.sort()
    #rlist.sort()
    #print(llist)
    #print(rlist)

    dsum = sum([similarity(item, rlist) for item in llist])
    #print(dsum)

    answer = dsum
    print("The solution is:",answer)

main()
