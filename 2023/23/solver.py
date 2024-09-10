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
Then need a longest path. Can use dijkstras again
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()

# Functions
class Node():
    def __init__(self) -> None:
        # Stores an r,c coordinate for where it exists
        # Stores references to incoming edges
        # Stores references to outgoing edges

        pass

class Edge():
    def __init__(self) -> None:
        # Stores reference to start node
        # Stores reference to end node
        # Stores length of edge

        pass


# Main code
def main():
    ### Map Newtork
    # Setup a register of nodes and edges
    # Initialise start node and first edge
    # set up a queue of edges to explore from. Initialise with first edge
    # >> start walking along an edge until a new node is found.
    # Create new node with this edge as incoming
    # Update the edge with distance and finishing node
    # Create new edges for all forks out of node and add to queue
    # Update node with outgoing edges
    # Store the new node and add the new start
    # Repeat from >> until queue is empty


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
