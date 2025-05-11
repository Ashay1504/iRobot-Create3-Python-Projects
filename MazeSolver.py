from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import AuxMazeSolver as aux

# === CREATE ROBOT OBJECT
robot = Create3(Bluetooth("C-3PO"))

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_ARRIVED = False

# === BUILD MAZE DICTIONARY
N_X_CELLS = 3
N_Y_CELLS = 3
CELL_DIM = 50
MAZE_DICT = aux.createMazeDict(N_X_CELLS, N_Y_CELLS, CELL_DIM)
MAZE_DICT = aux.addAllNeighbors(MAZE_DICT, N_Y_CELLS, N_Y_CELLS)

# === DEFINING ORIGIN AND DESTINATION
PREV_CELL = None
START = (2,0)
CURR_CELL = START
DESTINATION = (0,0)
MAZE_DICT[CURR_CELL]["visited"] = True

# === PROXIMITY TOLERANCES
WALL_THRESHOLD = 80

# ==========================================================
# FAIL SAFE MECHANISMS

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
    global HAS_COLLIDED
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255,0,0)
    HAS_COLLIDED = True
    
# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global HAS_COLLIDED
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255,0,0)
    HAS_COLLIDED = True
    
# ==========================================================
# MAZE NAVIGATION AND EXPLORATION

# === NAVIGATE TO CELL
async def navigateToNextCell(robot, nextCell, orientation):
    global MAZE_DICT, PREV_CELL, CURR_CELL, CELL_DIM
    neighbors = aux.getPotentialNeighbors(CURR_CELL,orientation)
    for i in range(len(neighbors)):
        if i == 0:
            if neighbors[i] == nextCell:
                await robot.turn_left(90)
                await robot.move(CELL_DIM)
        elif i == 1:
            if neighbors[i] == nextCell:
                await robot.move(CELL_DIM)
        elif i == 2:
            if neighbors[i] == nextCell:
                await robot.turn_right(90)
                await robot.move(CELL_DIM)
        else:
            await robot.turn_left(180)
            await robot.move(CELL_DIM)





# === EXPLORE MAZE
@event(robot.when_play)
async def navigateMaze(robot):
    global HAS_COLLIDED, HAS_ARRIVED
    global PREV_CELL, CURR_CELL, START, DESTINATION
    global MAZE_DICT, N_X_CELLS, N_Y_CELLS, CELL_DIM, WALL_THRESHOLD
    while HAS_COLLIDED == False and HAS_ARRIVED == False:
        if aux.checkCellArrived(CURR_CELL,DESTINATION):
            HAS_ARRIVED = True
            await robot.set_lights(Robot.LIGHT_ON,Color(0,255,0))
            break
        pos = (await robot.get_position())
        orientation = aux.getRobotOrientation(pos.heading)
        potentialNeighbors = aux.getPotentialNeighbors(CURR_CELL,orientation)
        readings = (await robot.get_ir_proximity()).sensors
        wallList = aux.getWallConfiguration(readings[0],readings[3],readings[6],WALL_THRESHOLD)
        navNeighbors = aux.getNavigableNeighbors(wallList,potentialNeighbors)
        MAZE_DICT = aux.updateMazeNeighbors(MAZE_DICT,CURR_CELL,navNeighbors)
        MAZE_DICT = aux.updateMazeCost(MAZE_DICT,START,DESTINATION)


        nextCell = aux.getNextCell(MAZE_DICT,CURR_CELL)

        await navigateToNextCell(robot,nextCell,orientation)

        CURR_CELL = nextCell





# start the robot
robot.play()
