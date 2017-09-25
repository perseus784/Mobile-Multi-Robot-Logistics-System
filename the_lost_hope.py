from matplotlib import pyplot as plt
start=0
stop=100
spacing=30
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

class cal:
    def __init__(self,grid,marker_ref):
        self.marker_ref=marker_ref
        self.grid=grid


        pass
    def addis(self,point,coeff,occ):
        temp = []
        temp.append([point[0]+coeff,point[1]])
        temp.append([point[0] - coeff,point[1]])
        temp.append([point[0],point[1] + coeff])
        temp.append([point[0],point[1] - coeff])

        for ik in temp:
            if not ik in self.grid:
                temp.remove(ik)
            if ik in occ:

                temp.remove(ik)
        return temp

    def cotoid(self,point,dic):
        for key, val in dic.items():
            if val == point:
                return (key)

    def distcost(self,pt1,des):
        return (abs(des[0]-pt1[0])+abs(des[1]-pt1[1]))

    def routecalc(self,start,desto,occupied):
        self.route=[]
        self.current=start
        self.dest=desto
        self.cost_dict={}
        self.route.append(self.cotoid(start,self.marker_ref))
        print 'occu',occupied

        while self.current != self.dest:

            pathlis = self.addis(self.current, 30,occupied)

            for ij in pathlis:
                self.cost_dict[self.cotoid(ij, self.marker_ref)] = self.distcost(ij, self.dest)

            too = min([v for k, v in self.cost_dict.items()])
            parent = self.cotoid(too, self.cost_dict)
            self.route.append(parent)
            self.current = self.marker_ref[parent]
        return self.route



#generate nodes
x=[[j,i] for j in range(start,stop,spacing) for i in range(start,stop,spacing)]
print x

#generate Ids
marker_ref={}
for ids,i in enumerate(x,1):
    marker_ref[ids]=i
print marker_ref
scatterplot(x,color='r')

print '----------------------------------------------'

c=cal(x,marker_ref)
r1= c.routecalc(start=[60,0],desto=[0,60],occupied=[])
print r1
blocks=[marker_ref[i] for i in r1][1:]
print blocks
c1=cal(x,marker_ref)
r2=c.routecalc(start=[60,0],desto=[90,60],occupied=blocks)
print r1,r2

plt.show()