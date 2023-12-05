# Scratchcard 2: mulitplying cards
# Each line contains winning numbers and your numbers
# Find out how many of your numbers match the winning numbers
# For x number of matches create copies of next x cards
# Each copy also creates copies according to it's matches
# I don't actually want to create all copies of the cards, instead lets keep track of matches for each card and copies for each card

# Step 0 readfile
with open("puzzle_input.txt") as file:
    all_cards = file.read().splitlines()

# print(all_cards[0]) # test

# Step 1 define function to split line into two lists, winning numbers and your numbers - reuse

def extract_numbers(line):
    remove_head = line.split(":")[1] # Removes leading "Card x:"
    numbers = [remove_head.split("|")[0].strip().split(" "), remove_head.split("|")[1].strip().split(" ")] # split, cleanup and split
    winning_numbers = [int(x) for x in numbers[0] if x] # removes empty elements and turns strings into integers
    chosen_numbers = [int(x) for x in numbers[1] if x]

    return(winning_numbers,chosen_numbers)

# print(extract_numbers(all_cards[0])) # test

# Step 2 define function to calculate matches for a given winning number and chosen number list - reuse

def find_matches(numbers):
    matches = 0
    for x in numbers[0]:
        if x in numbers[1]:
            matches += 1
    return(matches)

# Step 3 Create a score function to return score for x number of matches - remove
def score_matches(matches):
    scores = [0, 1] # 0 matches returns 0 score
    for x in range(9): scores.append(scores[-1]*2) # 10 matches is maximum but there would be no harm in adding more
    return(scores[matches])

# print(score_matches(3)) # test

# NEW - write a function that creates a list of cards, matches, copies. Iterate over the list to increment copies according to preceeding matches

# Step 4 iterate over all_cards to count matches - modify to count cards

total_score = 0
for card in all_cards:
    score = score_matches(find_matches(extract_numbers(card)))
    total_score += score

print(total_score)
