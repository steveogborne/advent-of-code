import time

with open("puzzle_input.txt") as file:
    input = file.read().splitlines()
    platform = [[x for x in l] for l in input]
    rocks = []
    count = 0
    for li, ln in enumerate(platform):
        for ci, ch in enumerate(ln):
            if ch == "O":
                rocks.append({"rock": count, "line": li, "column": ci})
    # [rocks[index].append(index) for index in range(len(rocks))]
    cubes_in_rows = [[[li,ci] for ci,ch in enumerate(ln) if ch=="#"] for li,ln in enumerate(platform)]
    # for x in cubes_in_rows: print(x)

    # rocks_bottom_up = rocks.sort(key = )

# row search ranges is a list of start and end coordinates for empty spaces between rocks on rows
row_search_ranges = []
for line in platform:
    row_search_ranges.append([])
    start = 0
    for cindex, char in enumerate(line):
        end = len(line)-1
        if char == "#":
            if cindex > start+1:
                row_search_ranges[-1].append([start, cindex])
            start = cindex +1
        if cindex == end and char != "#" and start!= cindex:
            row_search_ranges[-1].append([start, cindex+1])

for lindex, line in enumerate(row_search_ranges):
    for sindex, search_range in enumerate(line):
        if search_range[1] - search_range[0] == 1: row_search_ranges[lindex].pop(sindex)

# col search ranges is a list of start and end coordinates for empty spaces between rocks on columns
col_search_ranges = []
for cindex in range(len(platform[0])):
    col_search_ranges.append([])
    start = 0
    for lindex, line in enumerate(platform):
        end = len(platform)-1
        if line[cindex] == "#":
            if lindex > start:
                col_search_ranges[-1].append([start, lindex])
            start = lindex +1
        if lindex == end and line[cindex] != "#" and start!= cindex:
            col_search_ranges[-1].append([start, lindex+1])

for cindex, col in enumerate(col_search_ranges):
    for sindex, search_range in enumerate(col):
        if search_range[1] - search_range[0] == 1: col_search_ranges[cindex].pop(sindex)

def shift_west(image):
    for lindex, line in enumerate(row_search_ranges):
        for search_range in line:
            o_count = 0
            # before = [image[lindex][c] for c in range(search_range[0],search_range[1])]
            for cindex in range(search_range[0],search_range[1]):
                if image[lindex][cindex] == "O":
                    o_count+=1
                    image[lindex][cindex] = "."
            for cindex in range(search_range[0], search_range[0]+o_count):
                image[lindex][cindex] = "O"
            # after = [image[lindex][c] for c in range(search_range[0],search_range[1])]
            # print(before, "->", after)
    return(image)

def shift_east(image):
    for lindex, line in enumerate(row_search_ranges):
        for search_range in line:
            o_count = 0
            for cindex in range(search_range[0],search_range[1]):
                if image[lindex][cindex] == "O":
                    o_count += 1
                    image[lindex][cindex] = "."
            for cindex in range(search_range[1]-o_count, search_range[1]):
                image[lindex][cindex] = "O"
    return(image)

def shift_north(image):
    for cindex, col in enumerate(col_search_ranges):
        for search_range in col:
            o_count = 0
            # before = [image[l][cindex] for l in range(search_range[0],search_range[1])]
            for lindex in range(search_range[0],search_range[1]):
                if image[lindex][cindex] == "O":
                    o_count += 1
                    image[lindex][cindex] = "."
            for lindex in range(search_range[0], search_range[0]+o_count):
                image[lindex][cindex] = "O"
            # after = [image[l][cindex] for l in range(search_range[0],search_range[1])]
            # print(before, "->", after)
    return(image)

