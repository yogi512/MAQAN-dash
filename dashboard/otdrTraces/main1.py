import pandas as pd 
import json 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import sys

##filename = str(sys.argv[1])##
##f = open(filename)##

f = open('RP_1_0001-dump.json')
data = json.load(f)

l=[]
for i in range(1,100):
    try:
        l.append((data['KeyEvents']['event {}'.format(i)]['distance'],data['KeyEvents']['event {}'.format(i)]['refl loss'],data['KeyEvents']['event {}'.format(i)]['splice loss']))
    except:
        break
df0 = pd.DataFrame(l, columns =['distance','reflectionLoss','spliceLoss'])
print(df0)

out=[]
out.append((data['FxdParams']['date/time'],data['FxdParams']['wavelength'],data['FxdParams']['pulse width'],data['FxdParams']['range']))
df1 = pd.DataFrame(out,columns=['date/time','wavelength','pulseWidth','range'])
print(df1)

df1.to_csv('data2.csv',index=False)
df0.to_csv('data1.csv',index=False)

fig,ax=plt.subplots(2,1)
fig.set_size_inches(7,5)
fig.set_tight_layout('tight')
sns.set_theme()
sns.set(rc={'axes.facecolor':'#e5e5e5','figure.facecolor':'#ffffff','grid.color': '#ffffff','grid.linestyle':'dotted'})


x=df0['distance'].to_list()
y=df0['reflectionLoss'].to_list()
z=df0['spliceLoss'].to_list()

x=[float(i) for i in x]
y=[float(i) for i in y]
z=[float(i) for i in z]

ax[0].plot(x,y,'maroon',marker='o',linewidth=2)
ax[1].plot(x,z,'Blue',marker='o',linewidth=2)

ax[0].set_xlabel('Distance (km)',fontsize=10)
ax[1].set_xlabel('Distance (km)',fontsize=10)
ax[0].set_ylabel('Reflection loss (dB)',fontsize=10)
ax[1].set_ylabel('Splice loss (dB)',fontsize=10)
ax[1].set_title('Distance vs Splice loss',fontsize=17)
ax[0].set_title('Distance vs Reflection loss',fontsize=17)

ax[0].grid(True)
ax[1].grid(True)
plt.tight_layout()

plt.savefig("mygraph.png")


