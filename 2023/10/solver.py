# Problem scope
'''
Input is a 2D image. Each pixel is a pipe segment or background.
The image contains connected loops of pipes and also unconnected pieces and background.
Pipes are straight pieces: | and -, and bends: J F, 7, L
There is also a squirrel in one of the loops marked by S
Find the loop the squirrel is in and find the farthest point in the loop from the squirrel.
Puzzle answer is the number of steps around the loop the farthest opint is
'''

# Solution sketch
'''
Input shouldn't need any processing /
Run a search to find the squirrel and return it's coordinates /
Write a function that takes the starting coordinate and finds the two connecting pipes. (Do manually?) /
Write a function that takes a current location, a previous location and calculates the next position based on the symbol /
Write a function that steps around the loop keeping track of location and steps take
Write a function that runs both stepping functions in opposite directions simoultaneously until they meet at teh same coordinate.
Return the steps taken as teh answer.
'''

# Variables
with open("puzzle_input.txt") as file:
    pipe_map = file.read().splitlines()

map_width = len(pipe_map[0])
map_height = len(pipe_map)

# Coordinates defined as (line, character). So technically: (y, x) for ease of programming

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
            if pipe_map[line+1][col] == pipe:
                first_pipes.append([[line+1, col], "N"])
    # Look East
    if col != map_width:
        if pipe_map[line][col+1] == "J" or pipe_map[line][col+1] == "-" or pipe_map[line][col+1] == "7":
            first_pipes.append([[line, col+1], "E"])
    # Look South
    if line != map_height:
        if pipe_map[line-1][col] == "L" or pipe_map[line-1][col] == "|" or pipe_map[line-1][col] == "J":
            first_pipes.append([[line-1, col], "S"])
    # Look West
    if col != 0:
        if pipe_map[line][col-1] == "F" or pipe_map[line][col-1] == "-" or pipe_map[line][col-1] == "L":
            first_pipes.append([[line, col-1], "W"])
    return(first_pipes)

def step_through_pipe(this_loc, last_move):
    # (Previously moved North)
    if last_move == "N":
        match pipe_map[this_loc[0]][this_loc[1]]:
            case "7": next_loc = [[this_loc[0], this_loc[1]-1], "W"]
            case "|": next_loc = [[this_loc[0]+1, this_loc[1]], "N"]
            case "F": next_loc = [[this_loc[0], this_loc[1]+1], "E"]
    # (Previously moved East)
    if last_move == "E":
        match pipe_map[this_loc[0]][this_loc[1]]:
            case "J": next_loc = [[this_loc[0]+1, this_loc[1]], "N"]
            case "-": next_loc = [[this_loc[0], this_loc[1]+1], "E"]
            case "7": next_loc = [[this_loc[0]-1, this_loc[1]], "S"]
    # (Previously moved South)
    if last_move == "S":
        match pipe_map[this_loc[0]][this_loc[1]]:
            case "L": next_loc = [[this_loc[0], this_loc[1]+1], "E"]
            case "|": next_loc = [[this_loc[0]-1, this_loc[1]], "S"]
            case "J": next_loc = [[this_loc[0], this_loc[1]]-1, "W"]
    # (Previously moved West)
    if last_move == "W":
        match pipe_map[this_loc[0]][this_loc[1]]:
            case "F": next_loc = [[this_loc[0]-1, this_loc[1]], "S"]
            case "-": next_loc = [[this_loc[0], this_loc[1]-1], "W"]
            case "L": next_loc = [[this_loc[0]+1, this_loc[1]], "N"]
    return(next_loc)

# Main code
def main():
    start_loc = find_start()
    first_pipes = get_first_pipes(start_loc)
    print("Starting at:",start_loc,"move to:",first_pipes)

main()
