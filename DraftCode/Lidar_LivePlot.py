import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rplidar

# Initialize the RPlidar A1 scanner
PORT_NAME = '/dev/tty.usbserial-0001'   # Change this to the port name of your RPlidar A1
lidar = rplidar.RPLidar(PORT_NAME)

# Set up the figure and axis for the polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_rmax(4000)
ax.grid(True)

# Define the update function for the animation
def update(scan):
    # Convert the scan data to polar coordinates
    angles = np.array([np.radians(meas[1]) for meas in scan])
    distances = np.array([meas[2] for meas in scan])
    
    # Plot the polar data
    ax.clear()
    ax.set_rmax(4000)
    ax.plot(angles, distances, linewidth=0.5)
    
    return ax

# Set up the animation
ani = animation.FuncAnimation(fig, update, frames=lidar.iter_scans(),
                              repeat=False, interval=50)

# Show the plot
plt.show()

# Stop the RPlidar A1 scanner
lidar.stop()
lidar.disconnect()
