# Problem scope
'''
Digging a lagoon
Each line in puzzle input is a dig instruction with direction, distance and side wall colour
Create a map of the dig site. "." is level ground. "#" is a dug hole
Start with the outline as specified by the dig instructions
Fill in the outline with dug holes
Count the dug holes
'''

# Solution sketch
'''
Use the directions and distances to calculate canvas size /
Create canvas /
Output to file
Trace outline by following instructions
Fill inside using fill algorithm from chasing metal squirrels or something else
'''
# Variables
with open("test_input.txt") as file:
    input = file.read().splitlines()
    instructions = [[ line.split(" ")[0] , int(line.split(" ")[1]) , line.split(" ")[2][1:-1:] ] for line in input]
    # for line in instructions: print(line)

# Establish_canvas
    canvas_u = 0
    canvas_l = 0
    canvas_r = 0
    canvas_d = 0
    pos = [0,0]
    for line in instructions:
        match line[0]:
            case "U":
                pos[1] -= line[1] # indexes are +ve downwards!
                if pos[1] < canvas_u: canvas_u = pos[1]
            case "L":
                pos[0] -= line[1]
                if pos[0] < canvas_l: canvas_l = pos[0]
            case "R":
                pos[0] += line[1]
                if pos[0] > canvas_r: canvas_r = pos[0]
            case "D":
                pos[1] += line[1] # indexes are +ve downwards!
                if pos[1] > canvas_d: canvas_d = pos[1]
    # print(pos) # check return to start
    # print(canvas_u, canvas_l, canvas_r, canvas_d) # observe max deltas from start in all directions
    width = canvas_r - canvas_l
    height = canvas_d - canvas_u
    start_pos = [0 - canvas_u, 0 - canvas_l] # set start point such that canvas origin is at 0-index
    # print(width, height, start_pos)

    canvas = [["." for x in range(width+1)] for y in range(height+1)]
    # for line in canvas: print("".join(line))

# Functions

def output_canvas(canvas, dir):
        with open(dir, "w") as file2:
            for line in canvas:
                file2.write("".join(line)+"\n")

# Main code
def main():
    output_canvas(canvas, "puzzle_output.txt")
    answer = "Undefined"
    print("The solution is:",answer)

main()
