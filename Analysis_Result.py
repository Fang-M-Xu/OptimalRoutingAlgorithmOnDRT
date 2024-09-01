# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 20:31:47 2024

@author: Fang Xu
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

reslt_data = pd.read_csv('Data/Building_Result.csv');

bar=np.arange(len(reslt_data['Line']))
bar_width=0.15

fig = plt.figure(figsize=(10, 4), dpi=120)
ax = fig.add_subplot(111)

#plt.bar(reslt_data['Line'],reslt_data['Residential'],color='brown',label="Residential",width=0.3)
ax.bar(bar-bar_width*2,reslt_data['Residential-Commercial'],color='red',label="Residential-Commercial",width=0.15)
ax.bar(bar-bar_width,reslt_data['Commercial'],color='yellow',label="Commercial",width=0.15)
ax.bar(bar,reslt_data['Public'],color='green',label="Public",width=0.15)
ax.bar(bar+bar_width,reslt_data['Industrial'],color='purple',label="Industrial",width=0.15)
ax.bar(bar+bar_width*2,reslt_data['Sheltered Residence'],color='black',label="Sheltered Residence",width=0.15)

plt.xticks(bar,labels=reslt_data['Line'],rotation=70)
plt.ylabel('Amount')
plt.xlabel('Travel tool')
plt.title('Amount of building of travel route')

plt.legend()
plt.show()



#reslt_data.loc[1]
#reslt_data['Scenario']