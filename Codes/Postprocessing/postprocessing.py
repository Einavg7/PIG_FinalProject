import os
import qgis
from qgis.core import (
    QgsVectorLayer
)
import csv
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
import matplotlib.dates as mdates
from math import floor

#Set project, input and output directory
#projectDirectory="C:\\Users\\DELL\\Documents\\GitHub\\Project\\PIG_FinalProject"
#inputCSV_daily=os.path.join(projectDirectory, "Outputs/Processing/dailySummary.csv")
#inputCSV_hourly=os.path.join(projectDirectory, "Outputs/Processing/hourlySummary.csv")
#outputPath=os.path.join(projectDirectory, "Outputs/Postprocessing")


inputCSV_hourly = "C:\\Users\\einav\\Dropbox\\summer semester 2020\\Python in GIS\\Final Project\\hourlySummary.csv"
inputCSV_daily="C:\\Users\\einav\\Dropbox\\summer semester 2020\\Python in GIS\\Final Project\\dailySummary.csv"
outputPath = "C:\\Users\\einav\\Dropbox\\summer semester 2020\\Python in GIS\\Final Project"

#Open csv file
hourlyData=pd.read_csv(inputCSV_hourly)

hourlyData['kilometers']=hourlyData['distance']/1000

condition=(hourlyData['hour']< 4) | (hourlyData['hour']>18)
hourlyData=hourlyData.loc[condition]
hourlyData=hourlyData[hourlyData['kilometers']>0]
hours=hourlyData.loc[condition]['hour'].unique()
hours.sort()

#Get hour interval from integer digits
get_hour={0:"00:00",1:"01:00",2:"02:00",3:"03:00",4:"04:00",5:"05:00",6:"06:00",7:"07:00",8:"08:00",9:"09:00",10:"10:00",11:"11:00",12:"12:00",13:"13:00",14:"14:00",15:"15:00",16:"16:00",17:"17:00",18:"18:00",19:"19:00",20:"20:00",21:"21:00",22:"22:00",23:"23:00"}


"""Creates the polarplot showing average hourly distance travelled by all of the owls"""

#Get hourly data stored to arrary
hourlyAverageDistance=[]
for hour in hours:
    selectedDistance=hourlyData[hourlyData['hour']==hour]["kilometers"].mean()
    hourlyAverageDistance.append(selectedDistance)

# Compute pie slices
theta =  [hour * np.pi/12.0 +7.5*np.pi/180 for hour in hours]
radii = hourlyAverageDistance
width = np.pi / 12
colors = [plt.cm.jet(x/max(hourlyAverageDistance)) for x in radii]

fig0 = plt.figure()

axp = plt.axes(projection='polar')
axp.bar(theta, radii, width=width, bottom=0.0,color=colors, alpha=0.5)

# Make the labels go clockwise
axp.set_theta_direction(-1)

#Place Zero at 12'o clock position
axp.set_theta_offset(np.pi/2)

#Set the circumference ticks
axp.set_xticks(np.linspace(0, 2*np.pi, 24, endpoint=False))

# set the label names
ticks = [i for i in range(24)]
#Get formatted time
formattedHour={0:"00:00",1:"01:00",2:"02:00",3:"03:00",4:"04:00",5:"05:00",6:"06:00",7:"07:00",8:"08:00",9:"09:00",10:"10:00",11:"11:00",12:"12:00",13:"13:00",14:"14:00",15:"15:00",16:"16:00",17:"17:00",18:"18:00",19:"19:00",20:"20:00",21:"21:00",22:"22:00",23:"23:00"}
axp.set_xticklabels(formattedHour.get(i) for i in range(24))
#plt.set_title('Average Hourly distance(in km) \ntravelled by eagle owl',fontdict={'fontsize':14,'fontweight':0,'color' :'#3182bd','verticalalignment':'baseline', "y":1.15})


# show the radial labels
plt.setp(axp.get_yticklabels(), visible=True)
plt.title('Average Hourly Distance(km) \nTravelled by Eagle Owl')#,fontdict={'fontsize':14,'fontweight':0,'color' :'#3182bd','verticalalignment':'baseline', "y":1.15})
plt.savefig(os.path.join(outputPath,"polarPlot_hourly.png"), dpi=600, format='png')

#show the plot
plt.show()

"""Creates hourly vertical boxplot to show the distribution of hourly distances covered by all owls"""

