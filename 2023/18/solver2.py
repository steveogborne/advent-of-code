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
with open("puzzle_input.txt") as file:
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
    # for line in instructions: print(line)

def establish_canvas():
    # collect vertices while tracing instructions
    max_u = 0
    max_l = 0
    max_r = 0
    max_d = 0
    pos = [0,0]
    vertices = [] #  collect outline vertices here
    for line in instructions:
        match line[0]:
            case "U":
                pos[0] -= line[1] # indexes are +ve downwards!
                vertices.append([pos[0],pos[1]])
                if pos[0] < max_u: max_u = pos[0]
            case "L":
                pos[1] -= line[1]
                vertices.append([pos[0],pos[1]])
                if pos[1] < max_l: max_l = pos[1]
            case "R":
                pos[1] += line[1]
                vertices.append([pos[0],pos[1]])
                if pos[1] > max_r: max_r = pos[1]
            case "D":
                pos[0] += line[1] # indexes are +ve downwards!
                vertices.append([pos[0],pos[1]])
                if pos[0] > max_d: max_d = pos[0]

    # canvas stats
    width = max_r - max_l
    height = max_d - max_u
    start_pos = [0 - max_u, 0 - max_l]
    #print(width, height, start_pos,"\n")

    # Adjust all vertices such that canvas origin is at 0-index
    vertices = [[vertex[0]-max_u, vertex[1]-max_l] for vertex in vertices]
    vertices.sort() # sort vertices from top to bottom for scanning

    # Put all vertices of the same line into one list
    line_vertices = []
    current_line = -1
    for vertex in vertices:
        if vertex[0] == current_line:
            line_vertices[-1][-1].append(vertex[1])
        if vertex[0] != current_line:
            line_vertices.append([vertex[0], [vertex[1]]])
            current_line = vertex[0]

    # Check to see if we need branching logic (highly likely!)
    # ...and whether we need neighbour line exceptions (hopefully not!)
    # previous_line_index = 0
    #for line in line_vertices:
        #print(line)
        # if len(line[1])>2: print("Multiple branches here") # yep, many found
        # if previous_line_index == line[0]-1: print("Neighbour line found") # phew, no neighbours

    # For each line turn that list into a start stop map accounting for edges of existing branches
    # target format: line = [row, [col1, col2, ...]]
    line_maps = [line_vertices[0]] # initialise
    #print("\nFirst line in line_maps:",line_maps)

    for index, new_vertices in enumerate(line_vertices[1::]):
        # line_maps.append([line[0], line_maps[-1][1]])
        # print("\n"+"line maps[-1]", line_maps[-1])
        # print("line in line_vertices", line)
        old_vs = line_maps[-1][1].copy()
        #print("old vertices", old_vs)
        extra_list = line_maps[-1][1].copy()
        add_new_line = False
        #print("new vertices", new_vertices)
        #print("new pairs indexes:",list(range(0, len(new_vertices[1])//2)))

        for np in range(0, len(new_vertices[1])//2): # for each actual new pair
            a = new_vertices[1][2*np]
            b = new_vertices[1][2*np+1]
            if a in old_vs and b not in old_vs and old_vs.index(a) %2 == 0:
                #print("index even, a->b (reduce left) (new line)")
                extra_list.append(b)
                extra_list.remove(a)
                extra_list.sort()
                add_new_line = True
                #print("old_vs",old_vs,"extra_line",extra_list)
            elif a in old_vs and b not in old_vs and old_vs.index(a) %2 == 1:
                #print("index odd, a->b (extend right) (same line)")
                old_vs.append(b)
                old_vs.remove(a)
                old_vs.sort()
                #print("old_vs",old_vs,"extra_line",extra_list)
            elif b in old_vs and a not in old_vs and old_vs.index(b) %2 == 0:
                #print("index even, b->a (extend left) (same line)")
                old_vs.append(a)
                old_vs.remove(b)
                old_vs.sort()
                #print("old_vs",old_vs,"extra_line",extra_list)
            elif b in old_vs and a not in old_vs and old_vs.index(b) %2 == 1:
                #print("index odd, b->a (reduce right) (new line)")
                extra_list.append(a)
                extra_list.remove(b)
                extra_list.sort()
                add_new_line = True
                #print("old_vs",old_vs,"extra_line",extra_list)
            elif a in old_vs and b in old_vs and old_vs.index(a) %2 == 0:
                #print("index even, remove a,b (cap branch) (new line)")
                extra_list.remove(a)
                extra_list.remove(b)
                extra_list.sort()
                add_new_line = True
                #print("old_vs",old_vs,"extra_line",extra_list)
            elif a in old_vs and b in old_vs and old_vs.index(a) %2 == 1:
                #print("index odd, remove a,b (join branch) (same line)")
                old_vs.remove(a)
                old_vs.remove(b)
                old_vs.sort()
                #print("old_vs",old_vs,"extra_line",extra_list)
            elif a not in old_vs and b not in old_vs:
                old_vs.extend([a,b])
                old_vs.sort()
                #print(old_vs,"index a =", old_vs.index(a))
                if old_vs.index(a) %2 == 0:
                    continue
                    #print("pair is new branch (same line)")
                    #print("old_vs",old_vs,"extra_line",extra_list)
                elif old_vs.index(a) %2 ==1:
                    #print("pair is split branch (new line)")
                    old_vs.remove(a)
                    old_vs.remove(b)
                    old_vs.sort()
                    extra_list.extend([a,b])
                    extra_list.sort()
                    add_new_line = True
                    #print("old_vs",old_vs,"extra_line",extra_list)
        line_maps.append([new_vertices[0], old_vs])
        if add_new_line: line_maps.append([new_vertices[0]+1, extra_list])
        #print("\nLast line in line_maps:",line_maps[-1])

    # print("line maps", line_maps)
    #print("\n")
    return line_maps

# Functions

# Main code
def main():
    list = establish_canvas()
    total_weight = 0
    line_weight = 0
    last_line = 0
    for line in list:
        line_weight *= line[0] - last_line
        total_weight += line_weight
        line_weight = 0
        for pair in range(0, len(line[1])//2):
            a = line[1][2*pair]
            b = line[1][2*pair+1]
            line_weight += b-a +1
        last_line = line[0]

    # canvas = paint_infill(canvas, start_pos)
    # canvas = output_canvas(canvas, "puzzle_output.txt")
    # area = count_holes(canvas)
    # for line in list: print(line)

    answer = total_weight
    print("The solution is:",answer)

main()
