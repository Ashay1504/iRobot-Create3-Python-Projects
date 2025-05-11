import math as m

def getCorrectionAngle(heading):
    correctionAngle = heading - 90
    return int(correctionAngle)
    pass
"""
print(getCorrectionAngle(135.6))
print(getCorrectionAngle(25))
"""


def getAngleToDestination(currentPosition,destination):
    X = destination[0] - currentPosition[0]
    Y = destination[1] - currentPosition[1]
    angle = m.degrees(m.atan2(X, Y))
    return int(angle)

    pass
"""
currentPosition = (1, 1)
destination = (5, 3)
print(getAngleToDestination(currentPosition, destination))

currentPosition = (5, 5)
destination = (1, 1)
print(getAngleToDestination(currentPosition, destination))
"""


def getMinProxApproachAngle(readings, angles):
    proximities = [4095 / (reading + 1) for reading in readings]
    min_proximity_index = proximities.index(min(proximities))
    return proximities[min_proximity_index], angles[min_proximity_index]
    pass
"""
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
readings = [4, 347, 440, 408, 205, 53, 27]
print(getMinProxApproachAngle(readings, IR_ANGLES))

IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
readings = [731, 237, 202, 229, 86, 120, 70]
print(getMinProxApproachAngle(readings, IR_ANGLES))
"""


def checkPositionArrived(current_position, destination, threshold):
    x_distance = current_position[0] - destination[0]
    y_distance = current_position[1] - destination[1]
    distance = m.sqrt(x_distance**2 + y_distance**2)
    return distance <= threshold
    pass
"""
print(checkPositionArrived((97, 99), (100, 100), 5.0))
print(checkPositionArrived((50, 50), (45, 55), 5))
"""
