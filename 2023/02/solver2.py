# Find fewest possible cubes per game
# Result (minimum number) will be maximum seen value for each colour across the sets
# Keep track of min_red, min_blue, min_green and iterate over the same data as before
# Game power is product of min_r,g,b
# Finally sum all game powers

input_file = open("puzzle_input.txt", "r")
game_list = input_file.readlines()
input_file.close()

def nested_game_data(game_line):
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

# For a given game structured according to nested_game_data write a function that tests if the game is possible.
def game_is_possible(game, blue_max, red_max, green_max):
    for set in game:
        for draw in set:
            if draw[0] > blue_max and draw[1] == "blue": return False
            elif draw[0] > red_max and draw[1] == "red": return False
            elif draw[0] > green_max and draw[1] == "green": return False
            # else: print("possible so far...")
    return True

# Write a function that finds the max values for each colour
def colour_min(game):
    min_blue = 0 # initialise
    min_red = 0 # initialise
    min_green = 0 # initialise
    for set in game:
        for draw in set:
            if draw[1] == "blue" and draw[0] > min_blue: min_blue = draw[0]
            elif draw[1] == "red" and draw[0] > min_red: min_red = draw[0]
            elif draw[1] == "green" and draw[0] > min_green: min_green = draw[0]
    return(min_blue,min_red,min_green)

# Write a function that returns the power of a given set of cube values
def cube_power(blue,red,green):
    return blue*red*green


# test = colour_min(nested_game_data(game_list[0])[1])
# print(nested_game_data(game_list[0]))
# print(test)

# Write a loop that iterates over the game data, calculates the minimum set, cube power and sums over all games

total = 0

for line in game_list:
    nested_line_data = nested_game_data(line)[1] #  don't need game_ID
    minimum_set = colour_min(nested_line_data)
    power = cube_power(minimum_set[0],minimum_set[1],minimum_set[2])
    total += power

print("Total = " + str(total))
