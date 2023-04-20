import csv
import pandas as pd
import openpyxl

angle_array = list()
distance_array = list()
quality_array = list()

with open('testing_file.csv', newline='') as csvfile:
    lidar_data = csv.reader(csvfile, delimiter=' ')
    for row in list(lidar_data)[3:]:
        angle_array.append(row[0])
        distance_array.append(row[1])
        quality_array.append(row[2])

# print("angle array:")
# print(angle_array)
# print("distance array:")
# print(distance_array)
# print("quality array:")
# print(quality_array)

df = pd.DataFrame([[angle_array[i], distance_array[i], quality_array[i]] for i in range(len(angle_array))], columns=['Angle', 'Distance', 'Quality'])

# print(df)

df.to_excel('clean_lidar_data.xlsx', index = False)
# with open("clean_lidar_data.csv", "w", newline='') as csvWriteFile:
#     clean_lidar_data = csv.writer(csvWriteFile, delimiter=' ')