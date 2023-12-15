# Problem scope
'''
Input is a list of commands
Run the HASH algorithm on the each command
Sum the results to get the answer

HASH:
Determine the ASCII code for the current character of the string.
Increase the current value by the ASCII code you just determined.
Set the current value to itself multiplied by 17.
Set the current value to the remainder of dividing itself by 256.

Part 2:
There are 256 boxes that can recieve a number of lenses each. Each lens has focus strength 1-9
The instructions are split into two parts
The first part is the lens label (character string)
The HASH of the label is the destination box
The second part is an operation and an optional lens focus number
Operation signified by "-" means remove the lens if it exists from the box
Operation "=" means:
> if a lens with this label exists, swap it for the new lens
> if a lens with this label does not exist then add it to the back of the list
Running all instrucitons:
Add up total focusing power of all lenses for the answer
Focusing power for each lens = (box index +1) * slot index * lens focal length
'''

# Solution sketch
'''
Do what the problem says...
Get input
Split by comma
For each instruction iterate through characters
Convert to ASCII (.encode('ascii'))
Maths
Sum
Repeat

Part 2:
Create a list of boxes where each box is a list of lenses, where each lens is a tuple label and a focus:
[boxes...
    [lenses...
        [lens label 0, focus #], [lens label 1, focus #]...
    ]
]
Fill the boxes using the algorithm
Iterate over all lenses with the maths provided
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read()
    instructions = input.strip().split(",")
    for index, instruction in enumerate(instructions):
        if "=" in instruction:
            instructions[index] = [instruction[:instruction.index("="):], "=", int(instruction[instruction.index("=")+1::])]
        if "-" in instruction:
            instructions[index] = [instruction[:instruction.index("-"):], "-", 0]
    # instructions now in the form ["label", "-/=", 0/focal length]

# Functions

def my_hash(label):
    label_list = list(label.encode('ascii'))
    hash_i = 0
    for char in label_list:
        hash_i += char
        hash_i *= 17
        hash_i = hash_i %256
    return(hash_i)


# Main code
def main():
    boxes = [{} for x in range(256)]
    # box in boxes has structure {lens_label: focus_length, ...}
    total = 0
    for instruction in instructions:
        box_index = my_hash(instruction[0])
        match instruction[1]:
            case "-":
                if instruction[0] in boxes[box_index].keys(): boxes[box_index].pop(instruction[0])
            case "=": boxes[box_index].update({instruction[0]:instruction[2]})

    print(boxes)
    # for instruction in instructions:
    #     total += my_hash(instruction)

    answer = total
    print("The solution is:",answer)

main()
