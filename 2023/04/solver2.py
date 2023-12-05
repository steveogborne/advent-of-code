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

# print(find_matches(cleaned_card(raw_cards[0]))) # test

# Step 3 creates a list where each element conatins: card ID, number of matches, and number of copies.
# Initialise copies to 1 for existing card

tracker = [[cleaned_card(x)[0], find_matches(cleaned_card(x)), 1] for x in raw_cards] # initialise score tracker
# print(tracker[0]) # test

snippet = [x for x in tracker if x[0] <15]
# for x in snippet: print(x)

# Step 4 Iterate over the list to increment copies according to preceeding matches
def copy_cards(tracker):
    # print("Calculating...")
    for index, card in enumerate(tracker):
        if card[1] > 0: # if there are matches...
            # print("Calculating winnings from",card[2],"copies of card",card[0],"by updating next",card[1],"cards by",card[2])
            for x in range(card[1]): # for every x following cards where x is the number of matches...
                if index + x + 1 < len(tracker): # if still in the list
                    # print(x+1,"update card",index+x+2,"'s score from",tracker[index+x+1][2],"to",tracker[index + x + 1][2]+1*card[2])
                    tracker[index + x + 1][2] += 1*card[2]    # update that card's copies value by 1 (you win a copy of it) for every copy of the current card
                # else: print(x+1,"Can't keep updating, end of the list reached, next card")

copy_cards(tracker)

# Step 5 calculate total number of cards

total_score = 0
for card in tracker:
    total_score += card[2]

print(total_score)
