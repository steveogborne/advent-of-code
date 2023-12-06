# We have a list of seeds and a set of maps
# This time the list of seeds is actually a list of seed: range pairs
# It will be quicker to start from min location, see if location will trace back to any of the seeds. Once we get a seed match, success
# Need to write an inverse map function
# Need to sort map[-1] according to location
# Perhaps lets bin dictionaries and move to lists for ease...
# Should be able to reuse a lot of code this time. The only problem will be if if the data becomes too unweildy

import os

# Need a function to create maps. Map returned as a dictionary. For part 2 stays the same
def create_map(raw_map):
    # raw_map.split(":")[0].split(" ")[0].split("-") # "input,to,output"
    # source_name = raw_map.split(":")[0].split(" ")[0].split("-")[0] # "input"
    # destination_name = raw_map.split(":")[0].split(" ")[0].split("-")[2] # "output"
    # print(source_name, destination_name) # test
    this_map = []
    for line in raw_map.split(":")[1].strip().splitlines(): # "[[xxx yyy zzz], []...]"
        this_map.append([int(line.split(" ")[1]),    # yyy source_range_start
                    int(line.split(" ")[0]),    # xxx destination_range_start
                    int(line.split(" ")[2])])    # zzz range_length

    return(this_map)

# Function that creates a list of seeds and a list of all maps from raw file - Need to modify the seeds list
def process_raw(raw_file):
    with open(raw_file, 'r') as file:
        temp = file.read().split('\n\n')
    seed_range_list = [int(x) for x in temp[0].split(":")[1].strip().split(" ")]
    n = 0 # initialise counter
    seeds = [] # initialise seeds
    # append seeds with tuples by iterating n by 2 each time:
    while n < len(seed_range_list):
        seeds.append((seed_range_list[n], seed_range_list[n + 1]))
        n += 2
    # map list populated by repeatedly calling create_map for each raw map element in temp
    maps = [create_map(temp[x]) for x in range(len(temp)) if x>0]
    return(seeds, maps)

# Function to navigate a given map with a given input and return an output - for part 2 stays the same
def navigate_map(source, map):
    # Use of map to translate source to destination
    # 1 find nearest source (when source is in range of source[x] nearest source is source[x])
    # 2 record source offset (source[x] - source)
    # 3 calculate destination (destination[x] + offset)
    for line in enumerate(map):
        # source_start = line[0]
        offset = source - line[0]
        if offset >= 0 and offset < line[2]: # range_length = map[2]
            destination = line[1] + offset
            break
        else: destination = source # if no mapping then dest = source

    return(destination)

# debug navigate_map
# map_s2s = process_raw("puzzle_input.txt")[1][0]
# seed = process_raw("puzzle_input.txt")[0][0]
# soil = navigate_map(seed, map_s2s)
# print("for seed", seed, "soil is",soil)

def back_nav_map(destination, map):
    for index, line in enumerate(map):
        # destination_start = line[1]
        offset = destination - line[1]
        if offset >= 0 and offset < line[2]: # range_length = map[2]
            source = line[0] + offset
            break
        else: source = destination # if no mapping then dest = source

    return(source)

# Function that navigates all maps to translate seed to location - stays the same
def translate_seed(seed):
    working_location = seed
    for map in maps:
        # print(map["source category"],working_location,"to ",map["destination category"],navigate_map(working_location, map))
        working_location = navigate_map(working_location, map) # luckily maps are in order so don't need to name check sources to destinations!
    location = working_location
    return(location)

def back_translate_location(location):
    working_source = location
    for map in maps[::-1]:
        working_source = back_nav_map(working_source, map)
    seed = working_source
    return(seed)

# Function to find the closest location given a seed, range pair and maps
def find_closest(seed, seed_range):
    closest = 0
    current_seed = seed
    for n in range(seed_range):
        if n%100000 ==0:
            os.system('cls' if os.name == 'nt' else 'clear')
            calculations_remaining = seed_range - n
            print(calculations_remaining, "calculations remaining")
        location = translate_seed(current_seed, maps)
        if location < closest or closest == 0:
            closest = location
        else: continue
    return(closest)

# Function to check if seed is in seed range
def check_seed(seed):
    for seed_pair in seeds:
        if seed >= seed_pair[0] and seed <= seed_pair[0] + seed_pair[1]:
            # print(seed_pair[0],seed_pair[1],seed_pair[0]+seed_pair[1])
            return(True)
    return(False)

# Function to find smallest destination in map
def min_dest(map):
    min_dest = 99999999999
    for line in map:
        if line[1] < min_dest: min_dest = line[1]
    return(min_dest)

