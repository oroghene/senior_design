import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rplidar
import socket
# import pickle # serialization and deserialization

# =============== CLIENT ===============
HEADER = 64
PORT = 5050
# SERVER = "192.168.1.152"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
send(DISCONNECT_MESSAGE)
# =============== CLIENT ===============

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
