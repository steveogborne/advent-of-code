from typing import TypeAlias
from collections import defaultdict

# Problem scope
'''
Walk through the maze in the woods.
^,<,>,v are slopes. You can only go down slopes
What is the longest route through the woods?
'''

# Solution sketch
'''
Need a walker algorithm
Need a tracker algorithm that builds a network of the woods
The network can have nodes which are the fork points
The edges will have distances between nodes
Then need a longest path. BFScl
'''
# Variables
with open("test_input.txt") as file:
    grid = file.read().splitlines()

grid[0] = grid[0][0] + "v" + grid[0][2:] # Simplify walk algorithm

# Functions
Position: TypeAlias = tuple[int, int]

class Node():
    def __init__(n, pos: Position, inb: list = None, outb: list = None) -> None:
        n.pos = pos # Stores an r,c coordinate for where it exists
        n.inb = inb if inb is not None else [] # Stores list references to incoming edges
        n.outb = outb if outb is not None else [] # Stores references to outgoing edges

    def __str__(n) -> str:
        return f"{n.pos}, in: {len(n.inb)}, out: {len(n.outb)}"

class Edge():
    def __init__(e, start: Position, end: Node = None, l: int = None) -> None:
        e.start = start # Stores reference to start node
        e.end = end # Stores reference to end node
        e.l = l # Stores length of

    def __str__(e) -> str:
        en = e.end.pos if e.end else "TBC"
        return f"{e.start} -({e.l})-> {en}"

    def walk(e, grid):
        stopped = False
        dist = 0
        # print("Start:", e.start)
        r,c = e.start
        last = grid[r][c] if grid[r][c] != "." else "v"

        while not stopped:
            east = south = west = north = None
            # Check east
            if last != "<":
                try: east = grid[r][c+1]
                except: pass
            # Check south
            if last != "^":
                try: south = grid[r+1][c]
                except: pass
            # Check west
            if last != ">":
                try: west = grid[r][c-1]
                except: pass
            # Check north
            if last != "v":
                try: north = grid[r-1][c]
                except: pass

            match east:
                case ".": c += 1; dist += 1; last = ">"
                case ">": c += 2; dist += 2; stopped = True
                case _: pass
            match south:
                case ".": r += 1; dist += 1; last = "v"
                case "v": r += 2; dist += 2; stopped = True
                case _: pass
            match west:
                case ".": c -= 1; dist += 1; last = "<"
                case _: pass
            match north:
                case ".": r -= 1; dist += 1; last = "^"
                case _: pass

            if r == 22 and c == 21: stopped = True

        endpos = (r,c)
        # print("End:", endpos)
        e.l = dist
        return endpos

# Main code
def main():
    ### Map Network
    # Setup a register of nodes and edges
    nodes = {}
    edges = []

    # Initialise start node and first edge
    startpos = (0,1)
    start_n = Node(startpos)
    start_e = Edge(startpos)
    start_n.outb.append(start_e)
    nodes[startpos] = start_n

    # set up a queue of edges to explore from. Initialise with first edge
    frontiers = [start_e]

    # >> start walking along an edge until a new node is found.
    while len(frontiers) > 0:
        # Select an edge to evaluate
        active = frontiers.pop()
        # Find end of this edge and update edge distance
        endpos = active.walk(grid)
        # If node not previosuly found, create it and it's outgoing edges
        if endpos not in nodes:
            nodes[endpos] = Node(endpos)
            # If new node: Create new edges for all forks out of node and add to queue
            # Update node with outgoing edges
            try: east = grid[endpos[0]][endpos[1]+1]
            except: east = None
            if east == ">":
                east_e = Edge((endpos[0],endpos[1]+1))
                frontiers.append(east_e)
                nodes[endpos].outb.append(east_e)
            try: south = grid[endpos[0]+1][endpos[1]]
            except: south = None
            if south == "v":
                south_e = Edge((endpos[0]+1,endpos[1]))
                frontiers.append(south_e)
                nodes[endpos].outb.append(south_e)

        # New or not, update node with this edge as incoming
        nodes[endpos].inb.append(active)
        # Update the edge with finishing node
        active.end = nodes[endpos]
        # Put the finished edge in the edge list
        edges.append(active)
        # Repeat until queue is empty

    print("\nNodes")
    for node in nodes: print(node)
    print("\nEdges")
    for edge in edges: print(edge)
    ### Longest path
    # While end node not found:
    # Keep a list of route frontiers, initialise with start node
    # Traverse to next node, create new frontiers based on number of departing edges
    # Repeat until list of frontiers is empty
    # Don't know how to optimise because it's not shortest path. Selecting longest path in queue will just shortcut to end so...
    # Just go for completion. I guess it's BFS
    answer = "Undefined"
    print("The solution is:",answer)

main()
