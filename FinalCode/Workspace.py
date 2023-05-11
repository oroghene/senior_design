import csv

import matplotlib.pyplot as plt
import numpy as np

# Import csv and create list of Lidar points
Points_rad = np.array([[0,0]])
Points_deg = np.array([[0,0]])

with open('Scans.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        Points_rad = np.vstack([Points_rad, [float(row[0])*np.pi/180,float(row[1])]])
        Points_deg = np.vstack([Points_deg, [float(row[0]),float(row[1])]])
        
    Points_rad = Points_rad[1:,:]
    Points_deg = Points_deg[1:,:]

# Create functions here
def reg_plot(points):
    fig, ax = plt.subplots()
    ax.scatter(points[:,0],points[:,1])
    plt.show()
    return

def plot_points(points):
    fig1, ax1 = plt.subplots(subplot_kw={'projection': 'polar'})
    ax1.set_rlim(0,1000)
    ax1.scatter(points[:,0],points[:,1])
    ax.grid(True)
    plt.show()
    return


def paths_points(points):
    paths = np.array([[0,0]])
    array = []
    walls = []
    temp = []
    fp = points[0][1] # first point's distance
    
    for i in range(1,len(points)):
        if points[i][1] >= fp: #check if distance is 5%+ bigger than previous one
            temp.append(points[i])
        else:
            array.append(temp)
            temp = []
    paths = paths[1:,:]
   
    print('Paths:\n', paths)
    print('array size:\n', len(array))
    print('array:\n', array)
    return paths

def find_furthest_distance(points):
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
    
    return best_path

def orient_car(points):
    angle = np.average(points,axis=0)[0] # Find midpoint of angles
    print('Face', angle, 'degrees')
    if angle <= 180:
        print('Turn', angle, 'to the right')
    elif angle > 180:
        print('Turn', 360 - angle, 'degrees to the left') 
    
    return angle



# Test function here using the points from csv
#RunTest = find_furthest_distance(Points_deg)
#print('RunTest:\n', RunTest)
#reg_plot(RunTest)
c = find_furthest_distance(Points_deg)
b = orient_car(c)
reg_plot(c)
reg_plot(Points_deg)