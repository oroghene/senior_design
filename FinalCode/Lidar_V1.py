import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial.tools.list_ports
from rplidar import RPLidar
from math import pi, cos, sin

# Find the port name for the RPLidar A1 scanner
PORT_NAMES = [port.device for port in serial.tools.list_ports.comports() if 'USB' in port.name]
if not PORT_NAMES:
    raise IOError("RPLidar A1 not found on any USB ports.")
PORT_NAME = PORT_NAMES[0]
lidar = RPLidar(PORT_NAME)

# Set the motor speed and start the lidar
lidar.set_pwm(750)
lidar.start_motor()

# Set up the figure and axis for the polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_rmax(5000)
ax.grid(True)

# Define the update function for the animation
def update(scan):
    # Convert the scan data to polar coordinates
    angles = np.array([np.radians(meas[1]) for meas in scan])
    distances = np.array([meas[2] for meas in scan])
    
    # Plot the polar data
    ax.clear()
    ax.set_rmax(5000)
    ax.scatter(angles, distances, s=5, linewidth=0.5)
    
    # Process the scan data
    for (_, angle, distance) in scan:
        radians = angle * pi / 180.0
        x = distance * cos(radians)
        y = distance * sin(radians)
        point = (x, y)
        # Do something with the point, such as add it to a list or draw it on another plot
        
    return ax

# Set up the animation
ani = animation.FuncAnimation(fig, update, frames=lidar.iter_scans(),
                              repeat=False, interval=50)

# Show the plot
plt.show()

# Stop the lidar and disconnect from it
lidar.stop_motor()
lidar.stop()
lidar.disconnect()
