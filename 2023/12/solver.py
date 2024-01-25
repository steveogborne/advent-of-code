# Problem scope
'''
Nonagrams
'''

# Solution sketch
'''
Input file and split into a row string and group list /
Split row by . to give contiguous regions as a list
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
# Libraries
from math import factorial
from itertools import combinations

# Variables
with open("puzzle_input.txt") as file:
    raw_input = file.read().splitlines()

# Remove known "." and split into sections
data = [[".".join([x for x in line.split(" ")[0].split(".") if x]), [int(y) for y in line.split(" ")[1].split(",")]] for line in raw_input]

sample_data = data[:10]

# Add some useful stuff to the lines of inputs
for line in data:
    # Create target row representation in line[2]
    line.append(".".join(["#"*group for group in line[1]]))

    # Line stats
    damaged_known = line[0].count("#")
    damaged_target = line[2].count("#")
    damaged_toplace = damaged_target - damaged_known
    gaps = line[0].count("?")

    # Gap indexes
    gap_indexes = [i for i, x in enumerate(line[0]) if x == "?"]
    line.append(gap_indexes) # line[3]

    # How many ways to place r damaged springs in n gaps?
    # Naive combinations: choose r locations from n positions (Does not take into account blocking)
    n = gaps
    r = damaged_toplace
    naive_combinations = int(factorial(n) / factorial(r) / factorial(n-r))

    # Add useful stats to line
    line.append(damaged_toplace) # line[4]
    line.append(gaps) # line[5]
    line.append(naive_combinations) # line[6]

# Functions

# Take an incomplete record, a set of spring placement combinations and a target record
# Return number of correct combinations
def test_placements(combos, field, target):
    field_0 = field # starting string for spring layout
    correct_combinations = 0
    for combo in combos:
        trial_field = field_0
        for index in combo:
            # swap ? for # at index
            trial_field = trial_field[:index]+"#"+trial_field[index+1:]
        # swap remaining ? for .
        trial_field = trial_field.replace("?",".")
        # strip redundant .
        trial_field = ".".join([x for x in trial_field.split(".") if x])
        # test if trial_field matches target
        if trial_field == target:
            correct_combinations = correct_combinations +1
        #     print(trial_field,"is a match")
        # else:
        #     print(trial_field,"is not a match")
    return correct_combinations

# Test on a sample of lines
def test_code():
    for index, line in enumerate(data):
        if index < 1:
            # print(line)
            print(line[0],line[1],line[2],line[3],"--",line[4],"springs in",line[5],"gaps is",line[6],"combinations")
            trial_placements = combinations(line[3], line[4])
            print(test_placements(trial_placements, line[0], line[2]), "combinations fit")

# Main code
def main():
    # test_code()
    total_arrangements = 0
    for line in data:
        trial_placements = combinations(line[3], line[4])
        arrangements = test_placements(trial_placements, line[0], line[2])
        total_arrangements = total_arrangements + arrangements
        print(line[0],line[1],line[2],line[3],"--",line[4],"springs in",line[5],"gaps is",line[6],"potential combinations with", arrangements, "correct arrangements")

    print("The solution is:",total_arrangements)

main()
