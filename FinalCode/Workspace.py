
import csv

with open('Points.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')

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
