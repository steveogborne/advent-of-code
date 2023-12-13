# Problem scope
'''
Input is a 2D image. Each pixel is a pipe segment or background.
The image contains connected loops of pipes and also unconnected pieces and background.
Pipes are straight pieces: | and -, and bends: J F, 7, L
There is also a squirrel in one of the loops marked by S
Find the loop the squirrel is in and find the farthest point in the loop from the squirrel.
Puzzle answer is the number of steps around the loop the farthest opint is

Part 2: Find the number of tiles contained within the loop
'''

# Solution sketch
'''
Input shouldn't need any processing /
Run a search to find the squirrel and return it's coordinates /
Write a function that takes the starting coordinate and finds the two connecting pipes. (Do manually?) /
Write a function that takes a current location, a previous location and calculates the next position based on the symbol /
Write a function that steps around the loop keeping track of location and steps take / (this is the above!)
Write a function that runs both stepping functions in opposite directions simoultaneously until they meet at teh same coordinate. /
Return the steps taken as teh answer. /

Part 2: Not entirely sure how to solve this"
Add some lines that, as the looper steps, updates a copy of the map turning the pipes into "@"
I should change the stepper to only move in one direction
Visually inspect the map... Perhaps the answer will be obvious. Probably not.
Search from Top left for @. First P will be a RH turn going clockwise. Use this as the new start point. Go east to go clockwise.
The next step would be to go around the loop again, and this time check the neighbouring tiles on the pipes "inside side" on the "new map"
If the inspected tiles on the new map are not "@" mark them as "I"
This search will bo to the clockwise right hand side as deep as you can go until another @ is reached.
This should fill in all internal areas.
The count all Is

'''

# Variables
with open("puzzle_input.txt") as file:
    pipe_map = file.read().splitlines()

map_paint = [line for line in pipe_map]
map_width = len(pipe_map[0])
map_height = len(pipe_map)
# print(map_width*map_height)

# Coordinates defined as (line, character). So technically: (y, x) for ease of programming.
# Y axis increase DOWN the map! D'oh!

# Functions
def find_start():
    # scan for S return coordinates
    for index_l, line in enumerate(pipe_map):
        for index_c, char in enumerate(line):
            if char == "S": s_loc = [index_l, index_c]
    return(s_loc)

def get_first_pipes(start_loc):
    # scan around S and check pipes to see if they connect
    line = start_loc[0]
    col = start_loc[1]
    first_pipes = []
    # Look North
    if line != 0:
        for pipe in ["7","|","F"]:
            if pipe_map[line-1][col] == pipe:
                first_pipes.append([[line-1, col], "N", 1, pipe_map[line][col]])
    # Look East
    if col != map_width:
        if pipe_map[line][col+1] == "J" or pipe_map[line][col+1] == "-" or pipe_map[line][col+1] == "7":
            first_pipes.append([[line, col+1], "E", 1, pipe_map[line][col]])
    # Look South
    if line != map_height:
        if pipe_map[line+1][col] == "L" or pipe_map[line+1][col] == "|" or pipe_map[line+1][col] == "J":
            first_pipes.append([[line+1, col], "S", 1, pipe_map[line][col]])
    # Look West
    if col != 0:
        if pipe_map[line][col-1] == "F" or pipe_map[line][col-1] == "-" or pipe_map[line][col-1] == "L":
            first_pipes.append([[line, col-1], "W", 1, pipe_map[line][col]])
    # Before starting let's change "S" to it's pipe:
    start_line = list(pipe_map[line])
    start_line[col] = "J"
    pipe_map[line] = "".join(start_line)
    map_paint[line] = "".join(start_line)
    # print("".join(start_line))
    return(first_pipes)

