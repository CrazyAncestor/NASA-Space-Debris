# The debris are separated to two parts, and are plotted in blue for x>0 and in red for x<0.
# We can find an important region for debris and mark them in red.

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

def HST_Loader(load_mdoe):
    line1 = '1 20580U 90037B   21273.81193127  .00001057  00000-0  52853-4 0  9991'
    line2 = '2 20580  28.4698  87.8983 0002801 115.5815 264.4960 15.09755843527196'
    HST = EarthSatellite(line1, line2, 'HST', ts)
    return HST 
             
# Quest Position
r0=6300
def Satellite_Position_given_time(satellite, i):
    x=[]
    y=[]
    z=[]
    

    t=ts.utc(2021, 10, 5, 1, 35.625+i)

    
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

def Satellite_Position(satellite):
    x=[]
    y=[]
    z=[]
    t = ts.now()
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


def HST_Position(HST):
    t = ts.now()
    geocentric = HST.at(t)
    #print(geocentric.position.km)
    subpoint = wgs84.subpoint(geocentric)
            
    #print('Latitude:', subpoint.latitude.degrees)
    #print('Longitude:', subpoint.longitude.degrees)
    #print('Height: {:.1f} km'.format(subpoint.elevation.km))
            
    r=(subpoint.elevation.km+r0)/r0
    phi=subpoint.longitude.degrees
    theta=90-subpoint.latitude.degrees
    x1=r*np.cos(phi/180*np.pi)*np.sin(theta/180*np.pi)
    y1=r*np.sin(phi/180*np.pi)*np.sin(theta/180*np.pi)
    z1=r*np.cos(theta/180*np.pi)
    return x1,y1,z1
    
def update_plot_given_time(i):
    axlistx = []
    axlisty = []
    axlistz = []
    bxlistx = []
    bxlisty = []
    bxlistz = []
    
    x,y,z=Satellite_Position_given_time(satellite, i)
    
    #seperates Data in two parts
    for j in range(len(x)):
        if x[j]<=0:
            axlistx.append(x[j])
            axlisty.append(y[j])        
            axlistz.append(z[j])
        else:  
            bxlistx.append(x[j])
            bxlisty.append(y[j])        
            bxlistz.append(z[j])
            
    scat._offsets3d = (axlistx,axlisty,axlistz)
    scat2._offsets3d = (bxlistx,bxlisty,bxlistz)

def update_plot(i):
    axlistx = []
    axlisty = []
    axlistz = []
    bxlistx = []
    bxlisty = []
    bxlistz = []

    
    x,y,z=Satellite_Position(satellite)
    

    #seperates Data in two parts
    for j in range(len(x)):
        if x[j]<=0:
            axlistx.append(x[j])
            axlisty.append(y[j])        
            axlistz.append(z[j])
        else:  
            bxlistx.append(x[j])
            bxlisty.append(y[j])        
            bxlistz.append(z[j])
            
    scat._offsets3d = (axlistx,axlisty,axlistz)
    scat2._offsets3d = (bxlistx,bxlisty,bxlistz)


def update_plot_satellite_protect(i):
    axlistx = []
    axlisty = []
    axlistz = []
    bxlistx = []
    bxlisty = []
    bxlistz = []
    cxlistx = []
    cxlisty = []
    cxlistz = []
    
    x,y,z=Satellite_Position(satellite)
    x1,y1,z1=HST_Position(HST)
    
    #seperates Data in two parts
    for j in range(len(x)):
        if ((x[j]-x1)**2+(y[j]-y1)**2+(z[j]-z1)**2)**0.5*r0<=2000:
            axlistx.append(x[j])
            axlisty.append(y[j])        
            axlistz.append(z[j])
        else:  
            bxlistx.append(x[j])
            bxlisty.append(y[j])        
            bxlistz.append(z[j])
            
    cxlistx.append(x1)
    cxlisty.append(y1)        
    cxlistz.append(z1)
            
    scat._offsets3d = (axlistx,axlisty,axlistz)
    scat2._offsets3d = (bxlistx,bxlisty,bxlistz)
    scat3._offsets3d = (cxlistx,cxlisty,cxlistz)
    
if __name__ == '__main__':
    satellite = Satellite_Loader(load_mode)

    HST=HST_Loader(load_mode)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    
    ax.set_xlim3d([-1.5, 1.5])
    ax.set_ylim3d([-1.5, 1.5])
    ax.set_zlim3d([-1.5, 1.5])
    

    ax.set_xlabel('x')

    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    #plot data to the same axes

    scat = ax.scatter([], [], color='red', marker='.') 
    scat2 = ax.scatter([], [], color = 'blue', marker = '.')
    scat3 = ax.scatter([], [], color = 'black', marker = '*')

    
    # Specify simulating Mode
    mode = 'satellite_protect'
    
    if mode =='real_time':
        anim = animation.FuncAnimation(fig, update_plot, frames=20, interval=1000)
    if mode =='given_time':
        ani=animation.FuncAnimation(fig, update_plot_given_time, frames=20, interval=1000)
    if mode =='satellite_protect':
        ani=animation.FuncAnimation(fig, update_plot_satellite_protect, frames=20, interval=1000)

    
    plt.show()