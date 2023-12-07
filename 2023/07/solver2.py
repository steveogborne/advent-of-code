# Camel Cards - Joker variant
# Input is a list of hands and wagers
# Score hands by rank over all hands multiplied by their wager
# Final answer is sum of all scroes
# Hands are ranked first by type: 5k, 4k, FH, 3K, 2P, 1P, HC
# For cards of the same type, hands are ranked on highest card, starting from the first card in hand.
# Because of last stage, can't permanently sort hands
# NEW RULE: J are jokers.
# They can be any other card that makes the hand the strongest possible
# They are ranked the lowest when doing 1:1 comparisons

# Solution - part 1
# Perhaps sort lines into sublists of type
#   Create empty lists for types
#   Write a classifier function that identifies type
#   While reading a line from the input, call classifier and append to list
# Within each type list sort order by rank
# Write a scoring function that keeps track of global rank as it iterates over all type lists
# OR concatenate all lists in order and iterate over all items in final list

# Part 2 solution
# Should be able to keep mostly the same
# When hexifying the line J -> 1 so that hands are still alphanumerically sorted correctly
# When classifying the hand need a function or modification that maximises the hand
# If new classification works then all other code should stay the same

def hexify(line):
    # Function that turns hand nomenclature into something that can be alphanumerically sorted
    # returns a string with hand rewritten with T to A ... A to E, except J -> 1
    # >>> hexify("JQKA9 456")
    # "BCDE9 456"
    line_hex = ''
    for char in line:
        match char:
            case "T":
                line_hex += "A"
            case "J":
                line_hex += "1"
            case "Q":
                line_hex += "C"
            case "K":
                line_hex += "D"
            case "A":
                line_hex += "E"
            case _:
                line_hex += char
    return(line_hex)

def classify_hand(hand):
    # Function that takes a hand string and returns a classifier (hand needs to be hexified)
    # Assumes string is length 5
    # >>> classify_hand("AB434")
    # "k2"

    jokers = hand.count("1")
    counts = []
    for char in hand:
        counts.append(hand.count(char))
    counts.sort(reverse=True)
    match counts[0]:
        case 5:
            return("k5") # true regardless of jokers
        case 4:
            if jokers > 0: return("k5") # 4J or 1J upgrade k4 to k5
            else: return("k4")
        case 3:
            match jokers:
                case 0:
                    if counts[3] == 2: return("fh")
                    else: return("k3")
                case 1: return("k4")
                case 2: return("k5")
                case 3:
                    if counts[3] == 2: return("k5")
                    else: return("k4")
        case 2:
            match jokers:
                case 0:
                    if counts[2] == 2: return("p2")
                    else: return("p1")
                case 1:
                    if counts[2] == 2: return("fh") # p2 -> fh
                    else: return("k3") # 1p -> k3
                case 2:
                    if counts[2] == 2: return("k4")
                    else: return("k3")
        case 1:
            if jokers == 0: return("hc")
            else: return("p1")

import bisect

# turns classifier into index for referring to type sublists in hand list
type_key = {
    "hc" : 0,
    "p1" : 1,
    "p2" : 2,
    "k3" : 3,
    "fh" : 4,
    "k4" : 5,
    "k5" : 6
}

#initialise and empty list of lublists for all hand types
ordered_hands = []
for x in type_key: ordered_hands.append([])

# read lines from input text and insert the line into ordered hand according to type sublist and alphanumeric order
with open("puzzle_input.txt") as file:
    # counter = 0 # limit for testing
    for line in file:
        # if counter>5: break # limit for testing
        line_hex = hexify(line.strip())
        classifier = classify_hand(line_hex.split(" ")[0])
        bisect.insort_right(ordered_hands[type_key[classifier]],line_hex)
        # counter+=1 limit for testing

#flatten ordered hands
flat_ordered_hands = [hand for type_sublist in ordered_hands for hand in type_sublist]
# print(flat_ordered_hands) # test

# scoring time! iterate over flat ordered hands
# rank = index + 1
total_score = 0
for index, hand in enumerate(flat_ordered_hands):
    rank = index + 1
    bid = int(hand.split(" ")[1])
    score = rank * bid
    total_score += score
    # print(hand, "with bid", bid, "and rank", rank, "scores", score, "=> New total is", total_score) # test

print(total_score)
