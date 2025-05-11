from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import math as m

# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("Name"))

index_Max= 0
ashay= False

IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]

def proximityValue(ir_reading):
    return 4095 / (ir_reading + 1)

def maximumProximity(readings):
    global index_Max
    highest_Proximity = readings[0]
    for i in readings:
        if i > highest_Proximity: 
            highest_Proximity = i 
    return highest_Proximity

# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    global ashay
    ashay= True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights(Robot.LIGHT_ON, Color(255, 0, 0))
    

# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    global ashay
    ashay= True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights(Robot.LIGHT_ON, Color(255, 0, 0))

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global ashay
    ashay= True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights(Robot.LIGHT_ON, Color(255, 0, 0))


@event(robot.when_play)
async def robotPong(robot):
    await robot.set_wheel_speeds(15, 15)
    await robot.set_lights(Robot.LIGHT_SPIN, Color(0, 255, 255))
    count=0
    while True:
        if ashay == False:
            reading = (await robot.get_ir_proximity()).sensors #list
            proximity = maximumProximity(reading)
            n = proximityValue(proximity)
            if n <= 20:
                await robot.set_wheel_speeds(0, 0)
                approachAngle = getApproachAngle(reading, IR_ANGLES)
                if approachAngle > 0:
                    reflectionAngle = 180 - 2 * approachAngle
                    await robot.turn_left(reflectionAngle)
                    if count%2!=0:
                        await robot.set_lights(Robot.LIGHT_ON,Color(0,100,100))
                        count+=1
                    elif count%2==0:
                        await robot.set_lights(Robot.LIGHT_ON,Color(255,0,255))
                        count+=1
                    
                else:
                    reflectionAngle = 180 + 2 * approachAngle
                    await robot.turn_right(reflectionAngle)
                    if count%2!=0:
                        await robot.set_lights(Robot.LIGHT_ON,Color(0,100,100))
                        count+=1
                    elif count%2==0:
                        await robot.set_lights(Robot.LIGHT_ON,Color(255,0,255))
                        count+=1
            await robot.set_wheel_speeds(15, 15)
        else:
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights(Robot.LIGHT_ON, Color(255,0,0))


def getApproachAngle(reading, angles):
    global IR_ANGLES
    highest_Proximity = reading[0]
    for b in reading:
        if b > highest_Proximity:
            highest_Proximity = b
    index= reading.index(highest_Proximity)
    approachAngle = angles[index]
    return approachAngle




# ask for desired
robot.play()
