from matplotlib import pyplot as plt
import numpy as np
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import multiprocessing as mp
import threading as mt
import heapq
import csv, ast

# host='52.90.36.67'
host = 'iot.eclipse.org'

# host='192.168.1.6'
mqttc = mqtt.Client()
mqttc.connect(host, 1883, 60)
mqttc.loop_start()
start = 0
stop = 6
spacing = 1
bx = 0


#grid formation
# scatterplot format=[[]]
def scatterplot(x, color):
    [plt.scatter(k[0], k[1], c=color) for k in x]
    pass

#graphing purpose
# arrow format=robot point,direction
def direction(pos, dir):
    arrow(pos[0], dir)
    # update mqtt to move in certain direction
    pass


# just for gui arrow markings
def arrow(current_point, direction):
    mag1 = current_point[0] - 5
    mag2 = current_point[1] - 5

    if direction == 'fwd':
        X, Y = -current_point[0], -mag2
    elif direction == 'rev':
        X, Y = -current_point[0], -current_point[1] - 5
    elif direction == 'left':
        X, Y = -current_point[0] - 5, -current_point[1]
    elif direction == 'right':
        X, Y = -mag1, -current_point[1]
    plt.arrow(current_point[0], current_point[1], current_point[0] + X, current_point[1] + Y, edgecolor='k', width=0.5,
              head_width=5)
    pass


# plotting line between two points
def plot_line(pt1, pt2, color='r'):
    plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], color)
    pass


# fucntion to save logs via mqtt
def logger(val):
    mqttc.publish("log", val, 2)
    pass


# convert csv values to data
def csvfunc(x):
    endlist = []
    with open('crossref4.csv', 'rb') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter='|')
        for row in spamreader:
            if row['item'] == x:
                endlist.append([row['node'], row['markerid']])
    return endlist


# mqtt on message function updates a global variable
def on_message(client, userdata, message):
    global bx
    t = message.payload
    bx = str(t)
    client.disconnect()


# generate nodes for the grid
x = [[j, i] for j in range(start, stop, spacing) for i in range(start, stop, spacing)]

# generate Ids with respect to nodes
marker_ref = {}
for ids, i in enumerate(x, 1):
    marker_ref[ids] = i
print marker_ref
scatterplot(x, color='r')
print '----------------------------------------------'

r1 = []
r2 = []
r3 = []


# a class init to each node that out route requires
class Cell(object):
    def __init__(self, x, y, reachable):
        """Initialize new cell.
        @param reachable is cell reachable? not a wall?
        @param x cell x coordinate
        @param y cell y coordinate
        @param g cost to move from the starting cell to this cell.
        @param h estimation of the cost to move from this cell
                 to the ending cell.
        @param f f = g + h
        """

        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0


