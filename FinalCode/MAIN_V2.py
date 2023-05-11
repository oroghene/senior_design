from Motor import Motor
import math
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rplidar import RPLidar
#import socket

# Set up lidar 
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

#Define car boundaries and parameters
LF = [135, 50] #lEFT FRONT CORNER, [DEGREES, DISTANCE]
RF = [205, 50] #RIGHT FRONT CORNER,[DEGREES, DISTANCE]
LB = [45, 150] #LEFT BACK CORNER,[DEGREES, DISTANCE]
RB = [315, 150] #RIGHT BACK CORNER,[DEGREES, DISTANCE]

FS = (-500, -500, -500, -500) #Foward speed
RS = (500, 500, 500, 500) #Reverse speed
RS = (-1000, -1000, 1500, 1500) #Right turn
LF = (1500, 1500, -1000, -1000) #Left turn
NS = (0,0,0,) #No speed

# Set up functions for car control
def move_car(speed):
    motor.setMotorModel(speed) # Move forward or back
    if speed < 0:
        print ("The car is moving forward...")
    elif speed > 0:
        print ("The car is moving back...")
    return

def stop_car():
    motor.setMotorModel(NS)
    print("The car has stopped.")
    return

def orient_car(points):
    angle = np.average(points,axis=0)[0] # Find midpoint of angles
    print('Best path is at', angle, 'degrees.')
    print("Orienting car...")
    
    if angle <= 180:
        print('Turning', angle, 'degrees to the right...')
        motor.setMotorModel(RS) # Turn Right
        t = (angle/10)*0.5
        time.sleep(t)
        
    elif angle > 180:
        print('Turning', 360 - angle, 'degrees to the left...')
        motor.setMotorModel(LS) # Turn Left
        t = ((360 - angle)/10)*0.5
        time.sleep(t)
        
    print('Done orienting.')
    motor.setMotorModel(NS)
    return

def align_car(points):
    print("Adjusting orientation to align path...")
    angle = np.average(points,axis=0)[0] #Change this to offset angle
    
    if angle <= 180:
        print('Turning', angle, 'degrees to the right...')
        motor.setMotorModel(RS) # Turn Right
        t = (angle/10)*0.5
        time.sleep(t)
        
    elif angle > 180:
        print('Turning', 360 - angle, 'degrees to the left...')
        motor.setMotorModel(LS) # Turn Left
        t = ((360 - angle)/10)*0.5
        time.sleep(t)
        
    print('Done orienting.')
    motor.setMotorModel(FS) # Keep moving forward
    pass
    return
    

# Set up functions for obstacle detection and navigation
def clear_path_ahead(points):
    front = np.array([0,700])
    for p in points:
        if (p[0] < 270) and (p[0] > 90):
            front = np.vstack([front, p])
    #print("Closest obstacle is", min(front[:,1]),"mm away")
    if min(front[:,1]) >= 250:
        print("Front is Clear")
        return True
    else:
        print("Obstruction in", min(front[:,1]),"mm")
        return False

def find_furthest_distance(points):
    print("Finding best path (most open spaces)...")
    start = [] # Holds indices of first point in paths
    end = [] # Holds indices of last points in paths
    paths = np.array([0,0]) # Initiate array to hold paths points
    best_path = np.array([0,0]) # Initiate array to hold points for best path
    N = [] # Initiate list to hold sizes of paths

    avg = np.average(points,axis=1)[1] # Find average distance of all points
    
    for i in range(1,len(points)): # Find points further than the average distance
        if (points[i][1] > avg) and (len(start) == len(end)):
            start.append(i)
        elif (points[i][1] < avg) and (len(start) != len(end)):
            end.append(i-1)
        elif (points[i][1] > avg) and (len(start) != len(end)):
            paths = np.vstack([paths,points[i]])
            
    if (len(start) != len(end)): # Close the loop (360 deg and 0 deg)
        start[0] = start[-1]
        start = start[:-1]
        
    for i in range(0,len(start)-1): # Create list of sizes of paths
        n = end[i] - start[i]
        N.append(n)
        
    for i in range(0,len(start)-1): # Create array of path points
        for j in range(start[i],end[i]):
            paths = np.vstack([paths,points[j]])
            
    best = N.index(max(N)) # Find path with most points
                   
    for i in range(start[best], end[best]): # Create an array of points with the "best" path
        best_path = np.vstack([best_path,points[i]])
                   
    paths = paths[1:,:]
    best_path = best_path[1:,:]
    
    print('Done finding best path.')
    
    return best_path

def detect_obstacles(points):
    pass
    return True

# Set up server-client function
def car_server():
    pass
    return
    
# Define main function to run the car autonomously
def main():
    try:
        while True:
           
           # Read lidar scan data 
           for i, data in enumerate(lidar.iter_scans()): 
                points = [[a, d] for (_, a, d) in list(data)]
                #print(i, points)
             
                #Check if it is safe to move forward
                if clear_path_ahead(points) is True:
                    # If path is clear, move forward
                    move_car(FS) 
                else:
                    # If there is an obstacle
                    stop_car() 
                    time.sleep(2)
                    # Find furthest distance and orient car in that direction
                    fd = find_furthest_distance(points) 
                    orient_car(fd) 
                    
                

    except KeyboardInterrupt: # If CTRL+C is pressed
        # Stop the car
        stop_car()
        
        # Stop the Lidar
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == '__main__':
    main()

