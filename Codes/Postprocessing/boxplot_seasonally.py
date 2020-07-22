"""Displays daily distances covered by (all) birds in form on boxplot"""

## Create data
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Set project, input and output directory
projectDirectory="C:\\Users\\DELL\\Documents\\GitHub\\Project\\PIG_FinalProject"
inputCSV=os.path.join(projectDirectory, "Outputs/Processing/dailySummary.csv")
outputPath=os.path.join(projectDirectory, "Outputs/Postprocessing")
#Open csv file
dailyData=pd.read_csv(inputCSV)

dailyData['kilometers']=dailyData['distance']/1000
#get unique values for hour
dailyData=dailyData[dailyData['kilometers']>0]
seasons=list(dailyData['season'].unique())
sort_order={"Winter":0,"Spring":1,"Summer":2,"Autumn":3}
seasons.sort(key=lambda val:sort_order[val])

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
colors=['blue','orange','red','green']
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
    median.set(color='white', linewidth=1.5)

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
ax.set_ylabel('Daily Distance(km)', fontsize=14)
ax.set_xlabel('Season', fontsize=14)
ax.set_title('Season-wise daily distance travelled by eagle owl',fontdict={'fontsize':20,'fontweight':0,'color' :'black','verticalalignment':'baseline'})
# Save the figure
plt.savefig(os.path.join(outputPath,"boxplot_season"),dpi=600)
plt.show()