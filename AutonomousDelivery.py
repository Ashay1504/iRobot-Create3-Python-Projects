from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
import math as m
import AuxAutonomousDelivery as aux

# === CREATE ROBOT OBJECT
robot = Create3(Bluetooth("SOPHIA"))

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_REALIGNED = False
HAS_FOUND_OBSTACLE = False
HAS_ARRIVED = False

# === OTHER NAVIGATION VARIABLES
SENSOR2CHECK = 0
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
DESTINATION = (-140, 90)
ARRIVAL_THRESHOLD = 5
angle_to_move = 0


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
def getCorrectionAngle(heading):
    correctionAngle = heading - 90
    return int(correctionAngle)
    

def getAngleToDestination(currentPosition,destination):
    X = destination[0] - currentPosition[0]
    Y = destination[1] - currentPosition[1]
    angle = m.degrees(m.atan2(X, Y))
    return int(angle)

def getMinProxApproachAngle(readings, angles):
    proximities = [4095 / (reading + 1) for reading in readings]
    min_proximity_index = proximities.index(min(proximities))
    return proximities[min_proximity_index], angles[min_proximity_index]

# === REALIGNMENT BEHAVIOR
async def realignRobot(robot):
    global DESTINATION
    global HAS_REALIGNED
    currentPosition= await robot.get_position()
    angle_to_destination= getAngleToDestination(currentPosition,DESTINATION)
    angle=getCorrectionAngle(angle_to_destination)
    robot.turn_right(angle)
    HAS_REALIGNED = True



# === MOVE TO GOAL
async def moveTowardGoal(robot):
    global HAS_FOUND_OBSTACLE, IR_ANGLES, SENSOR2CHECK,angle_to_move
    reading = (await robot.get_ir_proximity()).sensors
    for i in range(len(reading)):
        if reading[i] == 20.0:
            angles = IR_ANGLES[i]
            SENSOR2CHECK = i
            HAS_FOUND_OBSTACLE == True
    angle_to_move = 90 - angles
    robot.turn_right(angle_to_move)




# === FOLLOW OBSTACLE
async def followObstacle(robot):
    global HAS_FOUND_OBSTACLE, HAS_REALIGNED, SENSOR2CHECK,angle_to_move
    await robot.set_wheel_speeds(5,5)
    reading = (await robot.get_ir_proximity()).sensors
    if reading[SENSOR2CHECK]< 20.0:
        if angle_to_move < 0 :
            await robot.turn_left(3)
        else:
            await robot.turn_right(3)
    elif reading[SENSOR2CHECK]< 100.0:
        await robot.move(50)
        HAS_FOUND_OBSTACLE = False
        HAS_REALIGNED = False    
    




# === NAVIGATION TO DELIVERY
@event(robot.when_play)
async def makeDelivery(robot):
    global HAS_ARRIVED, HAS_COLLIDED, HAS_REALIGNED, HAS_FOUND_OBSTACLE
    global DESTINATION, ARRIVAL_THRESHOLD, IR_ANGLES, SENSOR2CHECK
    while HAS_COLLIDED == False and HAS_ARRIVED == False: 
        if HAS_REALIGNED == False:
            await realignRobot(robot)
        if HAS_FOUND_OBSTACLE == True:
            await followObstacle(robot)
        if HAS_FOUND_OBSTACLE == False and HAS_REALIGNED == True:
            await moveTowardGoal(robot)


    




# start the robot
robot.play()

