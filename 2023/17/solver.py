# Problem scope
'''
Get your "lava crucible" from the lava pool to the factory losing the least amount of heat
Input is a city map. Each tile is a city block and the number in the tile is the "heat lost" on that tile
The crucible can move at most 3 steps in one direction before it needs to turn left or right
Crucible can never turn back on left, right or straight on.
It loses heat when it enters a tile therefore does not lose heat on the first tile unless it is entered again
What is the minimum heat loss?
'''

# Solution sketch
'''
Damn is this a machine learning problem???
If I were training somethign:
I would want to reward reducing number of steps (direct route).
But also avoid more heat loss tiles
Algorithmically:
Revise dijkstra's algorithm. But how to factor in the turning limit part?

'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()

example = '''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''
example_min_path = '''
2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
'''
# Functions



# Main code
def main():
    answer = "Undefined"
    print("The solution is:",answer)

main()
