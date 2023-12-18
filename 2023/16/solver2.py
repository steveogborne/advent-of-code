# Problem scope
'''
Laser mirrors
Input is an image. . is empty tile, \ and / are 90-degree reflecting mirrors and | and - are splitters.
Beam enters top left going left
A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it
How many tiles are being energised

Part 2: the laser can start anywhere on the edge facing in. What is the position with the max heat?
'''

# Solution sketch
'''
Get input
Need a function to step through the beam's path(s) depending on what is on a particular tile.
> Perhaps a vector so we can count all split beams as we go.
Need a function that updates an image of energised tiles (or otherwise tracks energised tiles)
Need a function that counts energised tiles

Part 2: iterate part 1 code over all input possibilities and keep max answer
'''
# Variables

import time
test_input = '''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\..
.-.-/..|..
.|....-|.\\
..//.|....
'''
test_map = test_input.splitlines()

with open("puzzle_input.txt") as file:
    mirror_map = file.read().splitlines()
    mirror_map = [[char for char in line] for line in mirror_map]
    max_c = len(mirror_map[0]) - 1
    max_l = len(mirror_map) - 1
    heat_map = [["." for char in line] for line in mirror_map]



class Beam:
    def __init__(self, l, c, heading):
        self.l = l #line_index
        self.c = c #column index
        self.heading = heading

    def move(self):
        match self.heading:
            case "N":
                if self.l != 0: self.l -=1
                else: self.heading = "X"
            case "E":
                if self.c != max_c: self.c +=1
                else: self.heading = "X"
            case "S":
                if self.l != max_l: self.l +=1
                else: self.heading = "X"
            case "W":
                if self.c != 0: self.c-=1
                else: self.heading = "X"
            case "X": return

    def display(self):
        return self.l,self.c,self.heading

# Functions

def step_beams(beams, mirror_map):
    # beams is list of Beam objects
    new_beams = []
    stopped = True
    for b in beams:
        heat_map[b.l][b.c] = "#" # energise tile
        if b.heading == "X": continue
        else:
            match mirror_map[b.l][b.c]:
                case ".":
                    match b.heading:
                        case "N": mirror_map[b.l][b.c] = "^"
                        case "E": mirror_map[b.l][b.c] = ">"
                        case "S": mirror_map[b.l][b.c] = "v"
                        case "W": mirror_map[b.l][b.c] = "<"
                    b.move()
                    stopped = False
                case "/":
                    match b.heading:
                        case "N": b.heading = "E"
                        case "E": b.heading = "N"
                        case "S": b.heading = "W"
                        case "W": b.heading = "S"
                    b.move()
                    stopped = False
                case "\\":
                    match b.heading:
                        case "N": b.heading = "W"
                        case "E": b.heading = "S"
                        case "S": b.heading = "E"
                        case "W": b.heading = "N"
                    b.move()
                    stopped = False
                case "|":
                    if b.heading in ["N","S"]: b.move()
                    else:
                        if b.l!=0: new_beams.append(Beam(b.l-1, b.c, "N"))
                        b.heading = "S"; b.move()
                    stopped = False
                case "-":
                    if b.heading in ["E","W"]: b.move()
                    else:
                        if b.c!=0: new_beams.append(Beam(b.l, b.c-1, "W"))
                        b.heading = "E"; b.move()
                    stopped = False
                case "v":
                    if b.heading in ["S","N"]: b.heading = "X"
                    else: mirror_map[b.l][b.c] = "2"; b.move(); stopped = False
                case "^":
                    if b.heading in ["S","N"]: b.heading = "X"
                    else: mirror_map[b.l][b.c] = "2"; b.move(); stopped = False
                case ">":
                    if b.heading in ["E","W"]: b.heading = "X"
                    else: mirror_map[b.l][b.c] = "2"; b.move(); stopped = False
                case "<":
                    if b.heading in ["E","W"]: b.heading = "X"
                    else: mirror_map[b.l][b.c] = "2"; b.move(); stopped = False
                case "2":
                    b.heading = "X"

        # match b.heading:
        #     case "X": continue
        #     case "N":
        #         match mirror_map[b.l][b.c]:
        #             case "|": b.move()
        #             case ".": b.move()
        #             case "/": b.heading = "E"; b.move()
        #             case "\\": b.heading = "W"; b.move()
        #             case "-":
        #                 if b.c!=0: new_beams.append(Beam(b.l, b.c-1, "W"))
        #                 b.heading = "E"; b.move()
        #     case "E":
        #         match mirror_map[b.l][b.c]:
        #             case "-": b.move()
        #             case ".": b.move()
        #             case "/": b.heading = "N"; b.move()
        #             case "\\": b.heading = "S"; b.move()
        #             case "|":
        #                 if b.l!=0: new_beams.append(Beam(b.l-1, b.c, "N"))
        #                 b.heading = "S"; b.move()
        #     case "S":
        #         match mirror_map[b.l][b.c]:
        #             case "|": b.move()
        #             case ".": b.move()
        #             case "/": b.heading = "W"; b.move()
        #             case "\\": b.heading = "E"; b.move()
        #             case "-":
        #                 if b.c!=0: new_beams.append(Beam(b.l, b.c-1, "W"))
        #                 b.heading = "E"; b.move()
        #     case "W":
        #         match mirror_map[b.l][b.c]:
        #             case "-": b.move()
        #             case ".": b.move()
        #             case "/": b.heading = "S"; b.move()
        #             case "\\": b.heading = "N"; b.move()
        #             case "|":
        #                 if b.l!=0: new_beams.append(Beam(b.l-1, b.c, "N"))
        #                 b.heading = "S"; b.move()
    for beam in new_beams: beams.append(beam)
    return beams, stopped


# Main code
def main():
    beams = [Beam(0,0,"E")]
    stopped = False
    while not stopped:
        beams, stopped = step_beams(beams, mirror_map)
    heat = sum([line.count("#") for line in heat_map])

    answer = heat
    print("The solution is:",answer)

start = time.time()
main()
end = time.time()
print(end-start)