#Get hourly data
data_to_plot=[]
for hour in hours:
    data=hourlyData[hourlyData['hour']==hour]['kilometers']
    data_to_plot.append(data)

# Create a figure instance
fig = plt.figure(1, figsize=(9,6), dpi=600)
#figsize=(9, 6)
# Create an axes instance
axh = plt.axes(facecolor= 'w')

bp = axh.boxplot(data_to_plot,showfliers=False, patch_artist=True)

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
axh.set_xticklabels([get_hour.get(hour) for hour in hours], rotation =0,)

## Remove top axes and right axes ticks
axh.get_xaxis().tick_bottom()
axh.get_yaxis().tick_left()
axh.set_ylabel('Distance(km)',fontdict={'fontsize':15,'color':'blue'})
axh.set_xlabel('Hours',fontdict={'fontsize':15,'color':'blue'})

#Add title to the plot
#fig.suptitle('Distribution of Hourly Distance travelled by eagle owl',fontsize=20,color="black")
plt.title('Distribution of Hourly Distance travelled by eagle owl')

plt.savefig(os.path.join(outputPath,"boxplot_hour.png"), dpi=600, format='png')
plt.show()


"""Creates hourly vertical boxplot to show the distribution of hourly distances covered by owls, classified by gender"""


genders=["m","f"]
get_gender={"m":"male owl","f":"female owl"}

#Create dictionary to  store hourly male and female plot
hourlyDict={}
for hour in hours:
    hourly=hourlyData[hourlyData['hour']==hour]
    thisHourArray=[]
    for gender in genders:
        thisHourArray.append(hourly[hourly['gender']==gender]['kilometers'])
    hourdict={hour:thisHourArray}
    hourlyDict.update(hourdict)
    
i=0
ncols=len(hourlyDict)

# Create a figure instance
fig1 ,axarr = plt.subplots(nrows=1,ncols=ncols,constrained_layout=False,figsize=(ncols *1.5,6),sharey=True,gridspec_kw = {'wspace':0, 'hspace':0}, dpi=600)

#Create hour-wise boxplot
for hour in hourlyDict.keys():
    axhg=axarr[i]
    axhg.set_facecolor("#f0f0f0")
    thisData=hourlyDict.get(hour)
    ## get fill color
    bp = axhg.boxplot(thisData,vert=True,showfliers=False,patch_artist=True, widths=0.6)
    
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
    axhg.get_xaxis().tick_bottom()
    axhg.get_yaxis().tick_left()
    axhg.set(xticklabels=genders, xlabel=get_hour.get(hour))
    i+=1

#Add title to the plot
fig1.suptitle('Distribution of Hourly Distance Travelled by Eagle Owl (Male vs Female)',fontsize=20,color="black")
#fig.savefig('fig1.png', bbox_inches='tight')
fig1.text(0.5, 0.01, 'Hour', ha='center', fontsize=14)
fig1.text(0.08, 0.5, 'Hourly Distance (km)', va='center', rotation='vertical',fontsize=14)
# Save the figure

plt.savefig(os.path.join(outputPath,"boxplot_gender_hourlyDistance.png"), dpi=600, format='png')
plt.show()

"""Creates a bar chart presenting the average hourly distance traveled by the owls, classified by gender"""

#For 1.3 male and female comparison
hourgend = hourlyData[['gender','hour', 'distance']].groupby(['gender', 'hour']).mean()

female_eagle_mean = hourgend.iloc[0:9,0:].values
female_eagle_mean = female_eagle_mean.T. flatten() #flatten `array_2d`


male_eagle_mean = hourgend.iloc[9:,0:].values
male_eagle_mean = male_eagle_mean.T. flatten() #flatten `array_2d`

width = 0.44
fig2 = plt.figure()
axhb = plt.axes(facecolor='w')
rects1 = axhb.bar(np.sort(hours) - width/2, male_eagle_mean, width, label='Male Eagle')
rects2 = axhb.bar(np.sort(hours) + width/2, female_eagle_mean, width, label='Female Eagle')

axhb.legend(labels=['Male', 'Female'])
axhb.set_ylabel('Distance (km)')
axhb.set_title('Average Hourly Distance of Male vs Female Eagle Owls')
axhb.set_xticks([0,5,10,15,20,23])
axhb.set_xticklabels(['00:00','05:00','10:00','15:00', '20:00', '23:00'])

