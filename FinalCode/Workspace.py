
import csv

# Import csv and create list of Lidar points
Points = []

with open('Scans.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        Points.append([float(row[0]),float(row[1])])
    print(Points)

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
