# Scratchcards
# Each line contains winning numbers and your numbers
# Find out how many of your numbers match the winning numbers
# Score the game based on doubling your score every winning number

# Step 0 readfile
with open("puzzle_input.txt") as file:
    all_cards = file.read().splitlines()

# print(all_cards[0]) # test

# Step 1 define function to split line into two lists, winning numbers and your numbers

def extract_numbers(line):
    remove_head = line.split(":")[1] # Removes leading "Card x:"
    numbers = [remove_head.split("|")[0].strip().split(" "), remove_head.split("|")[1].strip().split(" ")] # split, cleanup and split
    winning_numbers = [int(x) for x in numbers[0] if x] # removes empty elements and turns strings into integers
    your_numbers = [int(x) for x in numbers[1] if x]

    return(winning_numbers,your_numbers)

print(extract_numbers(all_cards[0])) # test

# Create a score function to return score for x number of matches
def score_matches(matches):
    scores = [0, 1] # 0 matches returns 0 score
    for x in range(9): scores.append(scores[-1]*2) # 10 matches is maximum but there would be no harm in adding more
    return(scores[matches])

# print(score_matches(3)) # test
