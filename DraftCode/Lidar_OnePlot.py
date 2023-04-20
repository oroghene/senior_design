from rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
#PORT_NAME = '/dev/tty.usbserial-0001'
#lidar = RPLidar('/dev/ttyUSB0')
lidar = RPLidar('/dev/tty.usbserial-0001')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

def process_data(data):
    global max_distance
    for angle in range(360):
        distance = angle[data]
        if distance > 0:
            max_distance = max(max_distance, min(5000, distance))
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
            
scan_data = [0]*360

for i, scan in enumerate(lidar.iter_scans(max_buf_meas = 2000, min_len = 200)):
    Scans = np.array([0,0])
    print('Got %d measurments' % (len(scan)))
    print(scan)
    for (a, angle, distance) in scan:
        #print('a', a)
        #print('b', b)
        Scans = np.vstack([Scans, [angle*(np.pi/180), distance]])
    #plt.polarplot(Scans[:,0],Scans[:,1])
   
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.scatter(Scans[:,0],Scans[:,1])
    ax.grid(True)
    plt.show()
    print(Scans)
    if i > 10:
        break


lidar.stop()
lidar.stop_motor()
lidar.disconnect()