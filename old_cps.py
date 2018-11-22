from matplotlib import pyplot as plt
import numpy as np
import csv,time
import paho.mqtt.subscribe as subscribe
import ast
from PyQt4 import QtCore, QtGui
import paho.mqtt.client as mqtt

################################################# inits
host='52.90.36.67'
mqttc=mqtt.Client()
mqttc.connect(host,1883,60)
mqttc.loop_start()
start=20
stop=100
origin=[[5,5]]
robot=[[5,5]] #always facing north of the plot GIVE LINE POS
target=[[70,50]]
facing=None
spacing=30
global ax
#################################################


#################################################  ploting
#scatterplot format=[[]]
def scatterplot(x,color):
    [plt.scatter(k[0], k[1], c=color) for k in x]
    pass

#arrow format=robot point,direction
def direction(pos,dir):
    arrow(pos[0], dir)
    #update mqtt to move in certain direction
    pass

#just for gui arrow markings
def arrow(current_point,direction):
    mag1=current_point[0]-5
    mag2=current_point[1]-5

    if direction=='fwd':
        X,Y=-current_point[0],-mag2
    elif direction=='rev':
        X,Y=-current_point[0],-current_point[1]-5
    elif direction=='left':
        X,Y=-current_point[0]-5,-current_point[1]
    elif direction=='right':
        X,Y=-mag1,-current_point[1]
    plt.arrow(current_point[0], current_point[1],current_point[0]+X, current_point[1]+Y,edgecolor='k',width=0.2,head_width=3)
    pass

def plot_line(pt1,pt2,color='r'):
    plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]],color)
    pass
###################################################

###################################################  utils

#csv conversion
def csvfunc(x):
    endlist = []
    with open('cross1.csv', 'rb') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter='|')
        for row in spamreader:
            if row['item'] == x:
                endlist.append([row['node'], row['markerid']])
    return endlist

def logger(val):
    mqttc.publish("log",val, 2)
    pass

def encoder(ids,direc):
    ctx=str(ids)+'||'+direc
    return ctx

def decoder(ctx):
    lis=ctx.split('|')
    return lis[0],lis[-1]

#mqtt func return on message
def on_message(client, userdata, message):
    global ax
    t=message.payload
    ax=str(t)
    client.disconnect()

####################################################

def overall_func(origin,robot,target):
    logger('@cps running algorithm')
    current_id = 0
    # snippet for robot in origin itself
    global ax

    # generate nodes
    x = [[j, i] for j in range(start, stop, spacing) for i in range(start, stop, spacing)]
    print x

    # generate Ids
    marker_ref = {}
    for ids, i in enumerate(x, 1):
        marker_ref[ids] = i

    scatterplot(x, color='r')
    scatterplot(robot, color='b')
    scatterplot(target, color='g')
    scatterplot(origin, color='b')
    #plt.show()

    # reaching row reference
    # calculaing the number of nodes that should be crossed
    x_nodes = (target[0][0] - start) / spacing
    y_nodes = (target[0][1] - start) / spacing
    print x_nodes, y_nodes
    x_n = x_nodes
    y_n = y_nodes

    # get route nodes
    route = []
    bot_node = x[0][:]
    route.append(bot_node[:])
    while x_n > 0:
        bot_node[0] = bot_node[0] + spacing
        route.append(bot_node[:])
        x_n = x_n - 1
    while y_n > 0:
        bot_node[1] = bot_node[1] + spacing
        route.append(bot_node[:])
        y_n = y_n - 1
    print "this is the route", route

    # trackback ids
    id_route = []
    for r in route:
        [id_route.append(key) for key, val in marker_ref.iteritems() if val == r]
    print id_route

    x_id = id_route[:x_nodes+1]
    y_id = id_route[-y_nodes:]

    print x_id, y_id
    logger('@cps calculated the route and Ids')
    if origin==robot:

        for kx in x_id:
            while 1:
                ax = 0
                # marker check

                sen = encoder(kx, 'f')
                print "giving marker to rpi", sen
                mqttc.publish("rpi", sen, 2)
                logger('@cps giving values to rpi')
                subscribe.callback(on_message, "cps", hostname=host)
                print "found marker by rpi"
                logger('@cps found marker by rpi')

                current_id = kx
                flag = ax
                # flag=raw_input()
                if flag == str(kx):
                    logger('@cps {} nodes to reach'.format(x_nodes))
                    print "{} more nodes to cross".format(x_nodes)
                    robot[0][0] = robot[0][0] + spacing
                    direction(robot, 'right')
                    scatterplot(robot, 'b')
                    x_nodes = x_nodes - 1
                    break
        logger('@cps horizontal movement complete')
        print "x-ref reached.........."

        time.sleep(3)
        # reorienting itself

        sen = encoder(current_id, 'l')
        mqttc.publish("rpi", sen, 2)
        print "giving marker to rpi", sen

        subscribe.callback(on_message, "cps", hostname=host)
        print "found marker by rpi"

        # robot[0][1] = robot[0][1] + 15
        direction(robot, 'fwd')
        scatterplot(robot, 'b')
        # direction(robot, 'fwd')


        for ky in y_id:
            while 1:
                ax=0
                # marker check

                sen = encoder(ky, 'f')
                print "giving marker to rpi", sen
                mqttc.publish("rpi", sen, 2)
                logger('@cps giving values to rpi')

                subscribe.callback(on_message, "cps", hostname=host)
                print "found marker by rpi"
                logger('@cps found marker by rpi')


                flag = ax
                current_id = ky
                # flag=raw_input()

                if flag == str(ky):
                    logger('@cps {} nodes to reach'.format(x_nodes))
                    print "{} more nodes to cross".format(y_nodes)
                    robot[0][1] = robot[0][1] + spacing
                    direction(robot, 'fwd')
                    scatterplot(robot, 'b')
                    y_nodes = y_nodes - 1
                    break
        logger('@cps vertical movement complete')
        print "y-ref reached..........."
        logger('@cps Destination reached')
        print "........................reached destination.........................."

    else:
        if robot[0][1] < target[0][1]:
            x_ref = "up"
        else:
            x_ref = 'down'
        print x_ref
        rout = []
        id_rout = []

        pass


if __name__== "__main__":
    logger('@cps CPS ONLINE')
    while 1:

        subscribe.callback(on_message, "gui", hostname=host)
        logger('@cps got item from gui')
        #ax='snacks'
        print ax
        crossrefval=csvfunc(ax)
        crossrefval=list(crossrefval[0])
        target=[ast.literal_eval(crossrefval[0])]
        print target
        overall_func(origin,robot,target)
        mqttc.loop_stop()
        mqttc.disconnect()
        plt.show()