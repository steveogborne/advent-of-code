# Boat races
# Each race is allocated x ms to run
# Boat speed charges 1 mm/s per ms
# Boat speed is constant and travels for y ms where y is x - charge time
# Distance = boat speed * y
# For each race you need to beat the record from puzzle_input
# For each race determine the number of ways to beat the record = z
# Final answer is product of z

# Extract race data
with open("puzzle_input.txt") as file:
    temp = file.read().splitlines()

times = temp[0].split(":")[1].strip().split(" ")
times = [int(i) for i in times if i]
distances = temp[1].split(":")[1].strip().split(" ")
distances = [int(i) for i in distances if i]
races = [[times[x], distances[x]] for x in range(len(times))]
print(races)

# races has structure [[race_time, distance_record], [].. ] for 4 races

# function to calculate distance travelled for charge time, race time
def calc_dist(charge_time,race_time):
    travel_time = race_time - charge_time
    distance = charge_time*travel_time
    return(distance)

# print(calc_dist(2,races[0][0])) # test

# function to compare if distance beats record
def is_win(distance, race_record):
    if distance > race_record: return(True)
    else: return(False)

# print(is_win(calc_dist(2,races[0][0]), races[0][1])) # test

# function to iterate over charge time and count wins
def count_wins(race):
    race_time = race[0]
    race_record = race[1]
    win_count = 0
    for x in range(race_time):
        if(is_win(calc_dist(x, race_time),race_record)):
            win_count += 1
    return(win_count)

# print(count_wins(races[0])) # test

# function to iterate over races and return product of wins
def score_races(races):
    score = 1
    for race in races:
        score *= count_wins(race)
    return(score)

print(score_races(races)) # result
