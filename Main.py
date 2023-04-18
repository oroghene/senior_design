import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rplidar
from math import floor, pi, cos, sin

# Initialize the RPlidar A1 scanner
PORT_NAME = '/dev/tty.usbserial-0001'   # Change this to the port name of your RPlidar A1
lidar = rplidar.RPLidar(PORT_NAME, baudrate=115200, timeout=1, logger=None)
lidar.motor_speed = 1020
max_distance = 0

print('motor speed: ', lidar.motor_speed)

# Set up the figure and axis for the polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_rmax(4000)
ax.grid(True)
            
scan_data = [0]*360

# Define the update function for the animation
def update(scan):
    def process_data(data):
        global max_distance
        for angle in range(360):
            distance = data[angle]
            if distance > 0:
                max_distance = max(min(5000, distance), max_distance)
                radians = angle * pi / 180.0
                x = distance * cos(radians)
                y = distance * sin(radians)
                point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
                print('Point:', point)
            
    # Convert the scan data to polar coordinates
    angles = np.array([np.radians(meas[1]) for meas in scan])
    distances = np.array([meas[2] for meas in scan])
    
    # Plot the polar data
    ax.clear()
    ax.set_rmax(4000)
    ax.scatter(angles, distances, linewidth=0.5)
    
    # for max distance
    for (_, angle, distance) in scan:
        scan_data[min(359, floor(angle))] = distance
    process_data(scan_data)
    
    return ax

# for scan in lidar.iter_scans():
    
# Set up the animation
ani = animation.FuncAnimation(fig, update, frames=lidar.iter_scans(),
                              repeat=False, interval=50, cache_frame_data=False)

# Show the plot
plt.show()

# Stop the RPlidar A1 scanner
lidar.stop()
lidar.disconnect()