def step_through_pipe(this_pipe):
    line = this_pipe[0][0]
    col = this_pipe[0][1]
    last_move = this_pipe[1]
    step = this_pipe[2]
    next_pipe = []
    # print(line, col, last_move, step, pipe_map[line][col])
    # (Previously moved North)
    if last_move == "N":
        match str(pipe_map[line][col]):
            case "7": next_pipe = [[line, col-1], "W", step+1, pipe_map[line][col]]
            case "|": next_pipe = [[line-1, col], "N", step+1, pipe_map[line][col]]
            case "F": next_pipe = [[line, col+1], "E", step+1, pipe_map[line][col]]
    # (Previously moved East)
    if last_move == "E":
        match str(pipe_map[line][col]):
            case "J": next_pipe = [[line-1, col], "N", step+1, pipe_map[line][col]]
            case "-": next_pipe = [[line, col+1], "E", step+1, pipe_map[line][col]]
            case "7": next_pipe = [[line+1, col], "S", step+1, pipe_map[line][col]]
    # (Previously moved South)
    if last_move == "S":
        match str(pipe_map[line][col]):
            case "L": next_pipe = [[line, col+1], "E", step+1, pipe_map[line][col]]
            case "|": next_pipe = [[line+1, col], "S", step+1, pipe_map[line][col]]
            case "J": next_pipe = [[line, col-1], "W", step+1, pipe_map[line][col]]
    # (Previously moved West)
    if last_move == "W":
        match str(pipe_map[line][col]):
            case "F": next_pipe = [[line+1, col], "S", step+1, pipe_map[line][col]]
            case "-": next_pipe = [[line, col-1], "W", step+1, pipe_map[line][col]]
            case "L": next_pipe = [[line-1, col], "N", step+1, pipe_map[line][col]]
    if next_pipe ==[]: print("Something went wrong at [",line, ",",col, "], with last move:", last_move, "and current pipe:", pipe_map[line][col])
    return(next_pipe)

def get_top_left():
    for il, line in enumerate(map_paint):
        for ic, col in enumerate(line):
            if col == "@": return([il,ic], "N", 0, pipe_map[il][ic])

def fill_in_tiles(current_pipe):
    # print("painting", current_pipe)
    if current_pipe[3] == "|" and current_pipe[1] == "N": # need to add more tiles
        fill_in_loc = [current_pipe[0][0],current_pipe[0][1]+1]
        while map_paint[fill_in_loc[0]][fill_in_loc[1]] != "@":
            new_painted_line = list(map_paint[fill_in_loc[0]])
            new_painted_line[fill_in_loc[1]] = "I"
            map_paint[fill_in_loc[0]] = "".join(new_painted_line)
            # print("on line", fill_in_loc[0], "starting at", current_pipe, "mark", fill_in_loc, "as I")
            fill_in_loc[1]+=1

def output_map(output):
    with open(output, "w") as file:
        for line in map_paint:
            file.write(line+"\n")

# Main code
def main():
    start_loc = find_start()
    current_pipe = get_first_pipes(start_loc)[0] # choose one arbitrarily we only need to go clockwise for the second loop
    print("Starting paint loop at:",start_loc, "move to", current_pipe[0]) #,"move to:")

    # Trace pipe, painting the pipe element "@"
    while current_pipe[0] != start_loc:
        line = current_pipe[0][0]
        col = current_pipe[0][1]
        new_painted_line = list(map_paint[line])
        new_painted_line[col] = "@"
        map_paint[line] = "".join(new_painted_line)
        next_pipe = step_through_pipe(current_pipe)
        current_pipe = next_pipe
    print("Finished painting at:",current_pipe[0], "after", current_pipe[2], "steps")
    output_map("pipe_output.txt") # write map_paint to file for inspection

    # Trace pipe, painting the internals "I"
    current_pipe = get_top_left() # reset current pipe to top left "F"
    new_start_loc = get_top_left()[0] # define fake start location to current location...
    new_start_loc[0] +=1      # moved south 1
    print("Starting fill in loop at:",new_start_loc, "move to", current_pipe[0]) #,"move to:")
    while current_pipe[0] != new_start_loc:
        fill_in_tiles(current_pipe)
        next_pipe = step_through_pipe(current_pipe)
        current_pipe = next_pipe
    print("Finished painting infill, check fill_output to check")
    output_map("fill_output.txt") # write map_paint to file for inspection

    # Count I's
    number_i = 0
    for line in map_paint:
        for col in line:
            if col == "I": number_i += 1
    print("There are",number_i,"internal tiles")

main()
