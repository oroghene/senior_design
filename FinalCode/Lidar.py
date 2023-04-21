import math
import time
import matplotlib.pyplot as plt
from rplidar import RPLidar


# Find the port name for the RPLidar A1 scanner
PORT_NAMES = [port.device for port in serial.tools.list_ports.comports() if 'USB' in port.name]
if not PORT_NAMES:
    raise IOError("RPLidar A1 not found on any USB ports.")
PORT_NAME = PORT_NAMES[0]

#PORT_NAME = '/dev/tty.usbserial-0001'   # Change this to the correct port name for your Rplidar
lidar = RPLidar(PORT_NAME)

# Create a figure and axes for plotting
fig, ax = plt.subplots(subplot_kw=dict(polar=True))

# Create a function for updating the plot with new data
def update_plot(points):
    ax.clear()
    ax.set_ylim(0, 4000)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.plot([math.radians(p[1]) for p in points], [p[2] for p in points], 'o')

try:
    # Start scanning the Rplidar
    lidar.start_motor()
    lidar.start_scan()

    # Keep looping to read and plot data until the program is terminated
    while True:
        # Read a full 360-degree scan from the Rplidar
        data = lidar.iter_scans()

        # Convert the data to a list of (quality, angle, distance) tuples
        points = [(q, math.degrees(a), d) for (_, a, d) in data]

        # Update the plot with the new data
        update_plot(points)

        # Print the raw data to the console
        print(points)

        # Wait a short time before reading the next scan
        time.sleep(0.1)

except KeyboardInterrupt:
    # Stop scanning and close the Rplidar when the program is terminated
    lidar.stop_motor()
    lidar.stop_scan()
    lidar.disconnect()
