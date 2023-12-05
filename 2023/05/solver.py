# We have a list of seeds and a set of maps
# Extract the seed list and maps
# Write a function to use a map to convert from source to destination
# Write a function to use all maps to convert from seed to location
# Write a function to select the nearest (lowest) location

# with open("puzzle_input.txt") as file:
#     raw_file = file.read().splitlines()

# Turn raw_file into usable tables
# Need a function to create maps. Will use dictionaries to create a structure

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

def process_raw(raw_file):
    with open(raw_file, 'r') as file:
        temp = file.read().split('\n\n')
    seeds = [int(x) for x in temp[0].split(":")[1].strip().split(" ")]
    maps = [create_map(temp[x]) for x in range(len(temp)) if x>0]
    return(seeds, maps)

seeds = process_raw("puzzle_input.txt")[0] # list of seeds
maps = process_raw("puzzle_input.txt")[1] # list of map dictionaries

print(maps[0]["source category"]) # test
