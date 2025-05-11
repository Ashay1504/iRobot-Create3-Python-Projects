from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("Name"))

CORRECT_CODE = "34421"
user_passcode = ""

# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    global user_passcode
    user_passcode += "1"
    print(user_passcode)

    if len(user_passcode) == len(CORRECT_CODE):
        await robot.play_note(Note.C5, 1)
        await checkUserCode(robot)
    else:
        await robot.play_note(Note.C5, 1)
  
    


# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    global user_passcode
    user_passcode += "2"
    print(user_passcode)

    if len(user_passcode) == len(CORRECT_CODE):
        await robot.play_note(Note.D5, 1)
        await checkUserCode(robot)
    else:
        await robot.play_note(Note.D5, 1)
    
    


# LEFT BUMP
@event(robot.when_bumped, [True, False])  # [left, right]
async def when_left_bumped(robot):
    global user_passcode
    user_passcode += "3"
    print(user_passcode)

    if len(user_passcode) == len(CORRECT_CODE):
        await robot.play_note(Note.E5, 1)
        await checkUserCode(robot)
    else:
        await robot.play_note(Note.E5, 1)
     
    


# RIGHT BUMP
@event(robot.when_bumped, [False, True]) # [left, right]
async def when_right_bumped(robot):
    global user_passcode
    user_passcode += "4"
    print(user_passcode)


    if len(user_passcode) == len(CORRECT_CODE):
        await robot.play_note(Note.F5, 1)
        await checkUserCode(robot)
    else:
        await robot.play_note(Note.F5, 1)
     
    


async def checkUserCode(robot):
    global user_passcode
    global CORRECT_CODE
    if user_passcode == CORRECT_CODE:
        await robot.play_note(Note.G4, 3)
        await robot.set_lights(Robot.LIGHT_SPIN,Color(255,0,0))
        await robot.set_lights(Robot.LIGHT_SPIN,Color(0,255,0))
        await robot.set_lights(Robot.LIGHT_SPIN,Color(0,0,255))  
    else:
        await robot.play_note(Note.A4, 3)  
        await robot.set_lights(Robot.LIGHT_BLINK,Color(255,0,0))
        user_passcode = ""    



@event(robot.when_play)
async def play(robot):
    print("ITS READY")
    
robot.play()
