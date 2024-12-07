# Problem scope
'''
Part 1 Corrupted code
Extract from the string the instances of text that correspond to the mul function:
mul(X,Y)
Once extracted sum all the multiples
'''

# Solution sketch
'''
Clean the string
Do the calc
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
    print(f"Length of new memory: {len(new_memory)}")

    new_new_memory = []
    for segment in new_memory:
        if len(segment) > 0 and segment[0] in "0123456789" and "," in segment and ")" in segment:
            # print(segment)
            try: new_new_memory.append([int(x) for x in segment.split(")")[0].split(",")])
            except: print(f"Rejected segment: {segment}")


    # print(f"New new memory: {new_new_memory}")
    print(f"Length of new new memory: {len(new_new_memory)}")


    final_memory = [pair for pair in new_new_memory if len(pair) == 2]
    # print(f"Final memory: {final_memory}")

    score = sum(map(mul_vec, final_memory))
    print(f"Number of muls: {len(final_memory)}")
    print(f"Score: {score}")
    return score


def mul_search(memory: str) -> int:
    index = 0
    recording = False
    muls = []
    while index < len(memory):
        if memory[index:index+4] == "mul(":
            recording = True
            index += 4
            first_no = ""
            while memory[index] in "0123456789":
                first_no += memory[index]
                index+=1
            if len(first_no) >0 and memory[index] == ",":
                index+=1
            else:
                index+=1
                recording = False
            second_no = ""
            while memory[index] in "0123456789":
                second_no += memory[index]
                index+=1
            if recording and len(second_no) > 0 and memory[index] == ")":
                index+=1
                muls.append(int(first_no) * int(second_no))
                print(f"mul({first_no},{second_no}) = {muls[-1]}")
            else:
                index+=1
        else:
            index += 1
    print(f"Number of muls: {len(muls)}")
    return sum(muls)


# Main code
def main():
    # search_answer = mul_search(input)
    # print(f"Search result: {search_answer}")
    strip_answer = mul_strip(input)
    print(f"Strip result: {strip_answer}")

main()
