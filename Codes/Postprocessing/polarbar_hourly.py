"""Creates the polarplot showing average hourly distance travelled by all of the birds"""

## Create data
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#Set project, input and output directory
projectDirectory="C:\\Users\\DELL\\Documents\\GitHub\\Project\\PIG_FinalProject"
inputCSV=os.path.join(projectDirectory, "Outputs/Processing/hourlySummary.csv")
outputPath=os.path.join(projectDirectory, "Outputs/Postprocessing")
#Open csv file
dailyData=pd.read_csv(inputCSV)

dailyData['kilometers']=dailyData['distance']/1000

condition=(dailyData['hour']< 4) | (dailyData['hour']>18)
dailyData=dailyData.loc[condition]
dailyData=dailyData[dailyData['kilometers']>0]
hours=dailyData.loc[condition]['hour'].unique()
hours.sort()

#Get hourly data stored to arrary
hourlyAverageDistance=[]
for hour in hours:
    selectedDistance=dailyData[dailyData['hour']==hour]["kilometers"].mean()
    hourlyAverageDistance.append(selectedDistance)

# Compute pie slices
theta =  [hour * np.pi/12.0 +7.5*np.pi/180 for hour in hours]
radii = hourlyAverageDistance
width = np.pi / 12
colors = [plt.cm.jet(x/max(hourlyAverageDistance)) for x in radii]

ax = plt.subplot(111, projection='polar')
ax.bar(theta, radii, width=width, bottom=0.0,color=colors, alpha=0.5)

# Make the labels go clockwise
ax.set_theta_direction(-1)

#Place Zero at 12'o clock position
ax.set_theta_offset(np.pi/2)

#Set the circumference ticks
ax.set_xticks(np.linspace(0, 2*np.pi, 24, endpoint=False))

# set the label names
ticks = [i for i in range(24)]
#Get formatted time
formattedHour={0:"00:00",1:"01:00",2:"02:00",3:"03:00",4:"04:00",5:"05:00",6:"06:00",7:"07:00",8:"08:00",9:"09:00",10:"10:00",11:"11:00",12:"12:00",13:"13:00",14:"14:00",15:"15:00",16:"16:00",17:"17:00",18:"18:00",19:"19:00",20:"20:00",21:"21:00",22:"22:00",23:"23:00"}
ax.set_xticklabels(formattedHour.get(i) for i in range(24))
ax.set_title('Average Hourly distance(in km) \ntravelled by eagle owl',fontdict={'fontsize':14,'fontweight':0,'color' :'#3182bd','verticalalignment':'baseline', "y":1.15})


# show the radial labels
plt.setp(ax.get_yticklabels(), visible=True)
plt.savefig(os.path.join(outputPath,"polarPlot_hourly"), dpi=600)
#show the plot
plt.show()

