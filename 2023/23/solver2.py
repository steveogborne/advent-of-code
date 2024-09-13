from typing import TypeAlias
from collections import defaultdict

# Problem scope
'''
Walk through the maze in the woods.
^,<,>,v are slopes. You can only go down slopes
What is the longest route through the woods?

Part 2:
Slopes don't matter anymore
What is the longest non repeating route?
'''

# Solution sketch
'''
Need a walker algorithm
Need a tracker algorithm that builds a network of the woods
The network can have nodes which are the fork points
The edges will have distances between nodes
Then need a longest path. BFScl

Part 2:
Nodes and edges remain the same but edges not directed
Can keep the network establishment the same
Need to fix the edges so that I can reference the start node
Add a edge method to traverse it given either start or end node
Update route finders to keep track of nodes or edges traversed for each route to avoid double stepping
I think distances should work out.
Need to choose from inbound and outbound edges to traverse
'''
# Variables
with open("puzzle_input.txt") as file:
    grid = file.read().splitlines()

final = (len(grid)-1, len(grid[0])-2)
# print("Final:",final)

# Functions
Position: TypeAlias = tuple[int, int]

class Node():
    def __init__(n, pos: Position, inb: list = None, outb: list = None, long: int = 0, vis: bool = False) -> None:
        n.pos = pos # Stores an r,c coordinate for where it exists
        n.inb = inb if inb is not None else [] # Stores list references to incoming edges
        n.outb = outb if outb is not None else [] # Stores references to outgoing edges
        n.long = long # Longest path to this node
        n.vis = vis
    def __str__(n) -> str:
        return f"{n.pos}, in: {len(n.inb)}, out: {len(n.outb)}"

class Edge():
    def __init__(e, dir: str, start: Node, end: Node = None, l: int = None) -> None:
        e.dir = dir # Direction edge travels to initiate edge
        e.start = start # Stores reference to start node
        e.end = end # Stores reference to end node
        e.l = l # Stores length of edge

    def __str__(e) -> str:
        en = e.end.pos if e.end else "TBC"
        return f"{e.start.pos} -({e.l})-> {en}"

    def walk(e, grid):
        stopped = False
        # print("Start:", e.start)
        r,c = e.start.pos
        last = e.dir
        match last:
            case ">": c += 1
            case "v": r += 1
        dist = 1

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

            if (r, c) == final: stopped = True

        endpos = (r,c)
        # print("End:", endpos)
        e.l = dist
        return endpos

    def traverseFrom(e, start) -> Node:
        if e.start == start: return e.end
        else: return e.start

def getLongestPath(node, currSum):
    if node.vis:
        return
    node.vis = True

    if node.long < currSum:
        node.long = currSum

    children = node.inb + node.outb
    for child in children:
        getLongestPath(child.traverseFrom(node), currSum + child.l)

    node.vis = False

# Main code
def main():
    ### Map Network
    # Setup a register of nodes and edges
    nodes = {} # int: (pos, list(edges))
    edges = [] # int: ((node, node), dist)

    # Initialise start node and first edge
    startpos = (0,1)
    start_n = Node(startpos)
    start_e = Edge("v", start_n)
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
                east_e = Edge(">", nodes[endpos])
                frontiers.append(east_e)
                nodes[endpos].outb.append(east_e)
            try: south = grid[endpos[0]+1][endpos[1]]
            except: south = None
            if south == "v":
                south_e = Edge("v", nodes[endpos])
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
    for k in nodes.keys(): print(nodes[k])
    print("\nEdges")
    for edge in edges: print(edge)

    ### Visualise
    output = [[" " for char in line] for line in grid]

    for r,c in nodes:
        output[r//5][c//5] = "@"

    edgemark = {">": "-", "v": "|"}

    for edge in edges:
        r0, c0 = edge.start.pos
        r1, c1 = edge.end.pos

        r= (r0//5+r1//5)//2
        c= (c0//5+c1//5)//2
        if output[r][c] != "@": output[r][c] = edgemark[edge.dir]


    output = ["".join(line) for line in output]
    with open("output.txt", "w") as file:
        for line in output:
            file.write(line+"\n")

    ### Longest path
    # Keep a list of route frontiers, initialise with start node
    # routes = [(nodes[(0,1)], 0, [])]
    # route_ds = []
    # count = 0

    # While end node not found:
    # while len(routes) > 0 and count < 1000:
    #     count += 1
    #     # Traverse to next node, create new frontiers based on number of departing edges
    #     current_n, current_d, comp_n = routes.pop()
    #     if current_n.pos != final:
    #         es = current_n.outb + current_n.inb
    #         ns = [(e.traverseFrom(current_n), e.l) for e in es]
    #         valid_ns = [(n, d) for (n, d) in ns if n not in comp_n]
    #         # print("Valid nodes:", *valid_ns)
    #         for (n, d) in valid_ns:
    #             routes.append((n, current_d + d, comp_n+[current_n]))
    #     else:
    #         route_ds.append(current_d)
    #         # print(current_d, current_n, len(comp_n))

    # print("\nRoutes in progress")
    # for route in routes[0:10]: print(*route[2], route[0], route[1])
    # print("\nRoute distances:")
    # print(route_ds)

    # answer = max(route_ds) if len(route_ds) > 0 else "TBC"

    getLongestPath(start_n, 0)
    answer = nodes[(140,139)].long

    print("The solution is:",answer)

main()
