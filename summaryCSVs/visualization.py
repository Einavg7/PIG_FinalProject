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

hourdist = hourdata[['Hour', 'Distance']].groupby(['Hour']).mean()
hours = hourdata['Hour'].unique()


#For 1.1 and 1.2a
fig, ax = plt.subplots(1,2, figsize = (12,4))
ax[0].bar(hourdist.index.values, hourdist['Distance'])
ax[0].set_title('Average hourly distance covered by eagle owl')
ax[0].set_xlabel('Hours')
ax[0].set_ylabel('Distance (m)')
ax[0].set_xticks([0,5,10,15,20,23])
ax[0].set_xticklabels(['00:00','05:00','10:00','15:00', '20:00', '23:00'])

ax[1].scatter(hourdata['Hour'], hourdata['Distance'])
ax[1].set_title('Hourly distances travelled by eagle owls')
ax[1].set_xlabel('Hours')
ax[1].set_ylabel('Distance (m)')
ax[1].set_xticks([0,5,10,15,20,23])
ax[1].set_xticklabels(['00:00','05:00','10:00','15:00', '20:00', '23:00'])
trendline = np.polyfit(hourdata['Hour'], hourdata['Distance'],1)
trendline = np.poly1d(trendline)
plt.plot(hourdata['Hour'], trendline(hourdata['Hour']), 'b--')


fig.tight_layout()
plt.show()


#For 1.3 male and female comparison
hourgend = hourdata[['Gender','Hour', 'Distance']].groupby(['Gender', 'Hour']).mean()
hours = hourdata['Hour'].unique()

male_eagle_mean = hourgend.iloc[0:14,0:].values
male_eagle_mean = male_eagle_mean.T. flatten() #flatten `array_2d`

female_eagle_mean = hourgend.iloc[14:,0:].values
female_eagle_mean = male_eagle_mean.T. flatten() #flatten `array_2d`


width = 0.75
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(hours, male_eagle_mean, width, color = 'r')
ax.bar(hours, female_eagle_mean, width, bottom = male_eagle_mean, color = 'b')
ax.legend(labels=['Men', 'Women'])
ax.set_ylabel('Distance (m)')
ax.set_title('Average hourly distance of male vs female eagle owl')
ax.set_xticks([0,5,10,15,20,23])
ax.set_xticklabels(['00:00','05:00','10:00','15:00', '20:00', '23:00'])
plt.show()



