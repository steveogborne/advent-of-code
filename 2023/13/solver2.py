# Problem scope
'''
Hidden mirrors
Input is a sequence of rectangular patterns
In each pattern is hidden a (some?) mirrors either vertical or horizontal
Find the mirror line
Output score is number of columns to the left of a vertical miror line (col index) or 100* number of rows above a mirror line
Sum all scores to get the result

Part 2: mirrors now have exactly 1 smudge.
Find the smudge and fix it.
Retrun a score based on the new mirror lines
'''

# Solution sketch
'''
Process input into lists of patterns /
Write a function that scans lines to check equivalency. Once equivalency is found check that equivalency matches other lines above and below
Write a way to do the above with a transposed pattern
Write the score tracker

Part 2:
Write a function that checks for near matches
Will need to check row and columns
Temporarily chnage the smudge and check that it creates a valid mirror
If so return that mirror
The problem seems to imply that we don't score any other reflection lines
'''
# Variables
with open("puzzle_input.txt") as file:
    raw_patterns = file.read().split("\n\n")
    patterns = [pattern.splitlines() for pattern in raw_patterns]
    # for line in patterns[0]: print(line)

# Functions
def fix_smudge(pattern, debug_on):
        # Find potential mirror
    for index, line in enumerate(pattern):
        #print("check line",index) # test
        if index > 0:
            differences = 0
            for c_index, char in enumerate(line):
                if char != pattern[index-1][c_index]: differences +=1
            if differences == 1:
                #print("potential smudged mirror found at", index) # test
                # If potential mirror: check mirror
                check_index_L = index-2
                check_index_R = index+1
                check_limit = len(pattern)-1
                mirror_check = True
                while check_index_L >=0 and check_index_R <= check_limit:
                    #print("Check pair:") # test
                    #print(pattern[check_index_L]) # test
                    #print(pattern[check_index_R]) # test
                    if pattern[check_index_L]!=pattern[check_index_R]:
                        mirror_check = False
                        if debug_on: # test
                            print("\nFalse mirror found at:",index, "on lines", check_index_L)
                            print(pattern[check_index_L], "and", check_index_R)
                            print(pattern[check_index_R])
                        break
                    check_index_L-=1
                    check_index_R+=1
                    if mirror_check:
                        pattern[index] = pattern[index-1] # Fix mirror
                        return(pattern, index)
                    if debug_on: # test
                        print("\nMirror found at:", index)
    return(0) # no smudged mirror found

def find_mirror(pattern, debug_on):

    # Find potential mirror
    mirror_indexes = []
    for index, line in enumerate(pattern):
        #print("check line",index) # test
        if index > 0 and line == pattern[index-1]:
                #print("potential smudged mirror found at", index) # test
                # If potential mirror: check mirror
                check_index_L = index-2
                check_index_R = index+1
                check_limit = len(pattern)-1
                mirror_check = True
                while check_index_L >=0 and check_index_R <= check_limit:
                    #print("Check pair:") # test
                    #print(pattern[check_index_L]) # test
                    #print(pattern[check_index_R]) # test
                    if pattern[check_index_L]!=pattern[check_index_R]:
                        mirror_check = False
                        if debug_on: # test
                            print("\nFalse mirror found at:",index, "on lines", check_index_L)
                            print(pattern[check_index_L], "and", check_index_R)
                            print(pattern[check_index_R])
                        break
                    check_index_L-=1
                    check_index_R+=1
                if mirror_check:
                    mirror_indexes.append(index)
                    if debug_on: # test
                        print("\nMirror found at:", index)

    return(mirror_indexes)

def transpose_pattern(pattern):
    pattern_t = [col for col in pattern[0]] # initiate all lines in transposed pattern
    # print(pattern_t)
    for index_l, line in enumerate(pattern):
        if index_l > 0: # don't repeat the first line
            for index_c, char in enumerate(line):
                pattern_t[index_c] +=char
    return(pattern_t)

def score_pattern(pattern, debug_on):
    # first attempt to fix the mirror if the smudge is on teh mirror line:
    h_score = 0
    v_score = 0
    fixed_pattern = fix_smudge(pattern, debug_on) # Attempt to fix smudge hirizontally
    if fixed_pattern:
        h_score = 100*fixed_pattern[1]
    else:
        pattern_t = transpose_pattern(pattern)
        fixed_pattern_t = fix_smudge(pattern_t, debug_on)
        if fixed_pattern_t:
            v_score = fixed_pattern_t[1]
        else:
            print("Uh-oh no fixed mirrors found")
            print("\nSee this pattern:") # test
            for line in pattern: print(line) # test

    return(h_score+v_score)


    # Then check for mirrors as before (if needed?)
    # if debug_on:
    #     print("\nChecking the following pattern for horizintal mirrors:") # test
    #     for line in pattern: print(line) # test
    # h_score = find_mirror(pattern, debug_on)
    # h_score = [100*x for x in h_score]
    # if debug_on:
    #     print("\nThis pattern scores:", h_score)
    #     if len(h_score)>1: print("multi mirror here")

    # pattern_t = transpose_pattern(pattern)
    # if debug_on:
    #     print("\nChecking the transpose pattern for 'vertical' mirrors:") # test
    #     for line in pattern_t: print(line) # test
    # v_score = find_mirror(pattern_t, debug_on)
    # if debug_on:
    #     print("\nThis pattern scores:", v_score)
    # if len(h_score)>1: print("multi mirror here!")
    # return(sum(h_score)+sum(v_score))

# Main code
def main():
    total_score = 0
    debug_on = False
    for index, pattern in enumerate(patterns):
        if True: # index >= 10 and index <=15:
            pattern_score = score_pattern(pattern, debug_on)
            total_score += pattern_score
    answer = total_score
    print("The solution is:",answer)

main()
