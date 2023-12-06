# We have a list of seeds and a set of maps
# This time the list of seeds is actually a list of seed: range pairs
# Expand the search to find the nearest location for all of these seeds
# Should be able to reuse a lot of code this time. The only problem will be if if the data becomes too unweildy

import os

# Need a function to create maps. Map returned as a dictionary. For part 2 stays the same
def create_map(raw_map):
    # raw_map.split(":")[0].split(" ")[0].split("-") # "input,to,output"
    source_name = raw_map.split(":")[0].split(" ")[0].split("-")[0] # "input"
    destination_name = raw_map.split(":")[0].split(" ")[0].split("-")[2] # "output"
    # print(source_name, destination_name) # test

    source_range_start = [] # init
    destination_range_start = [] # init
    range_length = [] # init

    for line in raw_map.split(":")[1].strip().splitlines(): # "[[xxx yyy zzz], []...]"
        source_range_start.append(int(line.split(" ")[1])) # yyy
        destination_range_start.append(int(line.split(" ")[0])) # xxx
        range_length.append(int(line.split(" ")[2])) # zzz

    map_dict = {
        "source category": source_name,
        "destination category": destination_name,
        "source range start": source_range_start,
        "destination range start": destination_range_start,
        "range length": range_length
    }

    return(map_dict)

# Function that creates a list of seeds and a list of all maps from raw file - Need to modify the seeds list
def process_raw(raw_file):
    with open(raw_file, 'r') as file:
        temp = file.read().split('\n\n') # list of seed string and map table strings
    seed_range_list = [int(x) for x in temp[0].split(":")[1].strip().split(" ")]
    n = 0 # initialise counter
    seeds = [] # initialise seeds
    # append seeds with tuples of seed, range pairs by iterating n by 2 each time to create list of seed, range pairs:
    while n < len(seed_range_list):
        seeds.append((seed_range_list[n], seed_range_list[n + 1]))
        n += 2
    # map list populated by repeatedly calling create_map for each raw map element in temp
    maps = [create_map(temp[x]) for x in range(len(temp)) if x>0]
    return(seeds, maps)

# Function to navigate a given map with a given input and return an output - for part 2 stays the same
# Actually no, need to optimise. Need to return an additoinal value equal to the offset for which we don't need to call this function again
def navigate_map(source, map):
    # Use of map to translate source to destination
    # 1 find nearest source (when source is in range of source[x] nearest source is source[x])
    # 2 record source offset (source[x] - source)
    # 3 calculate destination (destination[x] + offset)
    for index, source_start in enumerate(map["source range start"]):
        offset = source - source_start
        if offset >= 0 and offset < map["range length"][index]: # if source is within range of source start we have a mapping
            destination = map["destination range start"][index] + offset # dest_offset = source_offset therefore dest = dest_start + offset
            available_offset = map["range length"][index] - offset # how far can we keep searching before
            break
        else: # if source is not in any map ranges them mapping is 1:1
            destination = source # if no mapping then dest = source
            available_offset = 1 # and available_offset = 1

    if map["destination category"] == "location":
        location = destination # all locations in destination + available_offset are > location, therefore will not be minimums!
    else: location = 0

    return(destination, location, available_offset)

# debug navigate_map
# map_s2s = process_raw("puzzle_input.txt")[1][0]
# seed = process_raw("puzzle_input.txt")[0][0]
# soil = navigate_map(seed, map_s2s)
# print("for seed", seed, "soil is",soil)

# Function that navigates all maps to translate seed to location - stays the same but:
# Now the function needs to know when the next source call would change the output
def translate_seed(seed, maps): # translates start seed to tree branch
    working_source = seed # start at the beginning
    min_available_offset = max(maps[-1]["range length"]) # maximum possible offset
    for map in maps:
        map_output = navigate_map(working_source, map)
        if map_output[2] < min_available_offset: # map_output[2] = this_available_offset
            min_available_offset = map_output[2] # map_output[2] = this_available_offset
        if map["destination category"] == "location":
            min_location = map_output[1] # map_output[1] = this_min_location
        working_source = map_output[0] # map_output[0] = this_map_destination

    next_seed_offset = min_available_offset
    return(min_location, next_seed_offset)

# Function to find the closest location given a seed, range pair and maps
# When location is calculated for current seed, the translate_seed function will also return
# a value equal to the next seed that will change the location. Thus we can skip all the calls in between
def find_closest(seed, seed_range, maps):
    min_location = 0
    current_seed = seed
    seed_index = 0
    while current_seed <= seed + seed_range:
        result = translate_seed(current_seed, maps)
        if result[0] < min_location or min_location == 0: min_location = result[0]
        next_seed_offset = result[1]
        current_seed += next_seed_offset
        seed_index += next_seed_offset
        if(seed_index%100000 == 0):
            os.system('cls' if os.name == 'nt' else 'clear')
            calculations_remaining = seed_range - seed_index
            print(calculations_remaining, "calculations remaining")
    # for n in range(seed_range):
    #     if n%100000 ==0:
    #         os.system('cls' if os.name == 'nt' else 'clear')
    #         calculations_remaining = seed_range - n
    #         print(calculations_remaining, "calculations remaining")
    #     location = translate_seed(current_seed, seed_range, maps)[0]
    #     if location < closest or closest == 0:
    #         closest = location
    #     else: continue
    return(min_location)


# Solve the problem! - This time rather than calculating a list of seed_locatiosn and using a min function,
# we should keep track of the minimum and compare so that we can compute one seed at a time
def main():
    seeds = process_raw("puzzle_input.txt")[0] # list of seed pairs
    maps = process_raw("puzzle_input.txt")[1] # list of map dictionaries
    # test_dest = translate_seed(seeds[0], maps)
    # print(test_dest)

    # all_seed_minimum = 0
    min_location = find_closest(seeds[1][0], seeds[1][1], maps)
    # for seed in seeds:
    #     min_location = translate_seed(current_seed, maps)
    #     if location < closest or closest == 0:
    #         closest = location
    #     else: continue
    # return(closest)

    print(min_location)
    # keep track of minimum
    # create seed iterator for given seed, range pair
    # then repeat iterator for each seed pair

    # seed_locations = [[seed for seed in seeds], [translate_seed(seed, maps) for seed in seeds]] # need to define translate_seeds function
    # for x in range(len(seed_locations[0])): print(seed_locations[0][x], seed_locations[1][x]) # check do the seeds change?
    # closest_location = min(seed_locations[1])
    # closest_seed = seed_locations[0][seed_locations[1].index(closest_location)]
    # print("Closest location is", closest_location, "for seed", closest_seed)

main()
