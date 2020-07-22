"""Creates hourly vertical boxplot to show the distribution of hourly distances covered by birds, classified by gender"""

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
#convert distance in kilometers
dailyData['kilometers']=dailyData['distance']/1000
#get unique values for hour
condition=(dailyData['hour']< 4) | (dailyData['hour']>18)
dailyData=dailyData.loc[condition]
dailyData=dailyData[dailyData['kilometers']>0]
hours=dailyData.loc[condition]['hour'].unique()
hours.sort()
#Get hour interval from integer digits
get_hour={0:"00:00",1:"01:00",2:"02:00",3:"03:00",4:"04:00",5:"05:00",6:"06:00",7:"07:00",8:"08:00",9:"09:00",10:"10:00",11:"11:00",12:"12:00",13:"13:00",14:"14:00",15:"15:00",16:"16:00",17:"17:00",18:"18:00",19:"19:00",20:"20:00",21:"21:00",22:"22:00",23:"23:00"}


genders=["m","f"]
get_gender={"m":"male owl","f":"female owl"}
#Create dictionary to  store hourly male and female plot
hourlyDict={}
for hour in hours:
    hourlyData=dailyData[dailyData['hour']==hour]
    thisHourArray=[]
    for gender in genders:
        thisHourArray.append(hourlyData[hourlyData['gender']==gender]['kilometers'])
    hourdict={hour:thisHourArray}
    hourlyDict.update(hourdict)
    
i=0
ncols=len(hourlyDict)

# Create a figure instance
fig,axarr = plt.subplots(nrows=1,ncols=ncols,constrained_layout=False,figsize=(ncols *1.5,6),sharey=True,gridspec_kw = {'wspace':0, 'hspace':0}, dpi=600)

#Create hour-wise boxplot
for hour in hourlyDict.keys():
    ax=axarr[i]
    ax.set_facecolor("#f0f0f0")
    thisData=hourlyDict.get(hour)
    ## get fill color
    bp = ax.boxplot(thisData,vert=True,showfliers=False,patch_artist=True, widths=0.6)
    
    ## change outline color, fill color and linewidth of the boxes
    for box in bp['boxes']:
        # change outline color
        box.set( color='black', linewidth=1, alpha=1)
    
    
        # fill with colors
    colors = ['navy','orange']
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
        median.set(color='black', linewidth=1.5)
    
    ## change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', markerfacecolor='red', markeredgecolor="red", alpha=0.5,markersize=1)
    
    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set(xticklabels=genders, xlabel=get_hour.get(hour))
    i+=1

#Add title to the plot
fig.suptitle('Distribution of Hourly Distance travelled by eagle owl( Male Vs Female)',fontsize=20,color="black")
#fig.savefig('fig1.png', bbox_inches='tight')
fig.text(0.5, 0.01, 'Hour', ha='center', fontsize=14)
fig.text(0.08, 0.5, 'Hourly Distance (km)', va='center', rotation='vertical',fontsize=14)
# Save the figure
fig.savefig('fig1.png', bbox_inches='tight')
#plt.legend(loc=2)
plt.savefig(os.path.join(outputPath,"boxplot_gender_hourlyDistance"),dpi=600)
plt.show()