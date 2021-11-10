import copy
import time


# CLASS FUNCTIONS
class Node(object):

    def __init__(self, puzzle, costG, costH):
        self.puzzle = puzzle
        self.costG = costG
        self.costH = costH


# MAIN SEARCH FUNCTIONS

'''
GIVEN PSUEDOCODE FOR GENERAL SEARCH:
function genSearch(problem, QueueingFunction)
    nodes = makeQueue(makeNode(problem.InitState)
    loop do
        if empty(nodes) return failure
        node = removeFront(nodes)
        if problem.goalState(node.State) succeeds return node
        node = Queuing Function(nodes, expand(node,problem.ops)
'''


# General Search code for all 3 algorithms. Each algorithm go through this while loop to search for the puzzle
def general_search(currPuzzle, goalPuzzle, searchAlg):
    qSearch = []
    node = Node(currPuzzle, 0, 0)

    # Uniform Cost search's heurisitic is 0, while misplaced tile and manhattan distance have their own to calculate
    if searchAlg == 2:
        node.costH = misplacedTileHeuristic(node, goalPuzzle)
    elif searchAlg == 3:
        node.costH = manhattanDistanceHeuristic(node, goalPuzzle)

    maxNodes = 0
    expandedNodes = 0
    # nodes = makeQueue(makeNode(problem.InitState)
    qSearch.append(node)
    searchTree = []
    while True:
        # if empty(nodes) return failure
        if qSearch is None:
            return "Failure"
        if len(qSearch) > maxNodes:
            maxNodes = len(qSearch)

        # node = removeFront(nodes)
        lowCost = float('inf')
        index = 0
        for i in qSearch:
            if i.costG + i.costH < lowCost:
                lowCost = i.costG + i.costH
                index = qSearch.index(i)
        node = qSearch.pop(index)

        if meetGoal(node.puzzle, goalPuzzle):
            print("GOAL!")
            print("Solution was at depth,", node.costG)
            print("number of nodes expanded:", expandedNodes)
            print("maximum nodes in queue:", maxNodes)
            return 0

        qSearch, searchTree, numChildNodes = queueingFunction(searchAlg, qSearch, node, index, goalPuzzle, searchTree)
        expandedNodes += numChildNodes


# Queueing function that was called in the general search function is used to make the search tree to find the
# solution. Depending on what the user chose, each part adds the child node that is the lowest total cost.
def queueingFunction(searchAlg, qSearch, node, index, goalPuzzle, searchTree):
    print("The best state to expand with a g(n) is", node.costG, "and h(n) is", node.costH, "...")
    searchTree, childQueue = expandNodes(node, searchTree)

    for i in range(3):
        print(node.puzzle[i])

    if searchAlg == 1:
        for i in childQueue:
            if i.puzzle not in searchTree:
                qSearch.insert(index, i)
                index += 1
                searchTree.append(i.puzzle)
    else:
        for i in childQueue:
            if searchAlg == 3:
                i.costH = manhattanDistanceHeuristic(i, goalPuzzle)
            if searchAlg == 2:
                i.costH = misplacedTileHeuristic(i, goalPuzzle)

            if i not in searchTree:
                qSearch.append(i)
                searchTree.append(i.puzzle)

    return qSearch, searchTree, len(childQueue)


# This function expands the parent node by figuring out if the blank space is able to move up, down, left, or right.
# If it can, the child node is added to the queue, which then is returned to the expanded node function to be able to
# find the child node with the lowest cost.
def expandNodes(parentNode, searchTree):
    childQueue = []
    function = 0

    if moveUp(parentNode) == 0:
        function = 1
        searchTree, childQueue = childAppendToQueue(parentNode, searchTree, childQueue, function)

    if moveDown(parentNode) == 0:
        function = 2
        searchTree, childQueue = childAppendToQueue(parentNode, searchTree, childQueue, function)

    if moveLeft(parentNode) == 0:
        function = 3
        searchTree, childQueue = childAppendToQueue(parentNode, searchTree, childQueue, function)

    if moveRight(parentNode) == 0:
        function = 4
        searchTree, childQueue = childAppendToQueue(parentNode, searchTree, childQueue, function)

    return searchTree, childQueue


# The misplaced tile heuristic is calculated by comparing the current puzzle and the goal state puzzle. The puzzles
# are iterated through to figure how many tiles are not matching, excluding the empty space.
def misplacedTileHeuristic(node, goalState):
    misplaceTileCount = 0
    for i in range(3):
        for j in range(3):
            if node.puzzle[i][j] != 0 and node.puzzle[i][j] != goalState[i][j]:
                misplaceTileCount += 1

    return misplaceTileCount


# The manhattan distance heuristic is calculated similarly to the misplaced tile, except it calculates how many spaces
# it is from its goal location.
def manhattanDistanceHeuristic(node, goalState):
    heuristicCost = 0
    for i in range(3):
        for j in range(3):
            if node.puzzle[i][j] != goalState[i][j] and node.puzzle[i][j] != 0:
                heuristicCost += manhattDistance(node, goalState, i, j)

    return heuristicCost


