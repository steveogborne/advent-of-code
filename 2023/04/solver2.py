# Scratchcard 2: mulitplying cards
# Each line contains winning numbers and your numbers
# Find out how many of your numbers match the winning numbers
# For x number of matches create copies of next x cards
# Each copy also creates copies according to it's matches
# I don't actually want to create all copies of the cards, instead lets keep track of matches for each card and copies for each card

# Step 0 readfile
with open("puzzle_input.txt") as file:
    raw_cards = file.read().splitlines()

# print(raw_cards[0]) # test

# Step 1 define function to split line into two lists, winning numbers and your numbers - reuse

def cleaned_card(line):
    card = [int(line.split(":")[0].split(" ")[-1]),                                            # card number
               [int(x) for x in line.split(":")[1].split("|")[0].strip().split(" ") if x],     # winning numbers
               [int(x) for x in line.split(":")[1].split("|")[1].strip().split(" ") if x]]     # chosen numbers
    # Split game/numbers, split winning/chosen, cleanup and split strings into lists
    # ... with empty elements removed and strings turned into integers

    # Return "card" which has format: ["card_ID", ["list of winning numbers"], ["list of chosen numbers"]]
    return(card)

# print(cleaned_card(raw_cards[0])) # test

# Step 2 define function to calculate matches for a given winning number and chosen number list - reuse

def find_matches(card):
    matches = 0
    for x in card[1]:
        if x in card[2]:
            matches += 1
    return(matches)

print(find_matches(cleaned_card(raw_cards[0]))) # test

# NEW - write a function that creates a list of cards, matches, copies. Iterate over the list to increment copies according to preceeding matches
# tracker = [[game(card), find_matches(card), 0] for card in all_cards]

tracker = [(cleaned_card(x)[0], find_matches(cleaned_card(x)), 0) for x in raw_cards]
print(tracker[0])

# Step 4 iterate over all_cards to count matches - modify to count cards

# total_score = 0
# for card in all_cards:
#     score = score_matches(find_matches(extract_numbers(card)))
#     total_score += score

# print(total_score)
