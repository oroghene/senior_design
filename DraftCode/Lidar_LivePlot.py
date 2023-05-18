import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rplidar
import socket
import threading
# import pickle # serialization and deserialization

# =============== SERVER ===============
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:    
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                break
            print(f'[{addr}] {msg}')
            conn.send("Msg received".encode(FORMAT)) # send to client

    conn.close()

def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()
# =============== SERVER ===============

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
