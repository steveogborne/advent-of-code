# Problem scope
'''
Nonagrams
'''

# Solution sketch
'''
Input file and split into a row string and group list /
Split row by . to give gontiguous regions as a list
Compare the number of lists elements in each
If equal move to the arrangement calculation
If not equal calculate what could go where..?
Scan row and record known groups
Check ordered group matches (set function?)
Find an algorthm for counting arrangements from unkown patterns
Count missing # and . from known # total and given #
Replace ? with # and remaining ? with . Split row by dot - is this equivalent to required set? If yes count it, if not move on!
###

Approach 2 , rather than searching the line for info:
Create as many combinations of the number sequence using the supplied number of #
Find every possible location of each combination C to find total arrangements? (For x in line is [x:x+n:] == C where n = len(C))
e.g. "1" search combinations -> At start: [#., #?,] in middle: [.#.  .?.  ?#. .#?  ?#?] at end: [.#  ?#]
e.g. "2" -> [##.  #?.  ?#.  ??.  ##?  #??  ?#?  ???]
            [.##.  .#?.  .?#.  .??.  .##?  .#??  ?#  .???  ?##.  ?#?.  ??#.  ???.  ?##?  ?#??  ??#?  ????]
            [.##  .#?  .?#  .??  ?##  ?#?  ??#  ???]
Combinations can be 2^n combinations surrounded by 2 combinations at ends and 4 combinations in between.
i.e. (./?)(all combinations of n x (#/?))(./?)

Approach 3. Look for #
Count missing # and . from known # total and given #
Replace ? with # and remaining ? with . Split row by dot - is this equivalent to required set? If yes count it, if not move on!
'''
# Variables
with open("puzzle_input.txt") as file:
    raw_input = file.read().splitlines()

# Remove known "." and split into sections
data = [[[x for x in line.split(" ")[0].split(".") if x], [int(y) for y in line.split(" ")[1].split(",")]] for line in raw_input]

# Create a target row and collect some data
for line in data:
    line.append(["#"*group for group in line[1]]) # target row representation
    # line.append(len(line[1]) - len(line[0])) # number of missing groups G
    miss_func_spr = sum(line[1]) - sum([x.count("#") for x in line[0]]) # number of missing functional springs #
    line.append( miss_func_spr)
    no_unk = sum([x.count("?") for x in line[0]]) # number of unknown conditions ? = count(?)
    line.append(no_unk)
    miss_dam_spr = no_unk - miss_func_spr # Number of missing damaged strings . = (? -#)
    line.append(miss_dam_spr)

# Test on a sample of lines
for index, line in enumerate(data):
    if index < 10: print(line[0],line[1],line[2],line[3],line[4],line[5])

# Functions

# Find the first location a # block can be placed
def place_group(line):
    target_row = line[2]
    for target_group in target_row:
        first_index = 0 ### make this updateable
        if line[0][0][first_index:len(target_group)+1:] == "#"*len(target_group)+"." or line[0][0][:len(target_group)+1:] == "#"*len(target_group)+"?":
            print("fits so far...")


# Main code
def main():
    total_arrangements = 0
    # for line in data:
    #     if len(line[0]) == len(line[1]):
    #         print("Groups match")
    #     else: print("Groups don't match")

    print("The solution is:",total_arrangements)

main()
