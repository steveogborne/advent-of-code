# Boat race- singular!
# Update is one big race rather than one single race
# Race is allocated x ms to run
# Boat speed charges 1 mm/s per ms
# Boat speed is constant and travels for y ms where y is x - charge time
# Distance = boat speed * y
# For the race you need to beat the record from puzzle_input
# For the race determine the number of ways to beat the record = z
# Final answer is z

import os

# Extract race data - modify to create one race entry
with open("puzzle_input.txt") as file:
    temp = file.read().splitlines()

raw_time = temp[0].split(":")[1].strip().split(" ")
time = ""
for i in raw_time:
    if i:
        time += i

raw_distance = temp[1].split(":")[1].strip().split(" ")
dist = ""
for i in raw_distance:
    if i:
        dist += i

race = [int(time), int(dist)]
# print(race)

# function to calculate distance travelled for charge time, race time - same
def calc_dist(charge_time,race_time):
    travel_time = race_time - charge_time
    distance = charge_time*travel_time
    return(distance)

# print(calc_dist(2,races[0][0])) # test

# function to compare if distance beats record - same
def is_win(distance, race_record):
    if distance > race_record: return(True)
    else: return(False)

# print(is_win(calc_dist(2,races[0][0]), races[0][1])) # test

# function to iterate over charge time and count wins - same, can it handle big numbers? no.
# def count_wins(race):
#     race_time = race[0]
#     race_record = race[1]
#     win_count = 0
#     for x in range(race_time):
#         if(is_win(calc_dist(x, race_time),race_record)):
#             win_count += 1
#     return(win_count)

# NEW PLAN Use a binary search to find the minimum and maximum charge time that wins and calculte the range from that
def find_min_charge(race):
    lower_charge = 0 # initialise
    upper_charge = race[1]//2 # initialise
    while upper_charge -lower_charge > 1:
        target_charge = (lower_charge + upper_charge) //2
        if is_win(target_charge, race[1]):
            upper_charge = target_charge
        else: lower_charge = target_charge
        # os.system('cls' if os.name == 'nt' else 'clear')
        # target_range = upper_charge - lower_charge
        # print(target_range, "target range")
    return(upper_charge)

# print(find_min_charge(race))

def find_max_charge(race):
    max_charge = 0
    return(max_charge)

def calc_score(min_charge, max, charge):
    score = 0
    return(score)

race_time = race[0]
record = race[1]
count = 0
for i in range(race_time):
    if i%100000 == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(race_time-i, "remaining")
    if i*(race_time - i) < record: continue
    else: count +=1
print(count)

# print(count_wins(race)) # result

# function to iterate over races and return product of wins - not needed!
# def score_races(races):
#     score = 1
#     for race in races:
#         score *= count_wins(race)
#     return(score)

# print(score_races(races)) # result
