from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("Name")) 
ashay= True
# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255,0,0)
    global ashay
    ashay=False



# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255,0,0)
    global ashay
    ashay=False
    


# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255,0,0)
    global ashay
    ashay=False
    


@event(robot.when_play)
async def avoidCollision(robot):
     await robot.set_wheel_speeds(8,8)
     while True:
        if ashay == False:
            await robot.set_wheel_speeds(0, 0)
            break

        ir_reading = (await robot.get_ir_proximity()).sensors
        proximity = 4095 / (ir_reading[3] + 1)  # Calculate proximity
        if proximity <= 5.0:
            await robot.set_wheel_speeds(0, 0)
            await robot.set_lights_rgb(255,0,0)
            await robot.play_note(Note.D7, 1)
            break
        elif proximity > 5.0 and proximity <= 30.0:
            await robot.set_wheel_speeds(1, 1)  #  down to 1 cm/s
            await robot.set_lights(Robot.LIGHT_BLINK,Color(255,65,0))
            await robot.play_note(Note.D6, 0.1)
        elif proximity >30.0 and proximity <= 100.0:
            await robot.set_wheel_speeds(4, 4)  #  speed at 4 cm/s
            await robot.set_lights(Robot.LIGHT_BLINK,Color(255,234,0))
            await robot.play_note(Note.D5, 0.1)
        elif proximity > 100.0:
            await robot.set_wheel_speeds(8, 8)  #  speed at 8 cm/s
            await robot.set_lights(Robot.LIGHT_BLINK,Color(0,255,0))


# start the robot
robot.play()
