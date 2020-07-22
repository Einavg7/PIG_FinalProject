"""Creates hourly vertical boxplot to show the distribution of hourly distances covered by all birds"""
## Create data
import os
import matplotlib.pyplot as plt
import pandas as pd

#Set project, input and output directory
projectDirectory="C:\\Users\\DELL\\Documents\\GitHub\\Project\\PIG_FinalProject"
inputCSV=os.path.join(projectDirectory, "Outputs/Processing/hourlySummary.csv")
outputPath=os.path.join(projectDirectory, "Outputs/Postprocessing")

#Open csv file
dailyData=pd.read_csv(inputCSV)
#calculate distance in kilometers
dailyData['kilometers']=dailyData['distance']/1000
#get unique values for hour
condition=(dailyData['hour']< 4) | (dailyData['hour']>18)
dailyData=dailyData.loc[condition]
dailyData=dailyData[dailyData['kilometers']>0]
hours=dailyData.loc[condition]['hour'].unique()
hours.sort()
#Get hour interval from integer digits
get_hour={0:"00:00",1:"01:00",2:"02:00",3:"03:00",4:"04:00",5:"05:00",6:"06:00",7:"07:00",8:"08:00",9:"09:00",10:"10:00",11:"11:00",12:"12:00",13:"13:00",14:"14:00",15:"15:00",16:"16:00",17:"17:00",18:"18:00",19:"19:00",20:"20:00",21:"21:00",22:"22:00",23:"23:00"}

#Get hourly data
data_to_plot=[]
for hour in hours:
    data=dailyData[dailyData['hour']==hour]['kilometers']
    data_to_plot.append(data)

# Create a figure instance
fig = plt.figure(1, figsize=(9, 6), dpi=600)

# Create an axes instance
ax = fig.add_subplot(111)

bp = ax.boxplot(data_to_plot,showfliers=False, patch_artist=True)

## change outline color, fill color and linewidth of the boxes
for box in bp['boxes']:
    # change outline color
    box.set( color='black', linewidth=1, alpha=1)
    # change fill color
    box.set( facecolor = 'white' )

## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='red', linewidth=1.5)

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='black', linewidth=1.5)

## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='green', linewidth=1.5)

## change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', markerfacecolor='red', markeredgecolor="red", alpha=0.5,markersize=1)

## Custom x-axis labels
ax.set_xticklabels([get_hour.get(hour) for hour in hours], rotation =0,)

## Remove top axes and right axes ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.set_ylabel('Distance(km)',fontdict={'fontsize':15,'color':'blue'})
ax.set_xlabel('Hours',fontdict={'fontsize':15,'color':'blue'})

#Add title to the plot
fig.suptitle('Distribution of Hourly Distance travelled by eagle owl',fontsize=20,color="black")
plt.savefig(os.path.join(outputPath,"boxplot_hour"),dpi=600)


