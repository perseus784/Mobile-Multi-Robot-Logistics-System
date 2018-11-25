from matplotlib import pyplot as plt
import numpy as np
import csv
import paho.mqtt.subscribe as subscribe
import ast
from PyQt4 import QtCore, QtGui
import paho.mqtt.client as mqtt
mqttc=mqtt.Client()
mqttc.connect("localhost",1883,60)
mqttc.loop_start()
start=20
stop=200
origin=[[5,5]]
robot=[[5,5]] #always facing north of the plot GIVE LINE POS
target=[[170,50]]
facing=None
spacing=30
global ax


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
    plt.arrow(current_point[0], current_point[1],current_point[0]+X, current_point[1]+Y,edgecolor='k',width=0.5,head_width=5)
    pass

def plot_line(pt1,pt2,color='r'):
    plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]],color)
    pass

#mqtt func return on message
def on_message(client, userdata, message):
    global ax
    t=message.payload
    ax=str(t)
    client.disconnect()

def route_calc(xnodes,bot):
    xreach = [[robot[0][0] + 15, y_up[0][1]]]
    xnodes = ((xreach[0][1] - robot[0][1]) / spacing)

    print xreach, xnodes
    xn = xnodes
    bot = robot[0][:]
    bot[0] = bot[0] + 15
    rout.append([robot[0][0] + 15, robot[0][1]])
    while xn > 0:
        bot[1] = bot[1] + spacing
        rout.append(bot[:])
        xn = xn - 1
    print rout
    for r in rout:
        [id_rout.append(key) for key, val in marker_ref.iteritems() if val == r]
    print id_rout
    return rout,id_rout

#csv conversion
def csvfunc(x):
    endlist = []
    with open('crossref.csv', 'rb') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter='|')
        for row in spamreader:
            if row['item'] == x:
                endlist.append([row['node'], row['markerid']])
    return endlist

