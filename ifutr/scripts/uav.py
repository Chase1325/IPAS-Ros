#!/usr/bin/env python

from time import sleep
from multiprocessing import Process

#Import ROS items
import rospy
#Import Services
from ifutr.srv import *

#Import External Libraries
import pypozyx

#Import Scripts from package
import sensors.Pozyx as poz
#import flightController.rangefinder as ranger


def initialize():
    rospy.init_node('UAV', anonymous=False)


def run_IPAS():
    pass

def localize_serviceHandler(request):
    print('Starting the handler')

    #change the IDs and coordinates yourself according to your measurement
    anchors = rospy.get_param('/anchorpose')

    r = poz.IPozyx(anchors)
    r.setup()

    x_buff = []
    y_buff = []
    z_buff = []

    #print('About to gather position data')
    i=0
    while(i<100):
        try:
            pos = r.run()
            x_buff.append(pos.x)
            y_buff.append(pos.y)
            z_buff.append(pos.z)

            i+=1
        except:
            pass

    return localize_serviceResponse(x_buff,y_buff,z_buff)

def run_Localize():
    #Wait for client to request service
    print('Creating service')
    serv = rospy.Service('localize_serv', localize_service, localize_serviceHandler)
    print('Service Created')
    rospy.spin()

def run_FlightTest():
    #Flight test updates drone pose inside the workspace
    #by user-sent pose commands
    #print('Inside flight test')
    #range = Rangefinder()
    #print(range)
    #anchors = rospy.get_param('/anchorpose')
    #pozyx = IPozyx(anchors)
    #pozyx.setup()


    #while(rospy.get_param('/lightswitch'==True)):
        #try:
            #pos = pozyx.run(1000)
            #z = range.getRange()
            #print('got pozyx')
            #print('got range')
            #print(z)
            #print('X={}, Y={}, Z={}'.format(pos.x, pos.y, z))
            #print(str(pos.x) +" " + str(pos.y) + " " + str(z))
            #sleep(0.01)
        #except:
        #    print('fail')



def run():
    #System Mode ('IPAS', 'Localize', 'Flight_Test', 'Ground_Test')
    #Selected mode determined from rosparam values
    mode = rospy.get_param('/mode')

    if(mode=='IPAS'):
        run_IPAS()
    elif(mode=='Localize'):
        run_Localize()
    elif(mode=='Flight_Test'):
        run_FlightTest()
    elif(mode=='Ground_Test'):
        pass #Drone not required
    elif(mode=='IPAS_Sim'):
        pass #Drone not required
    else:
        print('Failed to initialize')

if __name__ == "__main__":

    initialize()
    run()
