from matplotlib import pyplot as plt
import numpy as np
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import multiprocessing as mp
import threading as mt
host='52.90.36.67'
#host='192.168.1.6'
mqttc=mqtt.Client()
mqttc.connect(host,1883,60)
mqttc.loop_start()
start=0
stop=100
spacing=30
ylim_down=start
ylim_up=stop-stop%spacing

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

#generate nodes
x=[[j,i] for j in range(start,stop,spacing) for i in range(start,stop,spacing)]

#generate Ids
marker_ref={}
for ids,i in enumerate(x,1):
    marker_ref[ids]=i
print marker_ref
scatterplot(x,color='r')
r1 = []
r2 = []
r3 = []
class warehouse:

    def __init__(self,name):
        self.name=name

        self.y1 = []
        self.x1 = []
        self.y2 = []
        self.overall = []
        if self.name == 'bot1':
            self.objsel = 1
            self.color='b'
        elif self.name == 'bot2':
            self.objsel = 2
            self.color='r'
        elif self.name == 'bot3':
            self.objsel = 3
            self.color='g'

    def logger(self,val):
        mqttc.publish("log", val, 2)
        pass

    def encoder(self,ids, direc):
        ctx = str(ids) + '||' + direc
        return ctx

    def decoder(self,ctx):
        lis = ctx.split('|')
        return lis[0], lis[-1]

    # mqtt func return on message
    def on_message(self,client, userdata, message):
        t = message.payload
        self.ax = str(t)
        client.disconnect()

    def movement(self,route_id,axis,coeff):
        self.route_id=route_id
        self.axis=axis
        self.coeff=coeff
        for kx in self.route_id:
            while 1:

                print "giving marker to rpi", kx
                mqttc.publish("rpi{}".format(self.objsel), kx, 2)

                subscribe.callback(self.on_message, "cps{}".format(self.objsel), hostname=host)
                print "found marker by rpi"
                # self.flag = input('give')
                self.flag = self.ax
                if self.flag == str(kx):
                    self.current_pos[self.axis] = self.current_pos[self.axis] + self.coeff * spacing
                    direction([self.current_pos], self.dir)
                    scatterplot([self.current_pos], self.color)
                    break

    def routecalc(self,current_pos, target_pos):
        global r1, r2, r3
        self.current_pos=current_pos[0]
        self.target_pos=target_pos[0]
        median = stop / 2


        ###################################################################################
        if self.current_pos[1] in [ylim_down , ylim_up]:
            self.coy1=1
            pass
        else:
            self.bot = self.current_pos[:]
            self.route = []
            self.route_id = []
            if self.current_pos[1]>self.target_pos[1]:

                self.dir='rev'
                self.coeff=-1
                self.x_reach = [self.current_pos[0], ylim_down]
            else:
                self.dir='fwd'
                self.coeff=1
                self.x_reach=[self.current_pos[0],ylim_up]
            self.xnodes = abs((self.x_reach[1] - self.current_pos[1]) / spacing)
            self.coy1=self.coeff
            while self.xnodes > 0:
                self.bot[1] += self.coeff*30
                self.route.append(self.bot[:])
                self.xnodes -=1

            for r in self.route:
                [self.route_id.append(key) for key, val in marker_ref.iteritems() if val == r]
            direction([self.current_pos], self.dir)
            scatterplot([self.current_pos], self.color)
            self.y1=self.route_id[:]
            self.current_pos=self.bot[:]
        ###################################################################################

        if self.current_pos[0]==self.target_pos[0]:
            self.cox1=1
            pass
        else:

            if self.target_pos[0] < self.current_pos[0]:

                self.dir = 'left'
                self.coeff = -1
            else:
                self.dir = 'right'
                self.coeff = 1
            self.y_reach = [self.target_pos[0], self.current_pos[1]]
            self.ynodes = abs((self.y_reach[0] - self.current_pos[0]) / spacing)
            self.cox1=self.coeff

            self.bot = self.current_pos[:]
            self.route = []
            self.route_id = []

            while self.ynodes > 0:
                self.bot[0] += self.coeff * 30
                self.route.append(self.bot[:])
                self.ynodes -= 1

            for r in self.route:
                [self.route_id.append(key) for key, val in marker_ref.iteritems() if val == r]
            direction([self.current_pos], self.dir)
            scatterplot([self.current_pos], self.color)
            self.x1 = self.route_id[:]
            self.current_pos = self.bot[:]
        ###################################################################################
        if self.current_pos[1]==self.target_pos[1]:
            self.coy2=1
            pass
        else:
            self.bot = self.current_pos[:]
            self.route = []
            self.route_id = []
            if self.target_pos[1]<self.current_pos[1]:

                self.dir='rev'
                self.coeff=-1
            else:
                self.dir='fwd'
                self.coeff=1

            self.x_reach=[self.current_pos[0],self.target_pos[1]]
            self.xnodes1 = abs((self.x_reach[1] - self.current_pos[1]) / spacing)
            self.coy2=self.coeff

            while self.xnodes1 > 0:
                self.bot[1] += self.coeff*spacing
                self.route.append(self.bot[:])
                self.xnodes1 -=1

            for r in self.route:
                [self.route_id.append(key) for key, val in marker_ref.iteritems() if val == r]
            direction([self.current_pos], self.dir)
            scatterplot([self.current_pos], self.color)
            self.y2 = self.route_id[:]
            self.current_pos = self.bot[:]


        ####################################################################################
        if self.objsel==1:
            r1=self.y1+self.x1+self.y2

        elif self.objsel==2:
            r2=self.y1+self.x1+self.y2

        elif self.objsel==3:
            r3=self.y1+self.x1+self.y2

        print 'routes are',r1,r2,r3

    def inter(self):
        self.movement(self.y1, 1, self.coy1)
        print '-------xref reched------'

        self.movement(self.x1, 0, self.cox1)
        print '------yref reched-------'

        self.movement(self.y2, 1, self.coy2)
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~{} destination reached~~~~~~~~~~~~~~~~~~~~~~~~~~'.format(self.name)



bot1=warehouse('bot1')
bot2=warehouse('bot2')
bot3=warehouse('bot3')

if __name__=="__main__":
    bot1.routecalc([[0,30]],[[90,60]])
    bot2.routecalc([[30,0]],[[60,30]])
    bot3.routecalc([[30, 60]], [[90, 30]])
    print "calculated route for all three"

    '''           COLLISION LOGIC          '''

    a=mt.Thread(target=bot1.inter)
    b=mt.Thread(target=bot2.inter)
    c=mt.Thread(target=bot3.inter)
    a.start()
    b.start()
    c.start()