# Function that returns a list of search locations roughly distributed by 10 between given LB and UB
def get_decimated_search_locations(bounds):
    search_location = bounds[0] # initialise
    location_search_breadth = bounds[1]-bounds[0]
    # print(location_search_breadth)
    if(location_search_breadth > 10):
        precision = location_search_breadth//10 # approx divide by 10
        search_locations = []
        while search_location < bounds[1]:
            search_locations.append(search_location)
            search_location += precision
        search_locations.append(bounds[1])
        return(search_locations)
    else: return(bounds)

def binary_search(bounds):
    bound_range = bounds[1]-bounds[0]
    if bound_range <= 1:
        return(bounds, 0)
    else:
        half_way = (bounds[1]+bounds[0])//2 # divide by two plus 1
        print(half_way)
        check_half_way = check_seed(back_translate_location(half_way))
        print(check_half_way)
        if check_half_way:
            return([bounds[0], half_way], 1)
        else: return([half_way, bounds[1]], 1)

def check_search_locations(search_locations):
    checked_locations = [] # initialise
    for location in search_locations:
        check = check_seed(back_translate_location(location))
        checked_locations.append([location, check])
    return(checked_locations)

def get_next_bounds(checked_locations):
    for x in checked_locations:
        if x[1]:
            UB = x[0]
            break
        LB = x[0]
    return([LB, UB])

def hone_in(bounds, print_out):
    search_locations = get_decimated_search_locations(bounds)
    search_locations_checked = check_search_locations(search_locations)
    if(print_out):
        for x in search_locations_checked: print(x)
    bounds = get_next_bounds(search_locations_checked)
    return(bounds)

# Solve the problem! - This time rather than calculating a list of seed_locatiosn and using a min function,
# we should keep track of the minimum and compare so that we can compute one seed at a time

#global variables
seeds = process_raw("puzzle_input.txt")[0] # list of seed pairs
maps = process_raw("puzzle_input.txt")[1] # list of map dictionaries
maps[-1].sort(key = lambda line: line[1])

def main():
    # print(maps[-1][0][1]) # smallest map location entry = 26879537

    # visually inspect if there are any discontinuities between map lines - there are not until map line 9
    # lre_update = maps[-1][0][1]
    # for line in maps[-1]:
    #     location_range_end = line[1]+line[2]
    #     print("start", line[1], "+ range", line[2], "range end:", location_range_end, "gap:", line[1]-lre_update)
    #     lre_update = location_range_end

    # visually inspect what line transtions from failing to match a seed and matches a seed
    # this corresponds to lower and upper bounds of location
    # from this we can identify our search start location = 99163750 on map line 5
    # from this we can also see our max search range is 63880419. This is 100x less than solver2 and solver3
    # for line in maps[-1]: print(line)

    # search_locations = [x[1] for x in maps[-1]] # initialise
    # bounds = get_next_bounds(check_search_locations(search_locations)) # initialise
    # print(bounds)
    # search_breadth = bounds[1] - bounds[0]
    # print(search_breadth)
    # while search_breadth > 1000:
    #     bounds = hone_in(bounds, False)
    # print(bounds)

    bounds = [maps[-1][0][1], maps[-1][-1][1]] # initialise with upper and lower bounds of last map.

    # binary search

    # print(bounds)
    # keep_going = 1
    # while keep_going:
    #     result = binary_search(bounds)
    #     bounds = result[0]
    #     keep_going = result[1]
    #     print(bounds)
    # print(bounds[1])

    # 1246164502

    length = 10
    while length > 2:
        decimated_search_locations = get_decimated_search_locations(bounds)
        length = len(decimated_search_locations)
        checked_search_locations = check_search_locations(decimated_search_locations)
        for x in checked_search_locations: print(x)
        bounds = get_next_bounds(checked_search_locations)
        print(bounds)

    final_search_locations = []
    for x in range(bounds[1]-bounds[0]+1):
        final_search_locations.append(bounds[0]+ x)
    print(final_search_locations)
    final_check = check_search_locations(final_search_locations)
    print(final_check)
    for x in final_check:
        if x[1]:
            print(x[0])
            break

    # 50716416




    # print(index+1, location_LB, location_UB)
    # print("location search range is ", location_UB- location_LB, "starting at", location_LB, "on line", index+2)

    # search!

    # seed_search(location_LB, location_UB, precision, maps, seeds)

    # location_LB = location_start # initialise
    # location = location_start # initialise
    # while location <= location_UB: # we should find it before then but just incase!
    #     seed = back_translate_location(location, maps)
    #     if location%precision == 0:
    #         os.system('cls' if os.name == 'nt' else 'clear')
    #         max_calculations_remaining = location_UB - location
    #         print("Max", max_calculations_remaining, "calculations remaining")
    #     if check_seed(seed, seeds): # we found it!
    #         return(location)
    #     else:
    #         location += precision

main()
