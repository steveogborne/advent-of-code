# Problem scope
'''
Part 1: Print Queue
Input has two sections, page order rules and a list of manual pages
Check the manual pages lists and check they follow rules
If they do find the middle page number and add it to a total
The final total is the answer

Part 2: fixing incorrect manuals
If a manual is incorrectly ordered, change it to make it pass
Add up the middle page numbers of all the fixed manuals
'''

# Solution sketch
'''
Parse input
Write a check function

Part 2:
Write a fix manual function
Change the main function to add only fixed manual pages
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

def fix_manual(m: list[int]) -> list[int]:
    fm = [m.pop(0)] # Initialise the fixed manual
    while len(m) > 0: # While there are still pages to check
        index = len(fm) # Set the index to the end of the fixed manual
        while index > 0: # While not at the beginning of the fixed manual
            if m[0] not in rulebook:
                fm.insert(index, m.pop(0)) # If the page isn't in the rulebook then it goes at the end of the fixed manual
                break
            if fm[index-1] in rulebook[m[0]]: #  If the current page in the fixed manual is in the rules for the next page to be added
                index -= 1 # Then check back one page
            else:
                fm.insert(index, m.pop(0)) # Otherwise add page here and
                break # Move on to adding the next page
            if index == 0:
                fm.insert(index, m.pop(0)) # If we get to the beginning of the manual add the page here.

    return fm

def middle_page(manual: list) -> int:
    return manual[(len(manual)-1)//2]

# Main code
def main():
    count = 0
    for manual in manuals:
        if not check_manual(manual):
            count += middle_page(fix_manual(manual))
    print("The solution is:",count)

main()
