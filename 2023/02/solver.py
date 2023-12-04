# Test if game is possible
# Criteria: 12 red cubes, 13 green cubes, 14 blue cubes
# So: fail if r > 12, g > 13, b > 14 on any draw
# Input data to be formatted as gameID, game[set(r, rv, g, gv, b, bv)] perhaps?
# There are not always the same number of sets in a game
# R, G, B are not always drawn
# Number drawn is always behind the word red blue or green,
# so perhaps can do a simple check if index -2 or -3 is a number and compare that number?

score_sheet = open("puzzle_input.txt")
game_list = score_sheet.readlines()
print(game_list[0])
