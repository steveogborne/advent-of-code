# Number word lookups
nums = "zero one two three four five six seven eight nine".split(" ")
rev_nums = [x[::-1] for x in nums]

# Function to find first digit or numer word in line
def d1(line, nums):
    for index, char in enumerate(line):
        if char.isdecimal(): return int(char)
        else:
            for n, num in enumerate(nums):
                if line.find(num) == index: return n

# set a value to keep track of score
total_value = 0

# For each line in puzzle input return a value which is the concatenated first and last numbers
with open("puzzle_input.txt", "r") as file:
    for line in file:
        total_value += int(str(d1(line, nums))+str(d1(line[::-1], rev_nums)))

print(total_value)




def first_digit(line):
    numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for count, character in enumerate(line):
        if character.isdecimal():
            return int(character)
        else:
            for value, number in enumerate(numbers):
                if line.find(number) == count:
                    return value

def last_digit(line):
    rev_line = line[::-1] # Slice string
    rev_numbers = ["orez", "eno", "owt", "eerht", "ruof", "evif", "xis", "neves", "thgie", "enin"]
    for count, character in enumerate(rev_line):
        if character.isdecimal():
            return int(character)
        else:
            for value, rev_number in enumerate(rev_numbers):
                if rev_line.find(rev_number) == count:
                    return value

total_2 = 0
with open("puzzle_input.txt") as file:
    for line in file:
        total_2 += (int(str(first_digit(line))+str(last_digit(line))))

print(total_2)
