import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import time
from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite
import linecache



# Time Operator
ts = load.timescale()

# Specify Loading Mode
load_mode = 'string_txt'

# Load by String
def Satellite_Loader(load_mode):
    # Load by String
    if load_mode =='string_txt':
        satellite=[]
        with open("FuLL_Catalog.txt") as f:
            lines=f.readlines()
            (c,d)=(0,10000)  #決定選取範圍
            for m in range(c,d,3):
                for line in lines[m:m+3]:
                    if 'DEB' in line:
                        line0=linecache.getline('FuLL_Catalog.txt', m+1)
                        line1=linecache.getline('FuLL_Catalog.txt', m+2)
                        line2=linecache.getline('FuLL_Catalog.txt', m+3)
                        satellites = EarthSatellite(line1, line2, line0, ts)
                        satellite.append(satellites)
            return satellite
# =============================================================================
#     elif load_mode =='string_url_to_txt':  #這段有問題尚未解決 
#         url = 'https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/%3Enow-30/orderby/NORAD_CAT_ID,EPOCH/format/3le'
#         filename = '3le.txt'
#         satellites = load.tle_file(url, filename=filename)
#         satellite=[]
#         (e,f)=(0,55) #決定選取範圍
#         for p in range(e,f,3):
#                 for line in satellites[p:p+3]:
#                     if 'DEB' in line:
#                         satellite.append(satellites[0])
#         return satellite
# =============================================================================
                      
# =============================================================================
#         line1 = '1 25544U 98067A   14020.93268519  .00009878  00000-0  18200-3 0  5082'
#         line2 = '2 25544  51.6498 109.4756 0003572  55.9686 274.8005 15.49815350868473'
#         satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)
# =============================================================================

    elif load_mode =='url':
        satellite=[]
        (a,b)=(125,131) #決定選取範圍
        for n in range(a,b):
            url = 'https://celestrak.com/satcat/tle.php?CATNR={}'.format(n)
            filename = 'tle-CATNR-{}.txt'.format(n)
            satellites = load.tle_file(url, filename=filename)
            if 'DEB' in str(satellites):
                satellite.append(satellites[0])
        return satellite
             
# Quest Position
r0=6300
def Satellite_Position(satellite, num):
    x=[]
    y=[]
    z=[]
    
    t=ts.utc(2014, 1, 18, 1, 35.625+num)
    
    if satellite==[]:
        pass
    else:
        for i in satellite:
            geocentric = i.at(t)
            #print(geocentric.position.km)
            subpoint = wgs84.subpoint(geocentric)
            
            #print('Latitude:', subpoint.latitude.degrees)
            #print('Longitude:', subpoint.longitude.degrees)
            #print('Height: {:.1f} km'.format(subpoint.elevation.km))
            
            r=(subpoint.elevation.km+r0)/r0
            phi=subpoint.longitude.degrees
            theta=90-subpoint.latitude.degrees
            x.append(r*np.cos(phi/180*np.pi)*np.sin(theta/180*np.pi))
            y.append(r*np.sin(phi/180*np.pi)*np.sin(theta/180*np.pi))
            z.append(r*np.cos(theta/180*np.pi))
    return x, y, z

def update_points(num, x, y, z, points):
    x,y,z=Satellite_Position(satellite, num)
    
    # calculate the new sets of coordinates here. The resulting arrays should have the same shape
    # as the original x,y,z
    new_x = x
    new_y = y
    new_z = z


    # update properties
    points.set_data(new_x,new_y)
    points.set_3d_properties(new_z, 'z')
    
    # return modified artists
    return points



if __name__ == '__main__':
    satellite = Satellite_Loader(load_mode)
    x,y,z=Satellite_Position(satellite, 0)
    
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    init = [[4, 6],
           [ 4, 6],
           [ 4, 6]]
    points, = ax.plot(x, y, z, '*')
    
    ax.set_xlim3d([-1.5, 1.5])
    ax.set_ylim3d([-1.5, 1.5])
    ax.set_zlim3d([-1.5, 1.5])
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    
    ani=animation.FuncAnimation(fig, update_points, frames=11, interval = 1000, fargs=(x, y, z, points))
    
    plt.show()