from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

# Problem scope
'''
Lava crucible update to supercricible
Super crucible can go minimum of 4 in straight line before turning OR ENDING
Super crucible can go max of 10 in straight line
'''

# Solution sketch
'''
Modify neighbours logic with new limits and this should work fine
'''
# Globals
with open("puzzle_input.txt") as file:
    heatMap = file.read().splitlines()

height = len(heatMap)
width = len(heatMap[0])

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

# Functions
def getHeuristic(vertex):
    (r, c) = vertex[0]
    return abs(height-1-r) + abs(width-1-c)

def getNeighbours(vertex):
    (r,c) = vertex[0]
    movement = vertex[1]
    m = vertex[2]
    neighbours = []
    match movement:
        case "^":
            if r > 0 and m < 10: neighbours.append(((r-1,c), "^", m+1)) # up
            if c > 0 and m > 3: neighbours.append(((r,c-1), "<", 1)) #left
            if c < width -1 and m > 3: neighbours.append(((r,c+1), ">", 1)) #right
        case ">":
            if r > 0  and m > 4: neighbours.append(((r-1,c), "^", 1)) # up
            if c < width -1 and m < 10: neighbours.append(((r,c+1), ">", m+1)) # right
            if r < height -1 and m > 3: neighbours.append(((r+1,c), "v", 1))# down
        case "v":
            if c < width -1 and m > 3: neighbours.append(((r,c+1), ">", 1)) # right
            if r < height -1 and m < 10: neighbours.append(((r+1,c), "v", m+1)) # down
            if c > 0 and m > 3: neighbours.append(((r,c-1), "<", 1)) # left
        case "<":
            if r < height -1 and m > 3: neighbours.append(((r+1,c), "v", 1)) # down
            if c > 0 and m < 10: neighbours.append(((r,c-1), "<", m+1)) # left
            if r > 0 and m > 3: neighbours.append(((r-1,c), "^", 1)) # up
        case "":
            neighbours.append(((r,c+1), ">", 1)) # right
            neighbours.append(((r+1,c), "v", 1)) # down
    return neighbours

# Main code

def main():

    visited = {} # vertices that have been evaluated; {vertex: distance}
    frontier = PriorityQueue() # next vertices to be evaluated PrioritisedItem(priority, vertex)

    origin = ((0,0),"",0) # first vertex
    visited[origin] = 0 # update visited with first vertex and distance
    frontier.put(PrioritizedItem(0, origin))
    searching = True

    best = 9999

    while not frontier.empty():
        nextPI = frontier.get()
        next = nextPI.item
        distance_so_far = visited[next]
        if next[0] == (width-1, height-1) and next[2]>3:
            score = visited[next]
            if score < best: best = score
            print(f"Destination reached with total heat: {score}")
            print(next)
            # searching = False
        else:
            neighbours = getNeighbours(next)
            for neighbour in neighbours:
                # get distance for neighbour
                (r,c) = neighbour[0]
                heat = int(heatMap[r][c])
                distance = distance_so_far + heat
                # if not in visited: add to visited, update best distance and add to frontier queue
                if neighbour not in visited.keys():
                    visited[neighbour] = distance
                    heuristic = abs(height-r) + abs(width-c)
                    frontier.put(PrioritizedItem(distance + heuristic, neighbour))
                elif distance < visited[neighbour]:
                    visited[neighbour] = distance
                    heuristic = abs(height-r) + abs(width-c)
                    frontier.put(PrioritizedItem(distance + heuristic, neighbour))
                else:
                    pass


                # if in visited, compare best distance and update if best distance is less

    top = 10
    topCount = 0
    print(f"Top {top}:")
    while not frontier.empty():
        topCount +=1
        vertex = frontier.get()
        if topCount < top:
            print(vertex.priority, vertex.item, visited[vertex.item])
    print(f"of {topCount} remaining frontiers")

    print(f"Best = {best}")

main()
