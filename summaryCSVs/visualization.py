# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 12:54:50 2020

@author: janak
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

hourdata = pd.read_csv('hourlyDistances.csv')
daydata = pd.read_csv('dailyDistances.csv')

hourdata['KM'] = round(hourdata['Distance']/1000,2)
condition = (hourdata['Hour']< 5) | (hourdata['Hour']> 17)
hourdata = hourdata.loc[condition]
hourdata = hourdata[hourdata['KM']>0]
hours = hourdata.loc[condition]['Hour'].unique()
hours.sort()
#Get hour interval from integer digits
get_hour={0:"00:00-01:00",1:"01:00-02:00",2:"02:00-03:00",3:"03:00-04:00",4:"04:00-05:00",5:"05:00-06:00",6:"06:00-07:00",7:"07:00-08:00",8:"08:00-09:00",9:"09:00-10:00",10:"10:00-11:00",11:"11:00-12:00",12:"12:00-13:00",13:"13:00-14:00",14:"14:00-15:00",15:"15:00-16:00",16:"16:00-17:00",17:"17:00-18:00",18:"18:00-19:00",19:"19:00-20:00",20:"20:00-21:00",21:"21:00-22:00",22:"22:00-23:00",23:"23:00-24:00"}


hourdist = hourdata[['Hour', 'Distance']].groupby(['Hour']).mean()
hours = hourdata['Hour'].unique()


#For 1.1 and 1.2a
fig, ax = plt.subplots(1,2, figsize = (12,4))
ax[0].bar(hourdist.index.values, hourdist['Distance'])
ax[0].set_title('Average hourly distance covered by eagle owl')
ax[0].set_xlabel('Hours')
ax[0].set_ylabel('Distance (km)')
ax[0].set_xticks([0,5,10,15,20,23])
ax[0].set_xticklabels(['00:00','05:00','10:00','15:00', '20:00', '23:00'])
ax[0].set_yticks([0,200,400,600,800,1000])
ax[0].set_yticklabels([0,0.2,0.4,0.6,0.8,1.0])

ci = 1.9*np.std(hourdata['Distance'])/np.mean(hourdata['Distance'])
ax[1].scatter(hourdata['Hour'], hourdata['Distance'])
#ax[1].fill_between(hourdata['Hour'], (hourdata['Distance'] - ci), (hourdata['Distance'] + ci), color = 'b', alpha=0.1)
ax[1].set_title('Hourly distances travelled by eagle owls')
ax[1].set_xlabel('Hours')
ax[1].set_ylabel('Distance (km)')
ax[1].set_xticks([0,5,10,15,20,23])
ax[1].set_xticklabels(['00:00','05:00','10:00','15:00', '20:00', '23:00'])
ax[1].set_yticks([0,2000,4000,6000,8000,10000])
ax[1].set_yticklabels([0,2,4,6,8,10])
trendline = np.polyfit(hourdata['Hour'], hourdata['Distance'],1)
trendline = np.poly1d(trendline)
plt.plot(hourdata['Hour'], trendline(hourdata['Hour']), 'b--')

fig.tight_layout()
plt.show()


#For 1.3 male and female comparison
hourgend = hourdata[['Gender','Hour', 'Distance']].groupby(['Gender', 'Hour']).mean()
hours = hourdata['Hour'].unique()

female_eagle_mean = hourgend.iloc[0:14,0:].values
female_eagle_mean = female_eagle_mean.T. flatten() #flatten `array_2d`
#female_hours = hourgend.iloc[0:14,0:].index.values


male_eagle_mean = hourgend.iloc[14:,0:].values
male_eagle_mean = male_eagle_mean.T. flatten() #flatten `array_2d`
male_eagle_mean = np.insert(male_eagle_mean, 6, 0, axis=None)

