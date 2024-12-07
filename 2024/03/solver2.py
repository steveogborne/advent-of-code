# Problem scope
'''
Part 1 Corrupted code
Extract from the string the instances of text that correspond to the mul function:
mul(X,Y)
Once extracted sum all the multiples

Part 2: Do and don't
Functions that follow do() enable mul instructions
Functions that follow don't() disable mul instructions
They start enabled
'''

# Solution sketch
'''
Clean the string
Do the calc

Part 2
Split the code into do sections
Remove the section code after don't segments
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read()
    # print(input)

# Functions
def mul_vec(pair: list[int]) -> int:
    if len(pair) ==2:
        return pair[0]*pair[1]
    return ValueError

def mul_strip(memory:str) -> str:
    # new_memory = ""
    # for char in memory:
    #     if char in "mul(),0123456789":
    #         new_memory += char

    # print(f"New memory: {new_memory}")
    new_memory = memory.split("mul(")
    # print(f"Length of new memory: {len(new_memory)}")

    new_new_memory = []
    for segment in new_memory:
        if len(segment) > 0 and segment[0] in "0123456789" and "," in segment and ")" in segment:
            # print(segment)
            try: new_new_memory.append([int(x) for x in segment.split(")")[0].split(",")])
            except: pass # print(f"Rejected segment: {segment}")


    # print(f"New new memory: {new_new_memory}")
    # print(f"Length of new new memory: {len(new_new_memory)}")


    final_memory = [pair for pair in new_new_memory if len(pair) == 2]
    # print(f"Final memory: {final_memory}")

    score = sum(map(mul_vec, final_memory))
    # print(f"Number of muls: {len(final_memory)}")
    # print(f"Score: {score}")
    return score



# Main code
def main():
    do_sections = input.split("do()")
    do_segments = [section.split("don't()")[0] for section in do_sections]
    segment_scores = [mul_strip(segment) for segment in do_segments]
    total_score = sum(segment_scores)
    print(f"Strip result: {total_score}")

main()
