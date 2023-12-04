# Test if game is possible
# Criteria: 12 red cubes, 13 green cubes, 14 blue cubes
# So: fail if r > 12, g > 13, b > 14 on any draw
# Input data to be formatted as gameID, game[set(r, rv, g, gv, b, bv)] perhaps?
# Game ID is also the line index + 1
# There are not always the same number of sets in a game
# R, G, B are not always drawn
# Number drawn is always behind the word red blue or green,
# so perhaps can do a simple check if index -2 or -3 is a number and compare that number?

input_file = open("puzzle_input.txt", "r")
game_list = input_file.readlines()
input_file.close()

def clean_game_data(game_line):
    game = game_line[5:-1] #strip padding "Game " at start and "/n" at end
    game_ID = int(game.split(":")[0]) #string before : is game ID
    raw_game_result = game.split(":")[1] # string after : is game result
    raw_set_results = raw_game_result.split(";") # split raw game results into raw set results according to ;
    game_result = [] # create empty list to recieve cleaned game results
    for set in raw_set_results:
        set_result = set.strip() # clean set results: remove outer spaces
        set_result = set_result.replace(',','') # clean set results: remove commas
        set_result = set_result.split(" ") # turn turn set results string into list of words
        set_result_nested = [] # create empty container for nested draw results
        draws = int(len(set_result)/2) # calculate number of draws in set
        for x in range(draws):
            draw = [] # create empty container for this draw result
            draw.append(int(set_result[2*x])) # append number value to draw result
            draw.append(set_result[(2*x)+1]) # append colour value to draw result
            set_result_nested.append(draw) # append draw result to set result
        game_result.append(set_result_nested) # append list to list of lists
    return(game_ID,game_result)

# example_set_result = [[0, "blue"], [0, "red"], [0, "green"]]
# This is more structure than is required to solve the challenge but maybe it will be needed in part 2 and this is good practice

print(clean_game_data(game_list[0]))

def game_is_possible(game):
    return True
