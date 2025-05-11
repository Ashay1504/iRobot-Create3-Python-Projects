from collections import deque

def createMazeDict(nXCells, nYCells, cellDim):
    mazeDict = {}
    for i in range(nXCells):
        for j in range(nYCells):
            mazeDict[(i, j)] = {
                'position': (i * cellDim, j * cellDim),
                'neighbors': [],
                'visited': False,
                'cost': 0
            }
    return mazeDict

nXCells, nYCells, cellDim = 2, 2, 10
mazeDict1 = createMazeDict(nXCells, nYCells, cellDim)
#print(mazeDict)



def addAllNeighbors(mazeDict, nXCells, nYCells):
    for i in range(nXCells):
        for j in range(nYCells):
            aNeighbors = [(i-1,j),(i,j+1),(i+1,j),(i,j-1)]
            for (x,y) in aNeighbors:
                if 0 <= x < nXCells and 0 <= y < nYCells:
                    mazeDict[(i, j)]['neighbors'].append((x,y))
                    if x == i and y == j:
                        continue
    return mazeDict

mazeDict = addAllNeighbors(mazeDict1,nXCells,nYCells)
#print(mazeDict)

    

def getRobotOrientation(heading):
    directions = ['E', 'N', 'W', 'S']
    index = round(heading / 90) % 4
    return directions[index]

#print(getRobotOrientation(361))
#print(getRobotOrientation(88.5))


def getPotentialNeighbors(currentCell, orientation):
    x, y = currentCell
    if orientation == 'E':
        return [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
    elif orientation == 'N':
        return [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    elif orientation == 'W':
        return [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]
    elif orientation == 'S':
        return [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
"""
print(getPotentialNeighbors((0,1),"E"))
print(getPotentialNeighbors((2,3),"S"))
"""


def isValidCell(cellIndices, nXCells, nYCells):
    x, y = cellIndices
    return 0 <= x < nXCells and 0 <= y < nYCells
"""
print(isValidCell((3,3), 4, 5))
print(isValidCell((1,2), 2, 2))
"""


def getWallConfiguration(IR0, IR3, IR6, threshold):
    def isWall(reading):
        return 4095 / (reading + 1) <= threshold

    leftWall = isWall(IR0)
    frontWall = isWall(IR3)
    rightWall = isWall(IR6)

    return [leftWall, frontWall, rightWall]
"""
print(getWallConfiguration(300, 200, 39, 100))
print(getWallConfiguration(23, 800, 10, 100))
"""


def getNavigableNeighbors(wallsAroundCell, potentialNeighbors, prevCell, nXCells, nYCells):
    navNeighbors = []
    if prevCell != None:
        navNeighbors.append(prevCell)
    for cell in potentialNeighbors:
        for i in range(len(wallsAroundCell)):
            if wallsAroundCell[i] == False:
                if potentialNeighbors[i] not in navNeighbors:
                    if isValidCell(cell,nXCells,nYCells):
                        navNeighbors.append(potentialNeighbors[i])
    return navNeighbors
"""
print(getNavigableNeighbors([True, True, False], [(1,2),(2,1),(1,0),(0,1)], (0,1), 2, 2))
print(getNavigableNeighbors([False, True, False], [(0,2),(1,3),(2,2),(1,1)], (1,1), 4, 4))
"""

def updateMazeNeighbors(mazeDict, currentCell, navNeighbors):
    for cell in mazeDict:
        if currentCell in mazeDict[cell]['neighbors']:
            if cell not in navNeighbors:
                mazeDict[cell]['neighbors'].remove(currentCell)
    mazeDict[currentCell]['neighbors'] = navNeighbors
    return mazeDict


def getNextMove(mazeDict, currentCell):
    neighbors = mazeDict[currentCell]['neighbors']
    
    # Filter out visited neighbors
    unvisited_neighbors = [neighbor for neighbor in neighbors if not mazeDict[neighbor]['visited']]

    if unvisited_neighbors:
        # If there are unvisited neighbors, find the one with the lowest cost
        nextMove = unvisited_neighbors[0]
        min_cost = mazeDict[unvisited_neighbors[0]]['cost']

        for neighbor in unvisited_neighbors[1:]:
            neighbor_cost = mazeDict[neighbor]['cost']
            if neighbor_cost < min_cost:
                nextMove = neighbor
                min_cost = neighbor_cost
    else:
        # If all neighbors are visited, find the one with the lowest cost
        nextMove = neighbors[0]
        min_cost = mazeDict[neighbors[0]]['cost']

        for neighbor in neighbors[1:]:
            neighbor_cost = mazeDict[neighbor]['cost']
            if neighbor_cost < min_cost:
                nextMove = neighbor
                min_cost = neighbor_cost

    return nextMove if nextMove else None


def checkCellArrived(currentCell, destination):
    return currentCell == destination
"""
print(checkCellArrived((4,3), (4,3)))
print(checkCellArrived((6,7), (7,6)))
"""


"""
The following implementation of the Flood Fill algorithm is
tailored for maze navigation. It updates the movement cost for
each maze cell as the robot learns about its environment. As
the robot moves and discovers navigable adjacent cells, it
gains new information, leading to frequent updates in the
maze's data structure. This structure tracks the layout and
traversal costs. With each step and discovery, the algorithm
recalculates the cost to reach the destination, adapting to
newly uncovered paths. This iterative process of moving,
observing, and recalculating continues until the robot reaches
its destination, ensuring an optimal path based on the robot's
current knowledge of the maze.
"""
def updateMazeCost(mazeDict, start, goal):
    for (i,j) in mazeDict.keys():
        mazeDict[(i,j)]["flooded"] = False
    queue = deque([goal])
    mazeDict[goal]['cost'] = 0
    mazeDict[goal]['flooded'] = True
    while queue:
        current = queue.popleft()
        current_cost = mazeDict[current]['cost']
        for neighbor in mazeDict[current]['neighbors']:
            if not mazeDict[neighbor]['flooded']:
                mazeDict[neighbor]['flooded'] = True
                mazeDict[neighbor]['cost'] = current_cost + 1
                queue.append(neighbor)
    return mazeDict

"""
This function prints the information from the dictionary as
a grid and can help you troubleshoot your implementation.
"""
def printMazeGrid(mazeDict, nXCells, nYCells, attribute):
    for y in range(nYCells - 1, -1, -1):
        row = '| '
        for x in range(nXCells):
            cell_value = mazeDict[(x, y)][attribute]
            row += '{} | '.format(cell_value)
        print(row[:-1])

