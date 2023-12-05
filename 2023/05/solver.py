# We have a list of seeds and a set of maps
# Extract the seed list and maps
# Write a function to use a map to convert from source to destination
# Write a function to use all maps to convert from seed to location
# Write a function to select the nearest (lowest) location

# Need a function to create maps. Map returned as a dictionary
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

# Function that creates a list of seeds and a list of all maps from raw file
def process_raw(raw_file):
    with open(raw_file, 'r') as file:
        temp = file.read().split('\n\n')
    seeds = [int(x) for x in temp[0].split(":")[1].strip().split(" ")]
    maps = [create_map(temp[x]) for x in range(len(temp)) if x>0]
    return(seeds, maps)

# Function to navigate a given map with a given input and return an output
def navigate_map(source, map):
    # Use of map to translate source to destination
    # 1 find nearest source (when source is in range of source[x] nearest source is source[x])
    # 2 record source offset (source[x] - source)
    # 3 calculate destination (destination[x] + offset)
    if source != "Error":
        for index, source_start in enumerate(map["source range start"]):
            offset = source - source_start
            if offset >= 0 and offset < map["range length"][index]:
                destination = map["destination range start"][index] + offset
                break
            else: destination = source # if no mapping then dest = source
    else: return("Error")

    return(destination)

# debug navigate_map
# map_s2s = process_raw("puzzle_input.txt")[1][0]
# seed = process_raw("puzzle_input.txt")[0][0]
# soil = navigate_map(seed, map_s2s)
# print("for seed", seed, "soil is",soil)

# Function that navigates all maps to translate seed to location
def translate_seed(seed, maps):
    working_location = seed
    for map in maps:
        # print(map["source category"],working_location,"to ",map["destination category"],navigate_map(working_location, map))
        working_location = navigate_map(working_location, map) # luckily maps are in order so don't need to name check sources to destinations!
    if working_location != "Error": location = working_location
    else: location = "Error"
    return(location)

# Solve the problem!
def main():
    seeds = process_raw("puzzle_input.txt")[0] # list of seeds
    maps = process_raw("puzzle_input.txt")[1] # list of map dictionaries
    # test_dest = translate_seed(seeds[0], maps)
    # print(test_dest)

    seed_locations = [[seed for seed in seeds], [translate_seed(seed, maps) for seed in seeds]] # need to define translate_seeds function
    # for x in range(len(seed_locations[0])): print(seed_locations[0][x], seed_locations[1][x]) # check do the seeds change?
    closest_location = min(seed_locations[1])
    closest_seed = seed_locations[0][seed_locations[1].index(closest_location)]
    print("Closest location is", closest_location, "for seed", closest_seed)

main()
