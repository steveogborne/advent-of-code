# Problem scope
'''
Hidden mirrors
Input is a sequence of rectangular patterns
In each pattern is hidden a (some?) mirrors either vertical or horizontal
Find the mirror line
Output score is number of columns to the left of a vertical miror line (col index) or 100* number of rows above a mirror line
Sum all scores to get the result
'''

# Solution sketch
'''
Process input into lists of patterns /
Write a function that scans lines to check equivalency. Once equivalency is found check that equivalency matches other lines above and below
Write a way to do the above with a transposed pattern
Write the score tracker
'''
# Variables
with open("puzzle_input.txt") as file:
    raw_patterns = file.read().split("\n\n")
    patterns = [pattern.splitlines() for pattern in raw_patterns]
    # for line in patterns[0]: print(line)

# Functions
def find_mirror(pattern, debug_on):

    # Find potential mirror
    mirror_indexes = []
    for index, line in enumerate(pattern):
        #print("check line",index) # test
        if index > 0 and line == pattern[index-1]:
            #print("potential mirror found at", index) # test
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
    if debug_on:
        print("\nChecking the following pattern for horizintal mirrors:") # test
        for line in pattern: print(line) # test
    h_score = find_mirror(pattern, debug_on)
    h_score = [100*x for x in h_score]
    if debug_on:
        print("\nThis pattern scores:", h_score)
        if len(h_score)>1: print("multi mirror here")

    pattern_t = transpose_pattern(pattern)
    if debug_on:
        print("\nChecking the transpose pattern for 'vertical' mirrors:") # test
        for line in pattern_t: print(line) # test
    v_score = find_mirror(pattern_t, debug_on)
    if debug_on:
        print("\nThis pattern scores:", v_score)
    if len(h_score)>1: print("multi mirror here!")
    return(sum(h_score)+sum(v_score))

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
