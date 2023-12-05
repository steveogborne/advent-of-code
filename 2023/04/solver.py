# Scratchcards
# Each line contains winning numbers and your numbers
# Find out how many of your numbers match the winning numbers
# Score the game based on doubling your score every winning number

# Step 0 readfile

with open("puzzle_input.txt") as file:
    all_cards = file.read().splitlines()

print(all_cards[0])
