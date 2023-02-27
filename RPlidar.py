from rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
#PORT_NAME = '/dev/tty.usbserial-0001'
#lidar = RPLidar('/dev/ttyUSB0')
lidar = RPLidar('/dev/tty.usbserial-0001')

"""info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)"""


for i, scan in enumerate(lidar.iter_scans()):
    Scans = np.array([0,0])
    print('Got %d measurments' % (len(scan)))
    print(scan)
    for (a, angle, distance) in scan:
        #print('a', a)
        #print('b', b)
        Scans = np.vstack([Scans, [angle*(np.pi/180), distance]])
    #plt.polarplot(Scans[:,0],Scans[:,1])
   
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(Scans[:,0],Scans[:,1])
    ax.grid(True)
    plt.show()
    print(Scans)
    if i > 10:
        break

    
lidar.stop()
lidar.stop_motor()
lidar.disconnect()