def manhattDistance(node, goalState, x, y):
    distance = 0
    tile = node.puzzle[x][y]

    intX = 0
    intY = 0
    for i in range(3):
        for j in range(3):
            if goalState[i][j] == tile:
                intX = i
                intY = j
                break

    distance = abs(intX - x) + abs(intY - y)
    return distance


# SEARCH HELPER FUNCTIONS
# This helper function for the expanded node function adds the node to the queues and moves based on which action it had
# went through
def childAppendToQueue(parentNode, searchTree, childQueue, function):
    searchTree.append(parentNode)
    child = copy.deepcopy(parentNode)
    child.costG += 1
    childQueue.append(child)
    if function == 1:
        moveDown(parentNode)
    if function == 2:
        moveUp(parentNode)
    if function == 3:
        moveRight(parentNode)
    if function == 4:
        moveLeft(parentNode)

    return searchTree, childQueue


# This helper function compares the current puzzle with the goal puzzle to see if they match or not.
def meetGoal(currPuzzle, goalPuzzle):
    for i in range(3):
        for j in range(3):
            if currPuzzle[i][j] != goalPuzzle[i][j]:
                return False

    return True


# These four functions take in a node and move in the direction it is asked to and ensures it does not move farther than
# the boundaries.
def moveUp(node):
    indX = 0
    indY = 0
    for i in range(3):
        for j in range(3):
            if i == 0 and node.puzzle[i][j] == 0:
                # print("Can't move up!")
                return -1
            if node.puzzle[i][j] == 0:
                indX = i
                indY = j
                break

    node.puzzle[indX][indY] = node.puzzle[indX - 1][indY]
    node.puzzle[indX - 1][indY] = 0
    return 0


def moveDown(node):
    indX = 0
    indY = 0
    for i in range(3):
        for j in range(3):
            if i == 2 and node.puzzle[i][j] == 0:
                # print("Can't move down!")
                return -1
            if node.puzzle[i][j] == 0:
                indX = i
                indY = j
                break

    if indX != 2:
        node.puzzle[indX][indY] = node.puzzle[indX + 1][indY]
        node.puzzle[indX + 1][indY] = 0
    return 0


def moveLeft(node):
    indX = 0
    indY = 0
    for i in range(3):
        for j in range(3):
            if j == 0 and node.puzzle[i][j] == 0:
                # print("Can't move left!")
                return -1
            if node.puzzle[i][j] == 0:
                indX = i
                indY = j
                break

    node.puzzle[indX][indY] = node.puzzle[indX][indY - 1]
    node.puzzle[indX][indY - 1] = 0
    return 0


def moveRight(node):
    indX = 0
    indY = 0
    for i in range(3):
        for j in range(3):
            if j == 2 and node.puzzle[i][j] == 0:
                # print("Can't move right!")
                return -1
            if node.puzzle[i][j] == 0:
                indX = i
                indY = j
                break

    if indY != 2:
        node.puzzle[indX][indY] = node.puzzle[indX][indY + 1]
        node.puzzle[indX][indY + 1] = 0
    return 0


# MAIN FUNCTIONS
# Create a puzzle based on user input
def createOwn():
    print("Enter your puzzle, using a zero to represent the blank. ")
    puzzle = []

    for i in range(9):
        puzzle.append(int(input("Enter puzzle number")))

    return puzzle


# Convert puzzle into 2D Array for better representation
def convertToBoard(puzzle):
    newPuzz = []
    x = 0
    for i in range(3):
        row = []
        for j in range(3):
            row.append(puzzle[x])
            x += 1
        newPuzz.append(row)
    return newPuzz


def main():
    choice = int(
        input("Welcome to my 8-puzzle solver. Type '1' to use a default puzzle or type '2' to create your own."))
    puzzle = []
    goalState = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    defaultPuzzleDict = {"trivial": [1, 2, 3, 4, 5, 6, 7, 8, 0],
                         "veryEasy": [1, 2, 3, 4, 5, 6, 7, 0, 8],
                         "easy": [1, 2, 0, 4, 5, 3, 7, 8, 6],
                         "doable": [0, 1, 2, 4, 5, 3, 7, 8, 6],
                         "oh_boy": [8, 7, 1, 6, 0, 2, 5, 4, 3],
                         "testing": [1, 2, 3, 4, 0, 6, 7, 5, 8]}

    if choice == 1:
        puzzleDifficulty = input("Choose difficulty: (trivial), (veryEasy), (easy), (doable), (oh_boy), (testing)")
        puzzle = defaultPuzzleDict.get(puzzleDifficulty)
    elif choice == 2:
        puzzle = createOwn()
    else:
        print("Input not valid")

    puzzle = convertToBoard(puzzle)
    goalState = convertToBoard(goalState)

    choice = int(input("Select algorithm. \n(1) for Uniform Cost Search \n(2) for Misplace Tile Heuristic "
                       "\n(3) for Manhattan Distance Heuristic."))

    runningTime = 0
    if choice == 1 or choice == 2 or choice == 3:
        start_time = time.time()
        general_search(puzzle, goalState, choice)
        end_time = time.time()
        runningTime = end_time - start_time
    else:
        print("Input not valid")

    print("Algorithm took", runningTime, "seconds")


main()
