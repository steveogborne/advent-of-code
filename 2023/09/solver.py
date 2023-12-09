# Problem scope
'''
Each line is a history
Each element in the history is incremented to the next one by a certain difference value
This gives a new list of values
Each element in the is incremented to the next one by a certain difference value
When all diferences are 0 the pattern stops and the next value of teh original sequence can be inferred
The next value is the sum of all the last numbers in each of the value lists
'''

# Solution sketch
'''
Read lines one by one
For each line create a difference list and append it to a super list
If all lements of the last list in super list = 0
...then sum all final elements of all the lists
... otherwise create a new difference list base on the last list and add it to the superlist
'''

with open("puzzle_input.txt") as file:
    input = file.read().splitlines()

history_list = [[int(x) for x in line.split(" ")] for line in input]
first_history = history_list[0]


# Main code
def main():
    predictions_sum = 0
    for history in history_list:
        superlist = []
        superlist.append(history)
        while superlist[-1] != [0 for x in superlist[-1]]:
            new_difference_list = [superlist[-1][index+1]-superlist[-1][index] for index in range(len(superlist[-1])-1)]
            superlist.append(new_difference_list)
        predicted_value = 0
        for list in superlist:
            predicted_value += list[-1]
        print([x[-1] for x in superlist], predicted_value)
        predictions_sum += predicted_value
    print("Answer:",predictions_sum)

main()
