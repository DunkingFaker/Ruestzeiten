import random
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

########################### general ####################################
def show_demand(instance):
    fig,axs=plt.subplots(instance.C,1,figsize=(20,2*instance.C),sharex=True,sharey=True)
    axs=iter(axs.flat)
    for c in range(instance.C):
        ax=next(axs)
        demand=[instance.d[c][t] for t in range(instance.T)]
        ax.bar(range(instance.T),demand,color='b',width=0.2,align='edge',alpha=0.8,label="Bedarf "+chems[c]+" #"+str(c))
        ax.set_ylabel("Menge")
        #ax.set_title("Bedarf "+chems[c])
        ax.legend()
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xticks(range(instance.T))
        
    ax.set_xlabel("Zeit")

chems=['Chlor', 'Kohlenstoff', 'Schwefel', 'Kryptonit', 'Wasserstoff', 'Buckyballs']

def colour_pick(quantity):
    if quantity>0:
        return 'g'
    return 'gray'

######################  JSP ##################################

class instance2:
    def __init__(self,J=0,T=0,M=0):
        self.J=J
        self.T=T
        self.M=M

    def __repr__(self):
        result= "J Anzahl Jobs: ...................{}\n".format(self.J)
        result+="T Anzahl Zeitperioden: ................{}\n".format(self.T)
        result+="M Anzahl Maschinen: .......{}\n".format(self.M)
        return result
    
    def __str__(self):
        return self.__repr__()
        
def rnd_instance2(C=10,T=20,k=5,r=3,incompatability=0.1,seed=None):
    random.seed(seed)
    np.random.seed(seed=seed)
    g=1
    B=100
    h=10
    # Poisson...
    d=np.zeros(shape=(C,T))
    for c  in range(C):
        times=[t for t in np.cumsum(scipy.stats.poisson.rvs(3,size=10)+1)-1 if t < T]
        for t in times:
            d[c,t]=random.randint(5,50)
    I=[]
    for c in range(C):
        for cc in range(c+1,C):
            if random.random()<=incompatability:
                I.append((c,cc))
    return instance2(C=C,T=T,g=g,B=B,d=d,h=h,I=I,k=k,r=r)

def show_solution2(x,z,p,instance,chemical='all'):
    fig,axs=plt.subplots(2,1,figsize=(20,6),sharex=True)
    axs=axs.flat
    axs=iter(axs)
    ax=next(axs)

    if chemical=='all':
        chemicals=range(instance.C)
        chemical_string="gesamt"
    elif chemical in chems: 
        chemical_string=chemical
        chemical=chems.index(chemical)
        chemicals=[chemical]
    else:
        chemicals=[chemical]
        chemical_string=chems[chemical]
    demand=[sum([instance.d[c][t] for c in chemicals]) for t in range(instance.T)]
    storage=[sum([p[c][t].x for c in chemicals]) for t in range(instance.T)]
    deliveries=[sum([x[c][t][v].x for c in chemicals for v in range(instance.k)]) for t in range(instance.T)]
    ax.bar(range(instance.T),demand,color='b',width=0.2,align='edge',alpha=0.8,label="Bedarf")
    ax.bar(range(instance.T),deliveries,color='g',width=-0.2,align='edge',alpha=0.6,label="Lieferungen")
    ax.step(range(instance.T),storage,'k',linewidth=4,alpha=0.8,label="Lagerstand",where='post')
    ax.set_ylabel("Menge")
    ax.set_title("Bedarf / Lagerstand / Lieferungen: "+chemical_string)
    ax.legend()
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xticks(range(-instance.r,instance.T))
    
    offset=0.1
    ax=next(axs)
    for truck in range(instance.k):
        truck_rides=[[t-instance.r+offset,t-offset] for t in range(instance.T) if z[t][truck].x==1]
        colours=['g']*len(truck_rides)
        if chemical!='all':
            colours=[colour_pick(x[chemical][t][truck].x) for t in range(instance.T) if z[t][truck].x==1]
        for ride,colour in zip(truck_rides,colours):
            ax.plot(ride,[truck+1]*len(ride),colour,linewidth=10,alpha=0.6)
    ax.set_xlabel("Zeit")
    ax.set_ylabel("Lastwagen")
    ax.set_title("Lastwagenfahrten")
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.show()

### sample instance for second notebook  
def get_instance2():
    return rnd_instance2(C=4,T=12,k=7,r=3,incompatability=0.1,seed=42)