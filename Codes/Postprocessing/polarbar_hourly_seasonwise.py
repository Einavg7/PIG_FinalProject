"Creates polarplot for hourly distance travelled eagle owls in each season. Polar plots are arranged in 2 x 2 grid."
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import floor

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
seasons=list(dailyData.loc[condition]['season'].unique())
sort_order={"Winter":0,"Spring":1,"Summer":2,"Autumn":3}
seasons.sort(key=lambda val:sort_order[val])
hours.sort()

#Create maximum possible value of average hourly distance
def getRadius(df):
    distances=[]
    seasons=df['season'].unique()
    for season in seasons:
        seasonalData=df[df['season']==season]
        hours=seasonalData['hour'].unique()
        for hour in hours:
            hourlyAverage=seasonalData[seasonalData['hour']==hour]['kilometers'].mean()
            distances.append(hourlyAverage)
    return max(distances)
maxRadius=getRadius(dailyData)


import matplotlib.pyplot as plt
import numpy as np


# Four polar axes
nrows,ncols=2,2
fig,axarr =plt.subplots(nrows,ncols, figsize=(10,10),subplot_kw=dict(polar=True), constrained_layout=True)


for i in range(len(seasons)):
    row =floor(i/2)
    col=i%2
    ax=axarr[row,col]
    season=seasons[i]
    seasonalData=dailyData[dailyData['season']==season]
    hours=list(seasonalData['hour'].unique())
    hours.sort()
    hourlyAverageDistance=[]
    for hour in hours:
        selectedDistance=seasonalData[seasonalData['hour']==hour]["kilometers"].mean()
        hourlyAverageDistance.append(selectedDistance)
                
    # Compute pie slices
    theta =  [hour * np.pi/12.0 +7.5*np.pi/180 for hour in hours]
    radii = hourlyAverageDistance
    width = np.pi / 12
    colors = [plt.cm.viridis(x/maxRadius) for x in radii]
    
    #ax = plt.subplot(111, projection='polar')
    ax.bar(theta, radii, width=width, bottom=0.0,color=colors, alpha=0.5)
    
    # Make the labels go clockwise
    ax.set_theta_direction(-1)
    
    #Place Zero at Top
    ax.set_theta_offset(np.pi/2)
    
    #Set the circumference ticks
    ax.set_xticks(np.linspace(0, 2*np.pi, 24, endpoint=False))
    
    # set the label names
    ticks = [i for i in range(24)]

    #Get formatted time
    formattedHour={0:"00:00",1:"01:00",2:"02:00",3:"03:00",4:"04:00",5:"05:00",6:"06:00",7:"07:00",8:"08:00",9:"09:00",10:"10:00",11:"11:00",12:"12:00",13:"13:00",14:"14:00",15:"15:00",16:"16:00",17:"17:00",18:"18:00",19:"19:00",20:"20:00",21:"21:00",22:"22:00",23:"23:00"}
    ax.set_xticklabels(formattedHour.get(i) for i in range(24))
    ax.set_rlim(0,maxRadius)
    ax.set_title(season, fontdict={'fontsize':10,'verticalalignment': 'baseline', 'horizontalalignment': 'center', 'color':"#e6550d"})
    # show the radial labels
plt.setp(ax.get_yticklabels(), visible=True)
plt.suptitle('Seasonal variation of average hourly distance (km) travelled by eagle owl',fontdict={'fontsize':19,'color' :'black','verticalalignment':'baseline', "y":1.15})
    #plt.title("Hourly Distance")

plt.savefig(os.path.join(outputPath,"polar_hour_season"),dpi=600)
plt.show()

