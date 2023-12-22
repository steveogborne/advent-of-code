# Problem scope
'''
Digging a lagoon
Each line in puzzle input is a dig instruction with direction, distance and side wall colour
Create a map of the dig site. "." is level ground. "#" is a dug hole
Start with the outline as specified by the dig instructions
Fill in the outline with dug holes
Count the dug holes

Part 2 the hole is much bigger, what a surprise
The colour code is actually the instruction code
First 5 hexadecimal numbers are teh distance, the last hexadecimal number is the direction:
0 means R, 1 means D, 2 means L, and 3 means U
What is the actual area?
'''

# Solution sketch
'''
Use the directions and distances to calculate canvas size /
Create canvas /
Output to file /
Trace outline by following instructions /
Fill inside using fill algorithm from chasing metal squirrels or something else

Part 2:
Oh well lets start from scratch!
I assuuuuume the map is going to be so big now that computing the outline and fill step by step will take way too long.
Probably need to map corner coordinates. Then calculate infill by doing maths on coordinates line by line
Create new instructions parser
Use instructions to create a list of vertices.
Sort vertices by line
Iterate over canvas height, interpolating fill from vertices
'''
# Variables
with open("test_input.txt") as file:
    input = file.read().splitlines()
    instructions = []
    for line in input:
        direction_int = int(line.split(" ")[2][-2])
        match direction_int:
            case 0: direction = "R"
            case 1: direction = "D"
            case 2: direction = "L"
            case 3: direction = "U"
        distance = int(line.split(" ")[2][2:-2:],16)
        instructions.append([direction, distance])
    for line in instructions: print(line)

def establish_canvas():
    canvas_u = 0
    canvas_l = 0
    canvas_r = 0
    canvas_d = 0
    pos = [0,0]
    canvas = [[0,0]]
    for line in instructions:
        match line[0]:
            case "U":
                pos[1] -= line[1] # indexes are +ve downwards!
                canvas.append([pos[0],pos[1]])
                if pos[1] < canvas_u: canvas_u = pos[1]
            case "L":
                pos[0] -= line[1]
                canvas.append([pos[0],pos[1]])
                if pos[0] < canvas_l: canvas_l = pos[0]
            case "R":
                pos[0] += line[1]
                canvas.append([pos[0],pos[1]])
                if pos[0] > canvas_r: canvas_r = pos[0]
            case "D":
                pos[1] += line[1] # indexes are +ve downwards!
                canvas.append([pos[0],pos[1]])
                if pos[1] > canvas_d: canvas_d = pos[1]
    # print(pos) # check return to start
    # print(canvas_u, canvas_l, canvas_r, canvas_d) # observe max deltas from start in all directions
    width = canvas_r - canvas_l
    height = canvas_d - canvas_u
    start_pos = [0 - canvas_u, 0 - canvas_l] # set start point such that canvas origin is at 0-index
    print(width, height, start_pos)
    for vertice in canvas: print(vertice)
    return canvas, start_pos

# Functions
def paint_outline(canvas, start_pos):
    pos = start_pos
    for line in instructions:
        count = 0
        canvas[pos[0]][pos[1]] = "#"
        while count < line[1]:
            match line[0]:
                case "U": pos[0] -=1
                case "L": pos[1] -=1
                case "R": pos[1] +=1
                case "D": pos[0] +=1
            canvas[pos[0]][pos[1]] = "#"
            # print(pos)
            count +=1
    return canvas

def paint_infill(canvas, start_pos):
    # Visual inspection of test_input and puzzle_input shows that the instructions travel CW around the outline
    # Therefore inside is to the right of up
    pos = start_pos
    for line in instructions:
            count = 0
            while count < line[1]:
                match line[0]:
                    case "U":
                        fill_pos = [pos[0],pos[1]+1]
                        while canvas[fill_pos[0]][fill_pos[1]] != "#":
                            canvas[fill_pos[0]][fill_pos[1]] = "#"
                            fill_pos[1] +=1
                        pos[0] -=1
                        fill_pos = [pos[0],pos[1]+1]
                        while canvas[fill_pos[0]][fill_pos[1]] != "#":
                            canvas[fill_pos[0]][fill_pos[1]] = "#"
                            fill_pos[1] +=1
                    case "L": pos[1] -=1
                    case "R": pos[1] +=1
                    case "D": pos[0] +=1
                # print(pos)
                count +=1
    return canvas

def output_canvas(canvas, dir):
        with open(dir, "w") as file2:
            for line in canvas:
                file2.write("".join(line)+"\n")

def count_holes(canvas):
    count = 0
    for line in canvas:
        count += line.count("#")
    return count

# Main code
def main():
    canvas, start_pos = establish_canvas()
    # canvas = paint_outline(canvas, start_pos)
    # canvas = paint_infill(canvas, start_pos)
    # canvas = output_canvas(canvas, "puzzle_output.txt")
    # area = count_holes(canvas)
    answer = "Undefined"
    print("The solution is:",answer)

main()
