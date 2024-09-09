# Problem scope
'''
Jenga.
Falling blocks in 3d space.
Blocks start in mid air and must first come to rest either on teh ground or onto other blocks
Then everyblock that could be removed and not disturb the stack needs to be identified.
How many of these blocks are there?

Part 2:
Determine how many bricks would fall if any brick were disintegrated. Add these totals up
'''

# Solution sketch
'''
Sort blocks by z
Block objects reference blocks they rest on and blocks that rest on them?
Block method checks intersection
Set of blocks would form a contact network.
Disintigratable blocks would either support no blocks or be supported by more than one block

Part 2:
Recursively look for supported blocks that would fall.
Count em, loop em
'''
# Variables
def initialise(file):
    with open(file) as input:
        blocks = [Block([tuple(int(stapos) for stapos in line.split("~")[0].split(",")),
                tuple(int(endpos) for endpos in line.split("~")[1].split(","))]) for line in input.read().splitlines()]

    return sorted(blocks, key = lambda block: block.z0)

class Block():
    def __init__(b, pos) -> None:
        start = pos[0]
        end = pos[1]
        b.x0 = start[0]
        b.y0 = start[1]
        b.z0 = start[2]
        b.x1 = end[0]
        b.y1 = end[1]
        b.z1 = end[2]
        b.above = []
        b.below = []
        b.fallcount = None

    def __str__(b) -> str:
        return f"({b.x0}, {b.y0}, {b.z0}) -> ({b.x1}, {b.y1}, {b.z1}), supports {len(b.above)}, supported by {len(b.below)}"

    def isOnGround(b) -> bool:
        return b.z0 == 1

    def decendTo(b, z) -> None:
        height = b.z0 - z
        b.z0 = z
        b.z1 -= height

    def intersects(b, b2) -> bool:
        return b.x0 <= b2.x1 and b.x1 >= b2.x0 and b.y0 <= b2.y1 and b.y1 >= b2.y0

    def directlyAbove(b, b2) -> bool:
        return b.z0 == b2.z1 + 1

    def supports(b, b2) -> None:
        b.above.append(b2)

    def isNotSupporter(b) -> bool:
        return len(b.above) == 0

    def getSupportees(b) -> list:
        return b.above

    def getSupports(b) -> list:
        return b.below

    def sitsOn(b, b2) -> None:
        b.below.append(b2)

    def supportCount(b) -> int:
        return len(b.below)

    # def getFallCount(b) -> int:
    #     # If nothing above, fall count = 0
    #     # If someting above, fall count +1 above.fallcoutn if above not otherwise supported
    #     # Add above to list(disintegrated)
    #     if b.fallcount == None:
    #         b.fallcount = 0
    #         for b2 in b.above:
    #             if b2.support
    #             b.fallcount += b2.getFallCount()
    #     return b.fallcount

# Functions



# Main code
def main():
    # Create array of unsettled block objects from input data
    blocks = initialise("puzzle_input.txt")

    # print("Starting Positions:")
    # for block in blocks: print(block)

    # Settle blocks and update objects with neighbours
    settled = []
    for block in blocks:
        if block.isOnGround():
            settled.append(block)
        else:
            underneath = []

            # Find all below
            for below in reversed(settled):
                if block.intersects(below):
                    underneath.append(below)

            # Settle on tallest if present (reverse sort underneath by z1)
            underneath.sort(key = lambda block: block.z1, reverse = True)
            try: height = underneath[0].z1 + 1
            except: height = 1
            block.decendTo(height)

            # Update supporters and supported
            for below in underneath:
                if block.directlyAbove(below):
                    block.sitsOn(below)
                    below.supports(block)
                else: break
            settled.append(block)

    # print("Settled Positions:")
    # for block in settled: print(block)

    # For all blocks list supported blocks if they are solely supported.
    # For all of those blocks check their supported blocks
    # At end count them up
    # Optimisation: start from top of tower. Update block data for total supported blocks to speed up recursive search
    count = 0
    settled.sort(key = lambda x: x.z0) # Top block first

    # for block in settled: print(block)
    # print("\n")

    for block in settled:
        # block = settled[0]
        dis = set(()) # Disintegrated blocks
        newdis = [] # Queue of chain reaction of disintegrating blocks
        dis.add(block)
        newdis.append(block)
        while len(newdis) > 0:
            new = newdis.pop(0)
            for supportee in new.getSupportees():
                # print("Supportee:", supportee)
                # Check supportee to see it will fall without disintegrated blocks
                supports = set(supportee.getSupports())
                # print("Supports: ", supports)
                supports -= dis
                if len(supports)==0:
                    newdis.append(supportee)
                    dis.add(supportee)

        count += len(dis)-1
        # print(block)
        # print(f"Blocks disintigrated", len(dis)-1)

    answer = count
    print("The solution is:",answer)

main()
