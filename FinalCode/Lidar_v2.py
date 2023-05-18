import math
import time
import matplotlib.pyplot as plt
from rplidar import RPLidar
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
    time.sleep(1)

    # Start taking measurements and updating the plot
    for scan in lidar.iter_scans():
        points = []
        for (_, angle, distance) in scan:
            x = distance * math.cos(math.radians(angle))
            y = distance * math.sin(math.radians(angle))
            points.append((x, angle, y))
        update_plot(points)
        plt.pause(0.001)

except KeyboardInterrupt:
    print('Stopping...')
finally:
    # Stop scanning and clean up
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