axhb.set_yticklabels(['0.2','0.4','0.6','0.8', '1.0', '1.2'])
plt.savefig(os.path.join(outputPath,"MFHourly.png"), dpi=600, format='png')
plt.show()

"""Creates a bar chart presenting the average distance traveled by the owls, classified by gender"""
#Open csv file
dailyData=pd.read_csv(inputCSV_daily)

dailyData['kilometers']=dailyData['distance']/1000
#get unique values for hour
dailyData=dailyData[dailyData['kilometers']>0]
seasons=list(dailyData['season'].unique())
sort_order={"Winter":0,"Spring":1,"Summer":2,"Autumn":3}
seasons.sort(key=lambda val:sort_order[val])

fig3 = plt.figure()
ax0 = plt.axes(facecolor='w')
## plot by gender
ax0 = dailyData.groupby('gender')['kilometers'].mean().plot(kind='barh',title='Average daily distance traveled by Gender (Male vs Female)',
                                                                    color=["orange","navy"])
## male: 10.2, female: 7.139
ax0.set_yticklabels(["Female", "Male"])
ax0.set_xlabel('Distance (km)')
ax0.set_ylabel('')
plt.savefig(os.path.join(outputPath,"gender_avg_dist.png"), dpi=600, format='png')

plt.show()

"""Displays daily distances traveled by (all) owls in form on boxplot, season wise"""

#Get season-wise data
data_to_plot=[]
for season in seasons:
    data=dailyData[dailyData['season']==season]['kilometers']
    data_to_plot.append(data)

# Create a figure instance
fig4= plt.figure()

# Create an axes instance
axb = plt.axes(facecolor='w')


## add patch_artist=True option to ax.boxplot() 
## to get fill color
bp = axb.boxplot(data_to_plot,showfliers=False, patch_artist=True)

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
axb.set_xticklabels( seasons, rotation =0)

## Remove top axes and right axes ticks
axb.get_xaxis().tick_bottom()
axb.get_yaxis().tick_left()
axb.set_ylabel('Daily Distance(km)')
axb.set_xlabel('Season')
axb.set_title('Seasonal Daily Distance Travelled by Eagle Owls')#(,fontdict={'fontsize':20,'fontweight':0,'color' :'black','verticalalignment':'baseline'})
# Save the figure
plt.savefig(os.path.join(outputPath,"boxplot_season.png"), dpi=600, format='png')
plt.show()

""" Creates grouped bar diagram  with season as groups and each male and female owls average daily distance in kilometers """

#List genders
genders=["f","m"]

#Create array of season-wise average distance for male and female
maleDistances,femaleDistances=[],[]

#Populate seasonwise data for both male and female
for season in seasons:
    seasonalData=dailyData[dailyData['season']==season]
    maleDistance=seasonalData[seasonalData['gender']=="m"]['kilometers'].mean()
    femaleDistance=seasonalData[seasonalData['gender']=="f"]['kilometers'].mean()
    maleDistances.append(maleDistance)
    femaleDistances.append(femaleDistance)
# set width of bar
barWidth = 0.25

# Set position of bar on X axis
r1 = np.arange(len(femaleDistances))
r2 = [x + barWidth for x in r1]

# Create a figure instance
fig5= plt.figure()

# Create an axes instance
axbg = plt.axes(facecolor='w')

# Make the plot
axbg.bar(r1, maleDistances, color='navy', width=barWidth, edgecolor='white', label='male owl')
axbg.bar(r2, femaleDistances, color='orange', width=barWidth, edgecolor='white', label='female owl')

# Add xticks on the middle of the group bars
plt.xlabel('Season')
plt.xticks([r + barWidth for r in range(len(femaleDistances))], seasons)
plt.title("Average Daily Distance Travelled by Season and Gender")
plt.ylabel("Average Daily Distance(km)")

# Create legend & Show graphic
plt.legend(loc=2)
plt.savefig(os.path.join(outputPath,"bar_gender_season.png"), dpi=600, format='png')
plt.show()

""" Creates scatter plot for hourly distance travelled eagle owls in each day of the year colored by season """

df = dailyData
df["day-month"] = pd.to_datetime(df["day-month"], format='%d-%b', errors = 'coerce')
## create variables to plot
days = df['day-month'].unique()
days.sort()
index = [0]
days = np.delete(days, index)
avg_dist = df.groupby('day-month')['kilometers'].mean()
season = df.groupby('day-month')['season'].unique()

