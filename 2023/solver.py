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

# function to calculate distance travelled for charge time, race time

# function to compare if distance beats record

# function to iterate over charge time and count wins

# function to iterate over races and return product of wins
