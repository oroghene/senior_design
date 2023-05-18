from Motor import Motor
import math
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rplidar import RPLidar
import socket

# =============== CLIENT ===============
HEADER = 64
PORT = 8000
# SERVER = "127.0.0.1"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'client:\n{client}')
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message) # send to server
    print(client.recv(2048).decode(FORMAT))

send('Hello World')
input()
send('Casamigos')
input()
send('For my amigos')
input()
send('It\'s gone')
# send(DISCONNECT_MESSAGE)
# =============== CLIENT ===============

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
LF = [135, 150] #lEFT FRONT CORNER, [DEGREES, DISTANCE]
RF = [205, 150] #RIGHT FRONT CORNER,[DEGREES, DISTANCE]
LB = [45, 250] #LEFT BACK CORNER,[DEGREES, DISTANCE]
RB = [315, 250] #RIGHT BACK CORNER,[DEGREES, DISTANCE]

FS = (-2000, -2000, -2000, -2000) #Foward speed
BS = (500, 500, 500, 500) #Reverse speed
RS = (-2000, -2000, 2500, 2500) #Right turn
LS = (2000, 2000, -2500, -2500) #Left turn
NS = (0,0,0,0) #No speed

# Set up functions for car control
def move_car(speed):
    motor.setMotorModel(speed[0],speed[1],speed[2],speed[3]) # Move forward or back
    if speed[0] < 0:
        print ("The car is moving forward...")
    elif speed[0] > 0:
        print ("The car is moving back...")
    return

def stop_car():
    motor.setMotorModel(NS[0],NS[1],NS[2],NS[3])
    print("The car has stopped.")
    return

def orient_car(points):
    angle = np.average(points,axis=0)[0] # Find midpoint of angles
    print('Best path is at', angle, 'degrees.')
    print("Orienting car...")
    
    if angle >= 180:
        print('Turning', angle, 'degrees to the right...')
        motor.setMotorModel(RS[0],RS[1],RS[2],RS[3]) # Turn Right
        t = ((angle-180)/9)*0.0825
        time.sleep(t)
        
    elif angle < 180:
        print('Turning', 360 - angle, 'degrees to the left...')
        motor.setMotorModel(LS[0],LS[1],LS[2],LS[3]) # Turn Left
        t = ((180-angle)/9)*0.0825
        time.sleep(t)
        
    print('Done orienting.')
    motor.setMotorModel(NS[0],NS[1],NS[2],NS[3])
    return

def align_car(points):
    print("Adjusting orientation to align path...")
    angle = np.average(points,axis=0)[0] #Change this to offset angle
    
    if angle <= 180:
        print('Turning', angle, 'degrees to the right...')
        motor.setMotorModel(RS[0],RS[1],RS[2],RS[3]) # Turn Right
        t = (angle/10)*0.1
        time.sleep(t)
        
    elif angle > 180:
        print('Turning', 360 - angle, 'degrees to the left...')
        motor.setMotorModel(LS[0],LS[1],LS[2],LS[3]) # Turn Left
        t = ((360 - angle)/10)*0.1
        time.sleep(t)
        
    print('Done orienting.')
    motor.setMotorModel(FS[0],FS[1],FS[2],FS[3]) # Keep moving forward
    pass
    return
    

# Set up functions for obstacle detection and navigation
def clear_path_ahead(points):
    front = np.array([[0,700]])
    for p in points:
        if (p[0] < 250) and (p[0] > 70):
            front = np.vstack([front, p])
    #print("Closest obstacle is", min(front[:,1]),"mm away")
    print("Front",min(front[:,1]))
    #if min(front[:,1]) >= 250:
    if min(front[:,1]) <= 250:
        print("Obstruction in", min(front[:,1]),"mm")
        return False
    else:
        print("Front is Clear")
        return True

def find_furthest_distance(points):
    try:
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
        if len(N) > 1:        
            best = N.index(max(N)) # Find path with most points
        else:
            print("Failed to find best path")
            return [[90, 1000],[180,1000]]
                       
        for i in range(start[best], end[best]): # Create an array of points with the "best" path
            best_path = np.vstack([best_path,points[i]])
        
        print("Paths:", paths)
        print("Best path:", best_path)
        paths = paths[1:,:]
        best_path = best_path[1:,:]

        print('Done finding best path.')
        
        return best_path
    
    except IndexError:
        print("Failed to find best path\n Turning around")
        print('Backing up...')
        motor.setMotorModel(BS[0],BS[1],BS[2],BS[3]) # Turn Right
        t = 1
        time.sleep(t)
        return [[360, 1000],[360,1000]]
'''
def find_furthest_distance(points, angle_gap=10):
    try:
        print("Finding best path (most open spaces)...")
        start = [] # Holds indices of first point in paths
        end = [] # Holds indices of last points in paths
        paths = np.array([0,0]) # Initiate array to hold paths points
        best_path = np.array([0,0]) # Initiate array to hold points for best path
        N = [] # Initiate list to hold sizes of paths

        # Find the angles where no data is returned by the LIDAR sensor
        gap_start = None
        for i in range(len(points)):
            if points[i][1] > 0:
                if gap_start is not None:
                    if i - gap_start > angle_gap:
                        start.append(gap_start)
                        end.append(i)
                        gap_start = None
                if gap_start is None:
                    paths = np.vstack([paths, points[i]])
            else:
                if gap_start is None:
                    gap_start = i

        # If there's a gap wider than the specified angle gap, return it as the best path
        if len(start) == 0:
            print("No open paths found, returning widest gap.")
            max_gap_start = None
            max_gap_end = None
            max_gap_size = 0
            gap_start = None
            for i in range(len(points)):
                if points[i][1] == 0:
                    if gap_start is None:
                        gap_start = i
                    else:
                        gap_size = i - gap_start
                        if gap_size > max_gap_size:
                            max_gap_start = gap_start
                            max_gap_end = i
                            max_gap_size = gap_size
                        gap_start = None
            if max_gap_start is not None:
                best_path = points[max_gap_start:max_gap_end]
        else:
            # Otherwise, find the path with the most points
            for i in range(len(start)):
                n = end[i] - start[i]
                N.append(n)

            if len(N) > 0:
                best = N.index(max(N))
                for i in range(start[best], end[best]):
                    best_path = np.vstack([best_path, points[i]])
            else:
                print("Failed to find best path")
                return [[90, 1000],[180,1000]]

        paths = paths[1:,:]
        best_path = best_path[1:,:]

        print("Paths:", paths)
        print("Best path:", best_path)
        print('Done finding best path.')
        return best_path

    except IndexError:
        print("Failed to find best path\n Turning right")
        return [[90, 1000],[180,1000]]
'''
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
        stop_car()
        while True:
           
           # Read lidar scan data 
           for i, data in enumerate(lidar.iter_scans()): 
                points = [[a, d] for (_, a, d) in list(data)]
                print(i, points)
                print("[SENDING] client is sending points")
                #send(points)
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

