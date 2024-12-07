# Problem scope
'''
Part 1: Print Queue
Input has two sections, page order rules and a list of manual pages
Check the manual pages lists and check they follow rules
If they do find the middle page number and add it to a total
The final total is the answer
'''

# Solution sketch
'''
Parse input

Write a check function
'''
# Variables
with open("puzzle_input.txt") as file:
    rules, manuals = file.read().split("\n\n")

    rules = [[int(x.split("|")[0]),int(x.split("|")[1])] for x in rules.split("\n")]
    rulebook = {}
    for rule in rules:
        try: rulebook[rule[0]].append(rule[1])
        except: rulebook[rule[0]] = [rule[1]]
    # print(f"Rulebook: {rulebook}")

    manuals = [[int(x) for x in line.split(",")] for line in manuals.strip().split("\n")]
    # print(f"Manuals: {manuals}")

# Functions
def check_manual(m: list[int]) -> bool:
    check = True
    prior_pages = []
    for page in m:
        if page in rulebook:
            for rule in rulebook[page]:
                if rule in prior_pages:
                    return False
        prior_pages.append(page)

    return check

def middle_page(manual: list) -> int:
    return manual[(len(manual)-1)//2]

# Main code
def main():
    count = 0
    for manual in manuals:
        if check_manual(manual): count += middle_page(manual)
    print("The solution is:",count)

main()
