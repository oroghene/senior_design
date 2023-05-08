from Motor import Motor
from Lidar import Lidar
import math

# Initialize motor and lidar objects
motor = Motor()
lidar = Lidar()

# Define constants for motor control
FORWARD_SPEED = 2000
BACKWARD_SPEED = -2000
LEFT_SPEED = -500
RIGHT_SPEED = 500

# Define function to calculate distance between two points
def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

# Define function to find furthest distance without an obstacle
def find_furthest_distance():
    # Read lidar data
    data = lidar.get_data()

    # Find furthest distance without an obstacle
    max_distance = 0
    max_x, max_y = 0, 0
    for point in data:
        x, y = point
        d = distance(0, 0, x, y)
        if d > max_distance:
            max_distance = d
            max_x, max_y = x, y

    return max_distance, max_x, max_y

# Define function to orient the car in the direction of the furthest distance
def orient_car(max_x, max_y):
    angle = math.atan2(max_y, max_x)
    angle_degrees = math.degrees(angle)
    if angle_degrees < -45:
        motor.setMotorModel(0, 0, LEFT_SPEED, RIGHT_SPEED)
    elif angle_degrees > 45:
        motor.setMotorModel(RIGHT_SPEED, LEFT_SPEED, 0, 0)
    else:
        motor.setMotorModel(FORWARD_SPEED, FORWARD_SPEED, FORWARD_SPEED, FORWARD_SPEED)

# Define main function to run the car autonomously
def main():
    try:
        while True:
            # Find furthest distance without an obstacle
            max_distance, max_x, max_y = find_furthest_distance()

            # Orient the car in the direction of the furthest distance
            orient_car(max_x, max_y)

    except KeyboardInterrupt:
        # Stop the car
        motor.setMotorModel(0, 0, 0, 0)

if __name__ == '__main__':
    main()
