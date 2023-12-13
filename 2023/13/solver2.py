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
def find_mirror(pattern, debug_on):

    # Find potential mirror
    mirror_index = 0
    for l_index, line in enumerate(pattern):
        if l_index>0:
            # Is this line a match for the one before it?
            if line == pattern[l_index-1]: match_test= True
            else: match_test = False
            differences = 0
            if line != pattern[l_index-1]:
                for c_index, char in enumerate(line):
                    if char != pattern[l_index-1][c_index]: differences +=1
            if differences == 1: smudge_test = True
            else: smudge_test = False
            if match_test or smudge_test:
                if debug_on:
                    print("Potential smudged mirror found at", l_index) # test
                # If potential mirror: check mirror
                check_index_L = l_index-2
                check_index_R = l_index+1
                check_limit = len(pattern)-1
                mirror_check = True
                while check_index_L >=0 and check_index_R <= check_limit:
                    #print("Check pair:") # test
                    #print(pattern[check_index_L]) # test
                    #print(pattern[check_index_R]) # test
                    if pattern[check_index_L]!=pattern[check_index_R]:
                        for c_index, char in enumerate(pattern[check_index_L]):
                            if char != pattern[check_index_R][c_index]: differences +=1
                    if differences > 1:
                        mirror_check = False
                        if debug_on and match_test: # test
                            print("...False mirror found at:",l_index)
                        if debug_on and smudge_test:
                            print("...False smudged mirror found at:", l_index)
                        break
                    check_index_L-=1
                    check_index_R+=1
                if differences == 0:
                    mirror_check = False
                    if debug_on: # test
                        print("...Real mirror found at", l_index, "so it is ignored")
                if mirror_check:
                    mirror_index = l_index
                    if debug_on: # test
                        print("...SUCCESS: Smudged mirror found at:", l_index)

    return(mirror_index)

def transpose_pattern(pattern):
    pattern_t = [col for col in pattern[0]] # initiate all lines in transposed pattern
    # print(pattern_t)
    for index_l, line in enumerate(pattern):
        if index_l > 0: # don't repeat the first line
            for index_c, char in enumerate(line):
                pattern_t[index_c] +=char
    return(pattern_t)

def score_pattern(pattern, debug_on):

    # Then check for mirrors as before (if needed?)
    if debug_on:
        print("\nChecking the following pattern for horizintal mirrors:") # test
        # for line in pattern: print(line) # test
    h_score = 100* find_mirror(pattern, debug_on)
    #h_score = [100*x for x in h_score]
    if debug_on:
        print("This pattern scores:", h_score)
        #if len(h_score)>1: print("multi mirror here")

    pattern_t = transpose_pattern(pattern)
    if debug_on:
        print("\nChecking the transpose pattern for 'vertical' mirrors:") # test
        #for line in pattern_t: print(line) # test
    v_score = find_mirror(pattern_t, debug_on)
    if debug_on:
        print("\nThis pattern scores:", v_score)
    #if len(h_score)>1: print("multi mirror here!")
    #return(sum(h_score)+sum(v_score))
    return(h_score+v_score)

# Main code
def main():
    total_score = 0
    debug_on = 0
    full_search = 1
    for index, pattern in enumerate(patterns):
        if full_search or index >= 0 and index <=3:
            pattern_score = score_pattern(pattern, debug_on)
            if pattern_score == 0: print("ERROR at pattern", index)
            total_score += pattern_score
    answer = total_score
    print("The solution is:",answer)

main()
