"""Displays daily distances covered by (all) birds in form on boxplot"""

## Create data
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Open csv file
dailyData=pd.read_csv(r"C:\Users\DELL\Documents\GitHub\Project\PIG_FinalProject\summaryCSVs\dailyDistances.csv")
dailyData['kilometers']=dailyData['Distance']/1000
#get unique values for hour
dailyData=dailyData[dailyData['kilometers']>0]
seasons=dailyData['season'].unique()
seasons.sort()

#Get season-wise data
data_to_plot=[]
for season in seasons:
    data=dailyData[dailyData['season']==season]['kilometers']
    data_to_plot.append(data)

# Create a figure instance
fig = plt.figure(1, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)


## add patch_artist=True option to ax.boxplot() 
## to get fill color
bp = ax.boxplot(data_to_plot,showfliers=False, patch_artist=True)

## change outline color, fill color and linewidth of the boxes
colors=['lightgreen','orange','brown','yellow']
for box in bp['boxes']:
    # change outline color
    box.set( color='#7570b3', linewidth=1)

## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='#7570b3', linewidth=2)


        
## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='#7570b3', linewidth=2)

## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='blue', linewidth=1.5)

colors=['#deebf7','#fde0dd','#fee6ce','#eff5a0']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    
## change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', markerfacecolor='red', markeredgecolor="red", alpha=0.5,markersize=1)

## Custom x-axis labels
ax.set_xticklabels( seasons, rotation =0)

## Remove top axes and right axes ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.set_ylabel('Daily Distance(km)')
ax.set_xlabel('Season')
ax.set_title('Daily distance covered by eagle owl per season',fontdict={'fontsize':20,'fontweight':0,'color' :'black','verticalalignment':'baseline'})
# Save the figure
fig.savefig('fig1.png', bbox_inches='tight')