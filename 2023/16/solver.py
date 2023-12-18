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
    for b in beams:
        heat_map[b.l][b.c] = "#" # energise tile
        match b.heading:
            case "X": continue
            case "N":
                match mirror_map[b.l][b.c]:
                    case "|": b.move()
                    case ".": b.move()
                    case "/": b.heading = "E"; b.move()
                    case "\\": b.heading = "W"; b.move()
                    case "-":
                        if b.c!=0: new_beams.append(Beam(b.l, b.c-1, "W"))
                        b.heading = "E"; b.move()
            case "E":
                match mirror_map[b.l][b.c]:
                    case "-": b.move()
                    case ".": b.move()
                    case "/": b.heading = "N"; b.move()
                    case "\\": b.heading = "S"; b.move()
                    case "|":
                        if b.l!=0: new_beams.append(Beam(b.l-1, b.c, "N"))
                        b.heading = "S"; b.move()
            case "S":
                match mirror_map[b.l][b.c]:
                    case "|": b.move()
                    case ".": b.move()
                    case "/": b.heading = "W"; b.move()
                    case "\\": b.heading = "E"; b.move()
                    case "-":
                        if b.c!=0: new_beams.append(Beam(b.l, b.c-1, "W"))
                        b.heading = "E"; b.move()
            case "W":
                match mirror_map[b.l][b.c]:
                    case "-": b.move()
                    case ".": b.move()
                    case "/": b.heading = "S"; b.move()
                    case "\\": b.heading = "N"; b.move()
                    case "|":
                        if b.l!=0: new_beams.append(Beam(b.l-1, b.c, "N"))
                        b.heading = "S"; b.move()
    for beam in new_beams: beams.append(beam)
    return beams


# Main code
def main():
    beams = [Beam(0,0,"E")]
    buffer = 50
    while buffer >0:
        energised_tiles = sum([line.count("#") for line in heat_map])
        # for line in heat_map:print("".join(line))
        beams = step_beams(beams, mirror_map)
        energised_tiles2 = sum([line.count("#") for line in heat_map])
        # print(energised_tiles, energised_tiles2)
        # print([beam.display() for beam in beams])
        if energised_tiles2 - energised_tiles == 0: buffer-=1
    answer = energised_tiles
    print("The solution is:",answer)

main()