# Function to map the colors as a list from the input list of x variables
def pltcolor(lst):
    cols=[]
    for l in lst:
        if l=='Autumn':
            cols.append('green')
        elif l=='Winter':
            cols.append('blue')
        elif l=='Spring':
            cols.append('orange')
        elif l=='Summer':
            cols.append('red')
    return cols
# Create the colors list using the function above
cols=pltcolor(season)

# plot avg_dist vs days
f, ax  = plt.subplots(1)
ax.scatter(days, avg_dist, c=cols)
ax.plot(avg_dist.mean(), linewidth = 1)
ax.set_title('Average Daily Distance Traveled for Each Day of the Year')
ax.set_xlabel('Day/Month')
ax.set_ylabel('Distance (km)')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
datemin = np.datetime64(days[0])
datemax = np.datetime64(days[364])
ax.set_xlim(datemin, datemax)

## add legend (try make patches circles..)
legend_dict = { 'Autumn' : 'green', 'Summer' : 'red', 'Winter' : 'blue', 'Spring' : 'orange' }
patchList = []
for key in legend_dict:
        data_key =  mlines.Line2D([], [], linestyle="none", marker = 'o',color=legend_dict[key], label=key)
        patchList.append(data_key)
ax.legend(handles=patchList, loc=8, ncol=2)


plt.xticks(rotation = 45)
plt.savefig(os.path.join(outputPath,"daily_avg_dist.png"), dpi=600, format='png')

plt.show()

""" Creates polarplot for hourly distance travelled eagle owls in each season. Polar plots are arranged in 2 x 2 grid. """

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
maxRadius=getRadius(hourlyData)


# Four polar axes
nrows,ncols=2,2
figp,axarr =plt.subplots(nrows,ncols, figsize=(10,10),subplot_kw=dict(polar=True), constrained_layout=True)


for i in range(len(seasons)):
    row=floor(i/2)
    col=i%2
    ax=axarr[row,col]
    season=seasons[i]
    seasonalData=hourlyData[hourlyData['season']==season]
    hours=list(hourlyData['hour'].unique())
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
figp.suptitle('Seasonal Variation of Average Hourly Distance(km)\n Travelled by Eagle Owl', fontsize=20)

plt.savefig(os.path.join(outputPath,"polar_hour_season.png"), dpi=600, format='png')
plt.show()

""" Creates 2 plots for distance travelled for owl tags = 1753, 3893, 3896, 3897, females and males """
df = dailyData
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
fig.suptitle('Daily Distance Traveled - \nFemale Eagle Owls 1753 & 3897', fontsize=24)

ax1 = df[df.tag_ident == 1753].plot(x = 'date', y = 'kilometers', color = 'cyan',
  ax=axes[0])
L=ax1.legend()
L.get_texts()[0].set_text('Owl 1753')
ax1.set_xlabel('')
ax1.set_ylabel('Distance (km)')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

ax2 = df[df.tag_ident == 3897].plot(x = 'date', y = 'kilometers', color = 'navy', 
        ax=axes[1])
L2=ax2.legend()
L2.get_texts()[0].set_text('Owl 3897')
ax2.set_xlabel('Date')
ax2.set_ylabel('Distance (km)')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

plt.savefig(os.path.join(outputPath,"female_birds_dailydist.png"), dpi=600, format='png')
plt.show()



fig2, axes2 = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
fig2.suptitle('Daily Distance Traveled - \nMale Eagle Owls 3893 & 3896 in 2014', fontsize=24)

ax3 = df[df.tag_ident == 3893].plot(x = 'date', y = 'kilometers',
        color='purple', ax=axes2[0])
L3=ax3.legend()
L3.get_texts()[0].set_text('Owl 3893')
ax3.set_xlabel('')
ax3.set_ylabel('Distance (km)')
months3 = mdates.MonthLocator()
ax3.xaxis.set_major_locator(months3)
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))


ax4 = df[df.tag_ident == 3896].plot(x = 'date', y = 'kilometers',
        color='magenta', ax=axes2[1])
L4=ax4.legend()
L4.get_texts()[0].set_text('Owl 3896')
ax4.set_xlabel('Date')
ax4.set_ylabel('Distance (km)')
months4 = mdates.MonthLocator()
ax4.xaxis.set_major_locator(months4)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))

#save fig
plt.savefig(os.path.join(outputPath,"male_birds_dailydist.png"), dpi=600, format='png')

plt.show()
