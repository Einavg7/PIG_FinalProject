
## Create data
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams as rcParams
#Open csv file
dailyData=pd.read_csv(r"C:\Users\DELL\Documents\GitHub\Project\PIG_FinalProject\summaryCSVs\dailyDistances.csv")
dailyData['kilometers']=dailyData['Distance']/1000

dailyData=dailyData[dailyData['kilometers']>0]
seasons=dailyData['season'].unique()
seasons.sort()

genders=["f","m"]
get_gender={"m":"male owl","f":"female owl"}
#Create dictionary to  store hourly male and female plot
seasonwiseDict={}
for season in seasons:
    seasonalData=dailyData[dailyData['season']==season]
    thisseasonArray=[]
    for gender in genders:
        thisseasonArray.append(seasonalData[seasonalData['Gender']==gender]['kilometers'])
    seasonDict={season:thisseasonArray}
    seasonwiseDict.update(seasonDict)
    
i=0
ncols=len(seasonwiseDict)


# Create a figure instance
fig,axarr = plt.subplots(nrows=1,ncols=ncols,constrained_layout=False,figsize=(12, ncols*2),sharey=True,gridspec_kw = {'wspace':0, 'hspace':0})


for season in seasonwiseDict.keys():
    ax=axarr[i]
    ax.set_facecolor("#f0f0f0")
    thisData=seasonwiseDict.get(season)
    ## add patch_artist=True option to ax.boxplot() 
    ## to get fill color
    bp = ax.boxplot(thisData,vert=True,showfliers=False,patch_artist=True, widths=0.6)
    
    ## change outline color, fill color and linewidth of the boxes
    for box in bp['boxes']:
        # change outline color
        box.set( color='black', linewidth=1, alpha=1)
    
    
        # fill with colors
    colors = ['#e7e1ef', '#fee6ce']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
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
    
    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    #ax.set_xlabel('Distance(km)',fontdict={'fontsize':15,'color':'#de2d26'})
    ax.set(xticklabels=genders, xlabel=season)
    #ax.set_ylabel(get_hour.get(hour),fontdict={'fontsize':15,'color':'#de2d26'})
    #ax.set_title('Distribution of hourly distance covered by eagle owl',fontdict={'fontsize':20,'fontweight':0,'color' :'blue','verticalalignment':'baseline'})
    i+=1

#Add axes to the plot
#plt.ylabel("Daily distance(km)",fontdict={'fontsize':20,'fontweight':0,'color' :'blue'})
fig.suptitle('Distribution of daily distance covered by eagle owl, Mave Vs Female',fontsize=25,color="green")
# Save the figure
fig.savefig('fig1.png', bbox_inches='tight')