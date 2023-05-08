
import csv
import numpy as np

# Import csv and create list of Lidar points
Points = []

with open('Scans.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        Points.append([float(row[0]),float(row[1])])
    #print('Points:', Points)


# Create functions here
def find_furthest_distance(points):
    paths = np.array([['Angle','Distcance']])
    walls = []
    temp = []
    for i in range(1,len(points)):
        if points[i][1] >= points[i-1][1]*1.05:
            temp.append(points[i])
        else:
            if len(temp) > 0:
                paths = vstack([paths, temp])
            temp = []
    print('Paths:', paths)
    return paths[max(len(elem) for elem in paths)]


# Test function here using the points from csv

RunTest = find_furthest_distance(Points)
print('RunTest:', RunTest)