# Problem scope
'''
Laser mirrors
Input is an image. . is empty tile, \ and / are 90-degree reflecting mirrors and | and - are splitters.
Beam enters top left going left
A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it
How many tiles are being energised
'''

# Solution sketch
'''
Get input
Need a function to step through the beam's path(s) depending on what is on a particular tile.
> Perhaps a vector so we can count all split beams as we go.
Need a function that updates an image of energised tiles (or otherwise tracks energised tiles)
Need a function that counts energised tiles
'''
# Variables
with open("puzzle_input.txt") as file:
    mirror_map = file.read().splitlines()
    # max_c = len(mirror_map[0]) - 1
    # max_l = len(mirror_map) - 1
    max_c, max_l = 9,9
    heat_map = [["." for char in line] for line in mirror_map]

test_input = '''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\..
.-.-/..|..
.|....-|.\\
..//.|....
'''
test_input = test_input.splitlines()

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

def new_beam(bims, l, c, heading):
    # beams have names b_X where X is their index
    # Get last beam name
    last_name_index = int(list(bims.keys())[-1].split("_")[-1])
    new_name = "b_"+str(last_name_index +1)
    bims[new_name] = Beam(l, c, heading)
    return bims

def step_beams(beams, mirror_map):
    # beams is list of Beam objects
    new_beams = []
    go_flag = False
    for b in beams:
        heat_map[b.l][b.c] = "#" # energise tile
        match b.heading:
            case "X": continue
            case "N":
                go_flag = True
                match mirror_map[b.l][b.c]:
                    case "|": b.move()
                    case ".": b.move()
                    case "/": b.heading = "E"; b.move()
                    case "\\": b.heading = "W"; b.move()
                    case "-":
                        if b.c!=0: new_beams.append(Beam(b.l, b.c-1, "W"))
                        b.heading = "E"; b.move()
            case "E":
                go_flag = True
                match mirror_map[b.l][b.c]:
                    case "-": b.move()
                    case ".": b.move()
                    case "/": b.heading = "N"; b.move()
                    case "\\": b.heading = "S"; b.move()
                    case "|":
                        if b.l!=0: new_beams.append(Beam(b.l-1, b.c, "N"))
                        b.heading = "S"; b.move()
            case "S":
                go_flag = True
                match mirror_map[b.l][b.c]:
                    case "|": b.move()
                    case ".": b.move()
                    case "/": b.heading = "W"; b.move()
                    case "\\": b.heading = "E"; b.move()
                    case "-":
                        if b.c!=0: new_beams.append(Beam(b.l, b.c-1, "W"))
                        b.heading = "E"; b.move()
            case "W":
                go_flag = True
                match mirror_map[b.l][b.c]:
                    case "-": b.move()
                    case ".": b.move()
                    case "/": b.heading = "S"; b.move()
                    case "\\": b.heading = "N"; b.move()
                    case "|":
                        if b.l!=0: new_beams.append(Beam(b.l-1, b.c, "N"))
                        b.heading = "S"; b.move()
    for beam in new_beams: beams.append(beam)
    return beams, go_flag


# Main code
def main():
    beams = [Beam(0,0,"E")]
    print(".0123456789")
    for index, line in enumerate(test_input): print(str(index)+line)
    print("\n")
    go_flag = True
    while go_flag:
        beams, go_flag = step_beams(beams, test_input)
        print([beam.display() for beam in beams])
    answer = "Undefined"
    print("The solution is:",answer)

main()
# beams = {"b_0": Beam(0,0,"E")}
# beams["b_1"] = Beam(0,1,"S")
# # last_name_index = int(beams.keys()[-1].__name__.split("_")[-1])
# last_name_index = beams.keys()[0]
# print(last_name_index)
