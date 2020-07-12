import numpy as np
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
import matplotlib.dates as mdates

myfile = "C:\\Users\\einav\\Dropbox\\summer semester 2020\\Python in GIS\\Final Project\\dailyDistances2.csv"

df = pd.read_csv(myfile)

## add km column
df['Distance_km'] = df.Distance / 1000
# print(df)



## plot by gender
ax = df.groupby('Gender')['Distance_km'].mean().plot(kind='barh',title='Average distance traveled - Gender',
                                                                    color=["cyan", "purple"])
## male: 10.2, female: 7.139
ax.set_yticklabels(["Female", "Male"])
ax.set_xlabel('Distance (km)')
ax.set_ylabel('')
#plt.savefig('gender_avg_dist.png', dpi=300, format='png')
plt.show()


## plot by season
ax1 = df.groupby('season')['Distance_km'].mean().plot(kind='bar', title='Average distance traveled - Season',
                                               color=['green', 'orange', 'red', 'blue'] )
ax1.set_ylabel('Distance (km)')
ax1.set_xlabel('Season')
## summer : 8.689, autumn : 8.519, spring : 7.154, winter : 5.289
plt.xticks(rotation=45)
#plt.savefig('season_avg_dist.png', dpi=300,format='png')
plt.show()

## plot by owl
##df.groupby('tag_ident')['Distance_km'].agg(lambda x: sum(x)).plot(kind='bar',
##                                                                  title='Total distance traveled by each Eagle Owl')
##plt.savefig('owl_dist.png', dpi=300,format='png')
##plt.show()

## change to date objects - important to make sure the date field is this format
df["day-month"] = pd.to_datetime(df["day-month"], format='%m/%d/%Y')
df['arbDate'] = pd.to_datetime(df['arbDate'], format='%m/%d/%Y')
#df.info()

## create variables to plot
days = df['day-month'].unique()
avg_dist = df.groupby('day-month')['Distance_km'].mean()
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
ax.set_title('Average daily distance traveled for each day of the year')
ax.set_xlabel('Day/Month')
ax.set_ylabel('Distance (km)')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
datemin = np.datetime64(days[0])
datemax = np.datetime64(days[365])
ax.set_xlim(datemin, datemax)

## add legend (try make patches circles..)
legend_dict = { 'Autumn' : 'green', 'Summer' : 'red', 'Winter' : 'blue', 'Spring' : 'orange' }
patchList = []
for key in legend_dict:
        data_key =  mlines.Line2D([], [], linestyle="none", marker = 'o',color=legend_dict[key], label=key)
        patchList.append(data_key)
ax.legend(handles=patchList, loc=2, ncol=2)

## trend line
x = mdates.date2num(days)
z = np.polyfit(x, avg_dist,1)
p = np.poly1d(z)
ax.plot(x, p(x), '-', c='k', linewidth=2)

plt.xticks(rotation = 45)
#plt.savefig('daily_avg_dist.png', dpi=300, format='png')
plt.show()

## plot distances for owl tags = 1753, 3893, 3896, 3897

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
fig.suptitle('Daily distance traveled - \nFemale Eagle Owls 1753 & 3897', fontsize=24)

ax1 = df[df.tag_ident == 1753].plot(x = 'arbDate', y = 'Distance_km', color = 'cyan',
  ax=axes[0])
L=ax1.legend()
L.get_texts()[0].set_text('Owl 1753')
ax1.set_xlabel('')
ax1.set_ylabel('Distance (km)')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

ax2 = df[df.tag_ident == 3897].plot(x = 'arbDate', y = 'Distance_km', color = 'navy', 
        ax=axes[1])
L2=ax2.legend()
L2.get_texts()[0].set_text('Owl 3897')
ax2.set_xlabel('Date')
ax2.set_ylabel('Distance (km)')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.savefig('female_birds_dailydist.png', dpi=300, format='png')
plt.show()



fig2, axes2 = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
fig2.suptitle('Daily distance traveled - \nMale Eagle Owls 3893 & 3896 in 2014', fontsize=24)

ax3 = df[df.tag_ident == 3893].plot(x = 'arbDate', y = 'Distance_km',
        color='purple', ax=axes2[0])
L3=ax3.legend()
L3.get_texts()[0].set_text('Owl 3893')
ax3.set_xlabel('')
ax3.set_ylabel('Distance (km)')
months3 = mdates.MonthLocator()
ax3.xaxis.set_major_locator(months3)
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))


ax4 = df[df.tag_ident == 3896].plot(x = 'arbDate', y = 'Distance_km',
        color='magenta', ax=axes2[1])
L4=ax4.legend()
L4.get_texts()[0].set_text('Owl 3896')
ax4.set_xlabel('Date')
ax4.set_ylabel('Distance (km)')
months4 = mdates.MonthLocator()
ax4.xaxis.set_major_locator(months4)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))

plt.savefig('male_birds_dailydist.png', dpi=300, format='png')
plt.show()
