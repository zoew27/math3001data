# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 14:22:42 2024

@author: pinkn
"""


#Chosen threshold height:
ht=2.0

#Rating curve coefficients, listed from
#lowest range of heights to heighest range.
a=[0,1.128,1.185]
b=[11.1966,1.64501,1.709]
c=[0.098436,62.3969,73.82]

#upper and lower limits of ranges of 
#river heights given for rating curve

lower_limits=[1.0910,1.1943,1.8276]
upper_limits=[1.1943,1.8276,4.1200]

import matplotlib.pyplot as plt
import pandas as pd
import bisect
import numpy as np
fig, ax = plt.subplots()



Stage_Data= pd.read_csv('Stage data Victoria Bridge.csv')
time= Stage_Data['Time']
height=Stage_Data['Height']





plt.rcParams["figure.figsize"] = [11,8]
plt.rcParams['axes.edgecolor']='white'
ax.spines['left'].set_position(('center'))
ax.spines['bottom'].set_position(('center'))
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')

time_increment=(time[1]-time[0])*24*3600

number_of_days=int((len(time)*(time[1]-time[0])))

def scale(x):
    return ((x-min(x))/(max(x)-min(x)))
scaledtime=scale(time)
scaledheight=scale(height)

w=[]
for i in range(len(a)):
    w.append(i)

def Q(x):
    z=0
    while z<w[-1]:
        if x>lower_limits[z] and x<=upper_limits[z]:
            y = (c[z]*((x-a[z])**b[z]))
            break
        elif x>upper_limits[z]:
            z = z+1
    else:
        y = (c[w[-1]]*((x-a[w[-1]])**b[w[-1]]))
    return(y)

qt = Q(ht)     
    
Flow = []
for i in height:
    Flow.append(Q(i))

scaledFlow = []
for i in Flow:
    scaledFlow.append((i-min(Flow))/(max(Flow)-min(Flow)))

negheight=-scaledheight
negday=-(scaledtime)

ax.plot(negheight,scaledFlow,'black',linewidth=1)
ax.plot([0,-1],[0,1],'red',linestyle='--',marker='',linewidth=1)
ax.plot(scaledtime, scaledFlow,'black',linewidth=1)
ax.plot(negheight, negday,'black',linewidth=1)

#y_error=0.1


scaledht = (ht-min(height))/(max(height)-min(height))
scaledqt = (qt-min(Flow))/(max(Flow)-min(Flow))

QT=[]
for i in scaledFlow:
    i = scaledqt
    QT.append(i)

SF=np.array(scaledFlow)
e=np.array(QT)
    
ax.fill_between(scaledtime,SF,e,where=SF>=e,facecolor='red')

#lower_bound = SF - y_error
#upper_bound = SF + y_error
#lower_bound = np.maximum(lower_bound,0)



#ax.fill_between(scaledtime, lower_bound, upper_bound, color='gray', alpha=0.1,zorder=1)
#ax.plot(scaledtime, lower_bound, linestyle=':', color='black')
#ax.plot(scaledtime, upper_bound, linestyle=':', color='black')
idx = np.argwhere(np.diff(np.sign(SF - e))).flatten()

f=scaledtime[idx[0]]
g=scaledtime[idx[-1]]

def unscaletime(x):
    return (((max(time)-min(time))*x)+min(time))

C=unscaletime(f)
d=unscaletime(g)

Tf=(d-C)*24

time_increment=(time[1]-time[0])*24*3600

flow = []
for i in Flow:
    if i>=qt:
        flow.append((i-qt)*(time_increment))

FEV=sum(flow)

Tfs=Tf*(60**2)

qm=(FEV/Tfs)+qt
scaledqm = (qm-min(Flow))/(max(Flow)-min(Flow))

hm=((qm/c[-1])**(1/b[-1]))+a[-1]
scaledhm = (hm-min(height))/(max(height)-min(height))

ax.plot([-scaledht,-scaledht],[-1,scaledqt],'black',linestyle='--',linewidth=1)
ax.plot([-scaledhm,-scaledhm],[-1,scaledqm],'black',linestyle='--',linewidth=1)
ax.plot([-scaledht,1],[scaledqt,scaledqt],'black',linestyle='--',linewidth=1)
ax.plot([-scaledhm,1],[scaledqm,scaledqm],'black',linestyle='--',linewidth=1)

ax.plot([f,f,f],[scaledqt,scaledqm,-1/5], 'black', linestyle='--', linewidth=1)
ax.plot([g,g,g],[scaledqt,scaledqm,-1/5], 'black', linestyle='--', linewidth=1)
ax.plot([f,f],[scaledqm,scaledqt], 'black',linewidth=1.5)
ax.plot([f,g],[scaledqm,scaledqm], 'black',linewidth=1.5)
ax.plot([f,g],[scaledqt,scaledqt], 'black',linewidth=1.5)
ax.plot([g,g],[scaledqm,scaledqt], 'black',linewidth=1.5)
plt.annotate(s='', xy=(f-1/100,-1/5), xytext=(g+1/100,-1/5), arrowprops=dict(arrowstyle='<->'))

h=[]
for i in np.arange(1,number_of_days+1):
    h.append(i/number_of_days)


l=np.arange(0,max(Flow)+50,50)
m=bisect.bisect(l,min(Flow))

n=[]
for i in np.arange(l[m],max(Flow)+50,50):
    n.append(int(i))


o=np.arange(0,max(height)+1,1)
p=bisect.bisect(o,min(height))

q=[]
for i in np.arange(o[p],max(height)+1,1):
    q.append(i)

k=[]
for i in q:
    k.append(-(i-min(height))/(max(height)-min(height))) 

j=[]
for i in n:
    j.append((i-min(Flow))/(max(Flow)-min(Flow)))

ticks_x=k+h

r=[]
for i in h:
    r.append(-i)

ticks_y=r+j


s=[]
for i in np.arange(1,number_of_days+1):
    s.append(i)

Ticks_x=q+s
Ticks_y=s+n
    
ax.set_xticks(ticks_x)
ax.set_yticks(ticks_y)
ax.set_xticklabels(Ticks_x)
ax.set_yticklabels(Ticks_y)

ax.tick_params(axis='x',colors='black',direction='out',length=9,width=1)
ax.tick_params(axis='y',colors='black',direction='out',length=10,width=1)

plt.text(-scaledht+1/100, -1,'$h_T$', size=13)
plt.text(-scaledhm+1/100, -1,'$h_m$', size=13)
plt.text(1, scaledqm,'$Q_m$', size=13)
plt.text(1, scaledqt,'$Q_T$', size=13)
plt.text(((f+g)/2)-1/50,-0.18,'$T_f$',size=13)

plt.text(0.01, 1.05,'$Q$ [m$^3$/s]', size=13)
plt.text(0.95, -0.17,'$t$ [day]', size=13)
plt.text(0.01, -1.09,'$t$ [day]', size=13)
plt.text(-1.1, 0.02,'$\overline {h}$ [m]', size=13)

ax.scatter(0,0,color='white')

A=round(FEV/(10**6),2)
B=round(Tf,2)
C=round(ht,2)
D=round(hm,2)
E=round(qt,2)
F=round(qm,2)

plt.text(0.4,-0.4,'$FEV$ ≈ '+ str(A) +'Mm$^3$', size=15)
plt.text(0.4,-0.475,'$T_f$ = '+ str(B) +'hrs', size=15)
plt.text(0.4,-0.55,'$h_T$ = '+ str(C) +'m', size=15)
plt.text(0.4,-0.625,'$h_m$ = '+ str(D) +'m', size=15)
plt.text(0.4,-0.7,'$Q_T$ = '+ str(E) +'m$^3$/s', size=15)
plt.text(0.4,-0.775,'$Q_m$ = '+ str(F) +'m$^3$/s', size=15)

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=plt.figaspect(1)*0.7)
ax = Axes3D(fig)
plt.rcParams['axes.edgecolor']='white'
plt.rcParams["figure.figsize"] = [10,8]

ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.xaxis.pane.set_edgecolor('w')
ax.yaxis.pane.set_edgecolor('w')
ax.zaxis.pane.set_edgecolor('w')

sl = (FEV/2)**0.5

a = [sl, sl]
b = [sl, sl]
c = [2, 0]

d = [sl, 0]
e = [sl, sl]
f = [0, 0]

g = [sl, sl]
h = [sl, 0]
i = [0, 0]

ax.plot(a, b, c, '--', color = 'k')
ax.plot(d, e, f, '--', color = 'k')
ax.plot(g, h, i, '--', color = 'k')

x = [sl, sl, sl, 0, 0, 0, sl, sl, 0, 0, 0, 0]
y = [sl, 0, 0, 0, 0, sl, sl, 0, 0, 0, sl, sl]
z = [2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0, 2]

ax.plot(x, y, z, color = 'k')

ax.text(5*(sl/9), -5*(sl/9), 0, 'Side-length [m]', size=13)
ax.text(-sl/4, sl/4, 0, 'Side-length [m]', size=13)
ax.text(-0.02*sl, 1.01*sl, 0.8, 'Depth [m]',size=13)

ax.text(7*(sl/10), 5*(sl/4), 1, ''+str(int(round(sl)))+'m', size=13)
ax.text(14*(sl/10), 6*(sl/10), 1, ''+str(int(round(sl)))+'m', size=13)

ax.set_zticks([0, 2])

ax.set_xlim(sl,0)
ax.set_ylim(0,sl)
ax.set_zlim(0,10)


