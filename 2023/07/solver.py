# Camel Cards
# Input is a list of hands and wagers
# Score hands by rank over all hands multiplied by their wager
# Final answer is sum of all scroes
# Hands are ranked first by type: 5k, 4k, FH, 3K, 2P, 1P, HC
# For cards of the same type, hands are ranked on highest card, starting from the first card in hand.
# Because of last stage, can't permanently sort hands

# Solution
# Perhaps sort lines into sublists of type
#   Create empty lists for types
#   Write a classifier function that identifies type
#   While reading a line from the input, call classifier and append to list
# Within each type list sort order by rank
# Write a scoring function that keeps track of global rank as it iterates over all type lists
# OR concatenate all lists in order and iterate over all items in final list
