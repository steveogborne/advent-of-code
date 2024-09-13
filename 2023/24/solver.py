# Problem scope
'''
Colliding Hail Stones
Hail stones are moving linearly at constant speed.
The data gives a snapshot of their position and speed
Part 1:
Do the x,y FUTURE trajectories intersect within the test bounds?
'''

# Solution sketch
'''
For every stone find where they intersect with teh boundary in the x,y plane
Then every line has a start and end coord.
Iteratively check every pair of hailstones and check for intersection

'''
# Variables
class Stone:
    def __init__(s, pos: list, vel: list) -> None:
        s.x0 = pos[0]
        s.y0 = pos[1]
        s.z0 = pos[2]
        s.vx = vel[0]
        s.vy = vel[1]
        s.vz = vel[2]

    def __str__(s) -> str:
        return f"p0: ({s.x0},{s.y0},{s.z0}), v: ({s.vx},{s.vy},{s.vz})"

    def intersects(s, o, lb, ub, test = False) -> bool:
        gs = (s.vy / s.vx)
        go = (o.vy / o.vx)
        if gs == go:
            if test: print(f"No. Stones {s} and {o} trajectories parallel")
            return False
        else:
            x = (o.y0 - go * o.x0 - s.y0 + gs * s.x0) / (gs - go)
            y = gs * (x - s.x0) + s.y0
            ts = (x - s.x0) / s.vx
            to = (x - o.x0) / o.vx

        if test:
            if ts < 0 or to < 0:
                print(f"No. Stones {s} and {o} intersect at x = {x:.2f}, y = {y:.2f} in the past")
            elif not lb < x < ub or not lb < y < ub:
                print(f"No. Stones {s} and {o} intersect at x = {x:.2f}, y = {y:.2f} outside boundaries")
            else:
                print(f"Yes. Stones {s} and {o} intersect at x = {x:.2f}, y = {y:.2f}")

        return ts>0 and to>0 and lb < x < ub and lb < y < ub


# Functions
def initialise(input):
    with open(input) as file:
        hail = [Stone([int(pos.strip()) for pos in line.split("@")[0].split(",")],
                [int(vel.strip()) for vel in line.split("@")[1].split(",")])
                for line in file.read().splitlines()]

    # for stone in hail: print(stone)
    return hail


# Main code
def main():
    input = ["test_input.txt", "puzzle_input.txt"][1]
    bounds = {"test_input.txt": (7 , 27), "puzzle_input.txt": (200000000000000, 400000000000000)}
    hail = initialise(input)
    lb, ub = bounds[input]
    count = 0
    while len(hail) > 0:
        test_stone = hail.pop(0)
        for other_stone in hail:
            if test_stone.intersects(other_stone, lb, ub): count +=1

    answer = count
    print("The solution is:",answer)

main()
