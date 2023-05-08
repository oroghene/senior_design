from Motor import Motor
import math
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'  # Change this to the correct port name for your Rplidar
lidar = RPLidar(PORT_NAME)
lidar.__init__(PORT_NAME, 115200,3,None)
lidar.connect()
lidar.set_pwm(550)

info = lidar.get_info()
health = lidar.get_health()
print("Info:\n", info, "\nHealth:\n", health, "\nIter scans:\n",lidar.iter_scans())

# Initialize motor and lidar objects
motor = Motor()

#Define car boundaries
LF = [135, 50] #lEFT FRONT CORNER, [DEGREES, DISTANCE]
RF = [205, 50] #RIGHT FRONT CORNER,[DEGREES, DISTANCE]
LB = [45, 150] #LEFT BACK CORNER,[DEGREES, DISTANCE]
RB = [315, 150] #RIGHT BACK CORNER,[DEGREES, DISTANCE]

def find_furthest_distance(points):
    paths = []
    walls = []
    temp = []
    for i in range(1,len(points)+1):
        if points[i][1] >= points[i-1][1]*1.05:
            temp.append(points[i][1])
        else:
            paths.append(temp)
            temp = []
    pass
    return paths[max(len(elem) for elem in paths)]

def orient_car(t):
    motor.setMotorModel(1500,1500,-1000,-1000) # Turn Left
    time.sleep(t)
    motor.setMotorModel(0,0, 0, 0)
    return

def detect_obstacles(points):
    pass
    return True

def clear_path_ahead(points):
    front = np.array([0,700])
    for p in points:
        if (p[0] < 270) and (p[0] > 90):
            front = np.vstack([front, p])
    print("Front:", min(front[:,1]))
    if min(front[:,1]) >= 250:
        print("Front is Clear")
        return True
    else:
        print("Obstruction!", front[:,1].any() >= 50)
        return False

# Define main function to run the car autonomously
def main():
    try:
        z = 0
        while True:
           
           for i, data in enumerate(lidar.iter_scans()):
                points = [[a, d] for (_, a, d) in list(data)]
                print(i, points)
             
                #Check if it is safe to move forward
                clear = True
                clear = clear_path_ahead(points)
                
                
                if clear is True:
                    motor.setMotorModel(-500, -500, -500, -500) # Move forward
                    print ("The car is moving forward")
                else:
                    motor.setMotorModel(0, 0, 0, 0)
                    time.sleep(2)
                    orient_car(1)
                    
                

    except KeyboardInterrupt:
        # Stop the car
        motor.setMotorModel(0, 0, 0, 0)
        
        # Stop the Lidar
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == '__main__':
    main()

