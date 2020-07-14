## Create data
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams as rcParams
#Open csv file
dailyData=pd.read_csv(r"C:\Users\DELL\Documents\GitHub\Project\PIG_FinalProject\summaryCSVs\hourlyDistances.csv")
dailyData['kilometers']=dailyData['Distance']/1000
#get unique values for hour
condition=(dailyData['Hour']< 4) | (dailyData['Hour']>18)
dailyData=dailyData.loc[condition]
dailyData=dailyData[dailyData['kilometers']>0]
hours=dailyData.loc[condition]['Hour'].unique()
hours.sort()
#Get hour interval from integer digits
get_hour={0:"00:00-01:00",1:"01:00-02:00",2:"02:00-03:00",3:"03:00-04:00",4:"04:00-05:00",5:"05:00-06:00",6:"06:00-07:00",7:"07:00-08:00",8:"08:00-09:00",9:"09:00-10:00",10:"10:00-11:00",11:"11:00-12:00",12:"12:00-13:00",13:"13:00-14:00",14:"14:00-15:00",15:"15:00-16:00",16:"16:00-17:00",17:"17:00-18:00",18:"18:00-19:00",19:"19:00-20:00",20:"20:00-21:00",21:"21:00-22:00",22:"22:00-23:00",23:"23:00-24:00"}

#Get hourly data
data_to_plot=[]
for hour in hours:
    data=dailyData[dailyData['Hour']==hour]['kilometers']
    data_to_plot.append(data)

# Create a figure instance
fig = plt.figure(1, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)


## add patch_artist=True option to ax.boxplot() 
## to get fill color
bp = ax.boxplot(data_to_plot,showfliers=False, patch_artist=True)

## change outline color, fill color and linewidth of the boxes
for box in bp['boxes']:
    # change outline color
    box.set( color='black', linewidth=1, alpha=1)
    # change fill color
    box.set( facecolor = 'white' )

## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='black', linewidth=2)

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='red', linewidth=2)

## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='red', linewidth=1.5)

## change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', markerfacecolor='red', markeredgecolor="red", alpha=0.5,markersize=1)

## Custom x-axis labels
ax.set_xticklabels([get_hour.get(hour) for hour in hours], rotation =90)

## Remove top axes and right axes ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.set_ylabel('Distance(km)',fontdict={'fontsize':15,'color':'#de2d26'})
ax.set_xlabel('Hour',fontdict={'fontsize':15,'color':'#de2d26'})
ax.set_title('Distribution of hourly distance covered by eagle owl',fontdict={'fontsize':20,
 'fontweight':0,
 'color' :'blue',
 'verticalalignment': 'baseline'})

# Save the figure
fig.savefig('fig1.png', bbox_inches='tight')