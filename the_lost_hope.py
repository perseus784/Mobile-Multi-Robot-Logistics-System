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
    def __init__(self,grid,marker_ref,occupied):
        self.marker_ref=marker_ref
        self.grid=grid
        self.occupied = occupied

        pass
    def addis(self,point,coeff=30):
        temp = []
        temp.append([point[0]+coeff,point[1]])
        temp.append([point[0] - coeff,point[1]])
        temp.append([point[0],point[1] + coeff])
        temp.append([point[0],point[1] - coeff])

        for ik in temp:
            if not ik in self.grid:
                temp.remove(ik)
            #elif i in  self.occupied:temp.remove(i)
        return temp



    def cotoid(self,point):
        for key, val in self.marker_ref.items():
            if val == point:
                return (key)

    def distcost(self,pt1,des):
        return (abs(des[0]-pt1[0])+abs(des[1]-pt1[1]))

    def routecalc(self,start,desto):
        self.route=[]
        self.current=start
        self.dest=desto
        self.cost_dict={}
        for ti,to in self.marker_ref.items():
            self.cost_dict[ti]=10000

        pathlis=self.addis(self.current,30)
        self.cost_dict[self.cotoid(self.current)]=0

        for ij in pathlis:
            self.cost_dict[self.cotoid(ij)]=self.distcost(ij,self.dest)

        print self.cost_dict

        for ia,ie in self.cost_dict.iteritems():
            print ie
            if ie != 10000:

                pathlis = self.addis(self.marker_ref[ia])
                print pathlis
                for ij in pathlis:
                    dist=self.distcost(ij, self.dest)

                    if self.cost_dict[self.cotoid(ij)]==10000:
                            self.cost_dict[self.cotoid(ij)] = dist
                    else: self.cost_dict[self.cotoid(ij)] += dist

        print self.cost_dict

















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

c=cal(x,marker_ref,occupied=0)
c.routecalc(start=[60,0],desto=[90,60])

plt.show()