def shift_south(image):
    for cindex, col in enumerate(col_search_ranges):
        for search_range in col:
            o_count = 0
            # before = [image[l][cindex] for l in range(search_range[0],search_range[1])]
            for lindex in range(search_range[0],search_range[1]):
                if image[lindex][cindex] == "O":
                    o_count += 1
                    image[lindex][cindex] = "."
            for lindex in range(search_range[1]-o_count, search_range[1]):
                image[lindex][cindex] = "O"
            # after = [image[l][cindex] for l in range(search_range[0],search_range[1])]
            # print(before, "->", after)
    return(image)

def calculate_weight(image):
    total_weight = 0
    max_weight = len(image)
    for l_index, line in enumerate(image):
        line_count = line.count("O")
        weight = max_weight - l_index
        total_weight += weight*line_count
    return(total_weight)


def output_platform_image(image_matrix, dir):
        image_str = ["".join(line) for line in image_matrix]
        with open(dir, "w") as file2:
            for line in image_str:
                file2.write(line+"\n")

def spin_cycle_A(image):
    return shift_east(shift_south(shift_west(shift_north(image))))
    # 0.43 for 100 cycles

def main():
    spins = 1000
    last_spin = 1000
    loads = []
    while spins >0:
        # shift_north
        for cindex, col in enumerate(col_search_ranges):
            for search_range in col:
                o_count = 0
                # before = [platform[l][cindex] for l in range(search_range[0],search_range[1])]
                for lindex in range(search_range[0],search_range[1]):
                    if platform[lindex][cindex] == "O":
                        o_count += 1
                        platform[lindex][cindex] = "."
                for lindex in range(search_range[0], search_range[0]+o_count):
                    platform[lindex][cindex] = "O"
                # after = [platform[l][cindex] for l in range(search_range[0],search_range[1])]
                # print(before, "->", after)

        # shift_west
        for lindex, line in enumerate(row_search_ranges):
            for search_range in line:
                o_count = 0
                # before = [platform[lindex][c] for c in range(search_range[0],search_range[1])]
                for cindex in range(search_range[0],search_range[1]):
                    if platform[lindex][cindex] == "O":
                        o_count+=1
                        platform[lindex][cindex] = "."
                for cindex in range(search_range[0], search_range[0]+o_count):
                    platform[lindex][cindex] = "O"
                # after = [platform[lindex][c] for c in range(search_range[0],search_range[1])]
                # print(before, "->", after)

        # shift_south
        for cindex, col in enumerate(col_search_ranges):
            for search_range in col:
                o_count = 0
                # before = [platform[l][cindex] for l in range(search_range[0],search_range[1])]
                for lindex in range(search_range[0],search_range[1]):
                    if platform[lindex][cindex] == "O":
                        o_count += 1
                        platform[lindex][cindex] = "."
                for lindex in range(search_range[1]-o_count, search_range[1]):
                    platform[lindex][cindex] = "O"
                # after = [platform[l][cindex] for l in range(search_range[0],search_range[1])]
                # print(before, "->", after)

        # shift_east(platform):
        for lindex, line in enumerate(row_search_ranges):
            for search_range in line:
                o_count = 0
                for cindex in range(search_range[0],search_range[1]):
                    if platform[lindex][cindex] == "O":
                        o_count += 1
                        platform[lindex][cindex] = "."
                for cindex in range(search_range[1]-o_count, search_range[1]):
                    platform[lindex][cindex] = "O"
        spins -=1

    # new_platform = shift_east(shift_south(shift_west(shift_north(platform))))
    # output_platform_image(spun_platform, "platform_output.txt")
        target_load = 100492
        load = calculate_weight(platform)
        if load not in loads: loads.append(load)
        if load == target_load:
            print(spins, last_spin - spins)
            last_spin = spins
    print(len(loads), loads[-1])
    print(load)

start = time.time()
main()
end = time.time()
print(end - start)

# After settling the load cycles with period 39. So load at 1000000000 will be the same as the load at 1000000000 - 39*n
# Lets give it 1000 cycles to settle. There are 999999000 cycles after that
# 999999000 / 39 = 25641000 is a round number so load at 1000th cycle = load at 1000000000th cycle...