def overall_func(origin,robot,target):
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
    # print marker_ref
    # trackback ids
    id_route = []
    for r in route:
        [id_route.append(key) for key, val in marker_ref.iteritems() if val == r]
    print id_route

    x_id = id_route[:x_nodes]
    y_id = id_route[-y_nodes:]

    print x_id, y_id

    # line traced path

    br = [[stop, origin[0][1]]]
    tl = [[origin[0][0], stop]]
    tr = [[stop, stop]]
    scatterplot(br, 'b')
    scatterplot(tl, 'b')
    scatterplot(tr, 'b')
    plot_line(origin[0], br[0])
    # plot_line(origin,tl)
    plot_line(tl[0], tr[0])
    # plot_line(tr,br)
    y_up = []
    y_down = []

    for i in range(origin[0][0], stop, spacing):
        y_down.append([i, origin[0][1]])
    for i in range(tl[0][0], stop, spacing):
        y_up.append([i, tl[0][1]])

    for i, j in zip(y_up, y_down):
        plot_line(i, j)

    if origin == robot:
        print "im here"
        if target[0][0] > start:
            direction(robot, 'right')
        for kx in x_id:
            while 1:
                ax=0
                # marker check
                '''
                flagfile=open('flag.txt','r')
                flag=flagfile.read()
                flagfile.close()'''
                print "giving marker to rpi",kx
                mqttc.publish("rpi",kx,2)
                
                subscribe.callback(on_message, "cps", hostname="localhost")
                print "found marker by rpi"

                flag = ax
                if flag == str(kx):
                    print "{} more nodes to cross".format(x_nodes)
                    robot[0][0] = robot[0][0] + spacing
                    direction(robot, 'right')
                    scatterplot(robot, 'b')
                    x_nodes = x_nodes - 1
                    break

        print "x-ref reached.........."
        # reorienting itself
        direction(robot, 'fwd')

        robot[0][1] = robot[0][1] + 15
        scatterplot(robot, 'b')
        direction(robot, 'fwd')

        for ky in y_id:
            while 1:
                # marker check
                '''
                flagfile=open('flag.txt','r')
                flag=flagfile.read()
                flagfile.close()'''

                print ky
                mqttc.publish("rpi",ky,2)
                subscribe.callback(on_message, "cps", hostname="localhost")
                flag = ax
                if flag == str(ky):
                    print "{} more nodes to cross".format(y_nodes)
                    robot[0][1] = robot[0][1] + spacing
                    direction(robot, 'fwd')
                    scatterplot(robot, 'b')
                    y_nodes = y_nodes - 1
                    break
        print "y-ref reached..........."

        print "........................reached destination.........................."

    # random to random
    else:

        if robot[0][1] < target[0][1]:
            x_ref = "up"
        else:
            x_ref = 'down'
        print x_ref
        rout = []
        id_rout = []

        if x_ref == "up":
            direction(robot, 'fwd')
            xreach = [[robot[0][0] + 15, y_up[0][1]]]
            xnodes = ((xreach[0][1] - robot[0][1]) / spacing)

            print xreach, xnodes
            xn = xnodes
            bot = robot[0][:]
            bot[0] = bot[0] + 15
            rout.append([robot[0][0] + 15, robot[0][1]])
            while xn > 0:
                bot[1] = bot[1] + spacing
                rout.append(bot[:])
                xn = xn - 1
            print rout
            for r in rout:
                [id_rout.append(key) for key, val in marker_ref.iteritems() if val == r]
            print id_rout

            for kx in id_rout:
                while 1:
                    print kx
                    flag = input('give')
                    if flag == kx:
                        robot[0][1] = robot[0][1] + spacing
                        direction(robot, 'fwd')
                        scatterplot(robot, 'b')
                        print "here", robot
                        break

            if target[0][0] > bot[0]:
                direction(robot, 'right')
                ################################

                xreach = [[target[0][0], robot[0][1]]]
                xnodes = (xreach[0][0] - robot[0][0]) / spacing
                xn = xnodes
                bot = robot[0][:]
                bot[1] = bot[1] - 30
                bot[0] = bot[0] + 15
                rout = [robot[0]]

                while xn > 0:
                    bot[0] = bot[0] + 30
                    rout.append(bot[:])
                    xn = xn - 1
                print rout
                id_rout = []
                for r in rout:
                    [id_rout.append(key) for key, val in marker_ref.iteritems() if val == r]
                print id_rout
                for kx in id_rout:

                    while 1:
                        print kx
                        flag = input('give')
                        if flag == kx:
                            robot[0][0] = robot[0][0] + spacing
                            direction(robot, 'right')
                            scatterplot(robot, 'b')
                            break
            else:
                direction(robot, 'left')
                ################################

                xreach = [[target[0][0], robot[0][1]]]
                print xreach
                xnodes = ((robot[0][0] - xreach[0][0]) / spacing) + 1
                xn = xnodes
                bot = robot[0][:]
                bot[1] = bot[1] - 30
                bot[0] = bot[0] + 15
                rout = [robot[0]]
                print "xn", xn
                while xn > 0:
                    bot[0] = bot[0] - 30
                    rout.append(bot[:])
                    xn = xn - 1
                print rout
                id_rout = []
                for r in rout:
                    [id_rout.append(key) for key, val in marker_ref.iteritems() if val == r]
                print id_rout
                for kx in id_rout:

                    while 1:
                        print kx
                        flag = input('give')
                        if flag == kx:
                            robot[0][0] = robot[0][0] - spacing
                            direction(robot, 'left')
                            scatterplot(robot, 'b')
                            break

            ###########################

            direction(robot, 'rev')

            xreach = [[robot[0][0], target[0][1]]]
            xnodes = (robot[0][1] - xreach[0][1]) / spacing
            print robot
            print xreach, xnodes
            xn = xnodes
            bot = robot[0][:]
            rout = []
            id_rout = []
            bot[0] = bot[0] + 15
            while xn > 0:
                bot[1] = bot[1] - spacing
                rout.append(bot[:])
                xn = xn - 1
            print rout

            for r in rout:
                [id_rout.append(key) for key, val in marker_ref.iteritems() if val == r]
            print id_rout

            for kx in id_rout:

                while 1:
                    print kx
                    flag = input('give')
                    if flag == kx:
                        robot[0][1] = robot[0][1] - spacing
                        direction(robot, 'rev')
                        scatterplot(robot, 'b')
                        break

        elif x_ref == "down":

            xreach = [[robot[0][0] + 15, y_down[0][1] - 10]]

            xnodes = ((robot[0][1] - xreach[0][1]) / spacing) - 1

            print xreach, xnodes
            xn = xnodes
            bot = robot[0][:]
            bot[0] = bot[0] + 15
            rout.append([robot[0][0] + 15, robot[0][1]])
            while xn > 0:
                bot[1] = bot[1] - spacing
                rout.append(bot[:])
                xn = xn - 1
            print rout
            for r in rout:
                [id_rout.append(key) for key, val in marker_ref.iteritems() if val == r]
            print id_rout
            direction(robot, 'rev')
            for kx in id_rout:
                while 1:
                    print kx
                    flag = input('give')
                    if flag == kx:
                        robot[0][1] = robot[0][1] - spacing
                        direction(robot, 'rev')
                        scatterplot(robot, 'b')
                        print "here", robot
                        break

            robot[0][1] = robot[0][1] - 15

            if target[0][0] > bot[0]:
                scatterplot(robot, 'b')
                direction(robot, 'right')
                ################################

                xreach = [[target[0][0], robot[0][1]]]
                xnodes = (xreach[0][0] - robot[0][0]) / spacing
                xn = xnodes
                print xn
                bot = robot[0][:]
                bot[1] = bot[1] + 15
                bot[0] = bot[0] + 15
                rout = [robot[0]]

                while xn > 0:
                    bot[0] = bot[0] + 30
                    rout.append(bot[:])
                    xn = xn - 1
                print rout
                id_rout = []
                for r in rout:
                    [id_rout.append(key) for key, val in marker_ref.iteritems() if val == r]
                print id_rout
                for kx in id_rout:

                    while 1:
                        print kx
                        flag = input('give')
                        if flag == kx:
                            robot[0][0] = robot[0][0] + spacing
                            direction(robot, 'right')
                            scatterplot(robot, 'b')
                            break
            else:
                scatterplot(robot, 'b')
                direction(robot, 'left')
                ################################

                xreach = [[target[0][0], robot[0][1]]]
                print xreach
                xnodes = ((robot[0][0] - xreach[0][0]) / spacing) + 1
                xn = xnodes
                bot = robot[0][:]
                bot[1] = bot[1] + 15
                bot[0] = bot[0] + 15
                rout = [robot[0]]
                print "xn", xn
                while xn > 0:
                    bot[0] = bot[0] - 30
                    rout.append(bot[:])
                    xn = xn - 1
                print rout
                id_rout = []
                for r in rout:
                    [id_rout.append(key) for key, val in marker_ref.iteritems() if val == r]
                print id_rout
                for kx in id_rout:

                    while 1:
                        print kx
                        flag = input('give')
                        if flag == kx:
                            robot[0][0] = robot[0][0] - spacing
                            direction(robot, 'left')
                            scatterplot(robot, 'b')
                            break
                            ###########################

            robot[0][1] = robot[0][1] + 15
            direction(robot, 'fwd')

            xreach = [[robot[0][0], target[0][1]]]
            xnodes = (xreach[0][1] - robot[0][1]) / spacing
            print robot
            print xreach, xnodes
            xn = xnodes
            bot = robot[0][:]
            rout = []
            id_rout = []
            bot[0] = bot[0] + 15
            while xn > 0:
                bot[1] = bot[1] + spacing
                rout.append(bot[:])
                xn = xn - 1
            print rout

            for r in rout:
                [id_rout.append(key) for key, val in marker_ref.iteritems() if val == r]
            print id_rout

            for kx in id_rout:

                while 1:
                    print kx
                    flag = input('give')
                    if flag == kx:
                        robot[0][1] = robot[0][1] + spacing
                        direction(robot, 'fwd')
                        scatterplot(robot, 'b')
                        break

if __name__== "__main__":
    while 1:
        subscribe.callback(on_message, "gui", hostname="localhost")
        print ax
        crossrefval=csvfunc(ax)
        crossrefval=list(crossrefval[0])
        target=[ast.literal_eval(crossrefval[0])]
        print target
        overall_func(origin,robot,target)
        mqttc.loop_stop()
        mqttc.disconnect()
        plt.show()
        
    