width = 0.44
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
rects1 = ax.bar(np.sort(hours) - width/2, male_eagle_mean, width, label='Male Eagle')
rects2 = ax.bar(np.sort(hours) + width/2, female_eagle_mean, width, label='Female Eagle')
#ax.bar(hours, male_eagle_mean, width, color = 'r')
#ax.bar(hours, female_eagle_mean, width, bottom = male_eagle_mean, color = 'b')
ax.legend(labels=['Men', 'Women'])
ax.set_ylabel('Distance (km)')
ax.set_title('Average hourly distance of male vs female eagle owl')
ax.set_xticks([0,5,10,15,20,23])
ax.set_xticklabels(['00:00','05:00','10:00','15:00', '20:00', '23:00'])
ax.set_yticks([200,400,600,800,1000,1200])
ax.set_yticklabels(['0.2','0.4','0.6','0.8', '1.0', '1.2'])

#Label the bar values
# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{:.1f}'.format((height/1000)),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')


# autolabel(rects1)
# autolabel(rects2)

plt.show()

#Stacked plot of male and female...
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(hours, male_eagle_mean, color = 'r')
ax.bar(hours, female_eagle_mean, width, bottom = male_eagle_mean, color = 'b')
ax.legend(labels=['Men', 'Women'])
ax.set_ylabel('Distance (m)')
ax.set_title('Average hourly distance of male vs female eagle owl')
ax.set_xticks([0,5,10,15,20,23])
ax.set_xticklabels(['00:00','05:00','10:00','15:00', '20:00', '23:00'])
plt.show()



#For 1.4
def get_seasonwise_data(dataset):
    autumndist, autumnhour, springdist, springhour, summerdist, summerhour, winterdist, winterhour = [],[],[],[],[],[],[],[]
    indices = dataset.index.values
    distances = dataset.values
    for indice, distance in zip(indices, distances):
        if indice[0] == 'Autumn':
            #print(indice[1], distance)
            autumndist.append(distance)
            autumnhour.append(indice[1])
        elif indice[0] == 'Spring':
            #print(indice[1], distance)
            springdist.append(distance)
            springhour.append(indice[1])
        elif indice[0] == 'Summer':
            #print(indice[1], distance)
            summerdist.append(distance)
            summerhour.append(indice[1])
        elif indice[0] == 'Winter':
            #print(indice[1], distance)
            winterdist.append(distance)
            winterhour.append(indice[1])
    return autumndist, autumnhour, springdist, springhour, summerdist, summerhour, winterdist, winterhour



hourseason = hourdata[['Season','Hour', 'KM']].groupby(['Season', 'Hour']).mean()
hours = hourdata['Hour'].unique()

#Implement the function to get the data
autumndist, autumnhour, springdist, springhour, summerdist, summerhour, winterdist, winterhour = get_seasonwise_data(hourseason)
#Summer season doesn't have data recorded at six, so we assign it zero distance
summerdist = np.insert(summerdist, 6, 0, axis=None)
summerhour = np.insert(summerhour, 6, 6, axis=None)
    
#Now plot the data
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
plt.plot(autumnhour, autumndist, label = 'Autumn', marker = 'o')
plt.plot(springhour, springdist, label = 'Spring', marker = '*')
plt.plot(summerhour, summerdist, label = 'Summer', marker = '+')
plt.plot(winterhour, winterdist, label = 'Winter', marker = 'v')

ax.set_xticks([0,5,10,15,20,23])
ax.set_xticklabels(['00:00','05:00','10:00','15:00', '20:00', '23:00'])
#ax.set_xticklabels([get_hour.get(hour) for hour in hours], rotation =90)
#ax.set_yticks([200,400,600,800,1000,1200])
#ax.set_yticklabels(['0.2','0.4','0.6','0.8', '1.0', '1.2'])
plt.xlabel('Hour in a day')
# Set the y axis label of the current axis.
plt.ylabel('Distance (km)')
# Set a title of the current axes.
plt.title('Season-wise variation in mobility pattern in a typical day ')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()