# calculation of route and contains movement functions as well
class warehouse:
    #init class
    def __init__(self, name):
        self.opened = []
        self.name = name
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = None
        self.grid_width = None
        
        # selection of our robot identifier
        if self.name == 'bot1':
            self.objsel = 1
            self.color = 'b'
        elif self.name == 'bot2':
            self.objsel = 2
            self.color = 'r'
        elif self.name == 'bot3':
            self.objsel = 3
            self.color = 'g'

    # init a grid for given number of nodes
    def init_grid(self, width, height, walls, start, end):

        self.grid_height = height
        self.grid_width = width
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    # movement step heuristics
    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    # get a node next to a given node
    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    # get adjacent node for a given node
    def get_adjacent_cells(self, cell):

        cells = []

        if cell.x < self.grid_width - 1:
            a = (self.get_cell(cell.x + 1, cell.y))
            cells.append(a)

        if cell.y > 0:
            a = (self.get_cell(cell.x, cell.y - 1))
            cells.append(a)

        if cell.x > 0:
            a = (self.get_cell(cell.x - 1, cell.y))
            cells.append(a)

        if cell.y < self.grid_height - 1:
            a = (self.get_cell(cell.x, cell.y + 1))
            cells.append(a)

        return cells

    # matplotlib
    def get_arrow_dir(self, x_start, y_start, x_next, y_next):
        self.x_start = x_start
        self.x_next = x_next
        self.y_start = y_start
        self.y_next = y_next
        dir = ''

        if (self.x_start - 1 == self.x_next and self.y_start == self.y_next):
            dir = "r"
        if (self.x_start + 1 == self.x_next and self.y_start == self.y_next):
            dir = "l"
        if (self.x_start == self.x_next and self.y_start == self.y_next + 1):
            dir = "u"
        if (self.x_start == self.x_next and self.y_start == self.y_next - 1):
            dir = "d"
        return dir

    # generating the path
    def get_path(self):
        cell = self.end
        path = [[[cell.x, cell.y], 's']]
        while cell is not self.start:
            dire = self.get_arrow_dir(cell.x, cell.y, cell.parent.x, cell.parent.y)

            cell = cell.parent
            path.append([[cell.x, cell.y], dire])

        # path.append([[self.start.x, self.start.y]])
        path.reverse()

        return path

    #updaing the whole cell
    def update_cell(self, adj, cell):

        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    # checking and updating the given route
    def solve(self):
        #heap push to form the route check heap docs for fucntionalities
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is self.end:
                return self.get_path()
            adj_cells = self.get_adjacent_cells(cell)

            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:

                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

    # mqtt logging function
    def logger(self, val):
        mqttc.publish("log", val, 2)
        pass

    # for encoding and decoding stuff to send to robot
    def encoder(self, ids, direc):
        ctx = str(ids) + '||' + direc
        return ctx

    def decoder(self, ctx):
        lis = ctx.split('|')
        return lis[0], lis[-1]

    # utils
    def cotoid(self, point, dic):
        for key, val in dic.items():
            if val == point:
                return (key)

    # mqtt func return on message
    def on_message(self, client, userdata, message):
        t = message.payload
        self.ax = str(t)
        client.disconnect()

    # robot to move in a certain route.
    def movement(self, route_id):
        self.route_id = route_id

        for kx in self.route_id:
            while 1:
                sen = self.encoder(kx[0], kx[1])
                print "giving marker to rpi", sen
                mqttc.publish("rpi{}".format(self.objsel), sen, 2)

                subscribe.callback(self.on_message, "cps{}".format(self.objsel), hostname=host)
                print "found marker by rpi"
                # self.flag = input('give')
                self.flag = self.ax

                if self.flag == str(kx[0]):
                    break


# declaring for three robots
bot1 = warehouse('bot1')
bot2 = warehouse('bot2')
bot3 = warehouse('bot3')
object_list = [bot1, bot2, bot3]

if __name__ == "__main__":

    logger('@cps ONLINE')

    while 1:

        logger('@cps running algorithm')
        robots = [(1, 1), (2, 1), (0, 0)]
        all_routes = []
        wall = []
        
        # waiting to get message from the gui
        subscribe.callback(on_message, "gui", hostname=host)
        print bx
        item = bx.split('|')
        del item[-1]
        t = []
        
        # crossreferencing and converting to co-ordinates
        for inde, ite in enumerate(item):
            crossrefval = csvfunc(ite)
            crossrefval = list(crossrefval[0])
            t.append([robots[inde], ast.literal_eval(crossrefval[0])])
        logger('@cps calculated the route and Ids')
        # t= (start,end)
        # t = (((1, 5), (5, 5)), ((3, 4), (4, 3)), ((0, 0), (2, 4)))

        thread = []
        object_list = object_list[:len(item)]
        
        # route calc call
        for ind, obj in enumerate(object_list):
            obj.init_grid(6, 6, wall, t[ind][0], t[ind][1])
            routes = obj.solve()
            all_routes.append(routes)
            wall.append(routes)
            idm = [[[obj.cotoid(list(i[0]), marker_ref), i[1]] for i in routes]]
            thread.append(mt.Thread(target=obj.movement, args=idm))
        logger('@cps assigned threads')

        # movement operation
        for th in thread:
            logger('@cps robots starting now')
            th.start()

        print '----------------------------------------------'
