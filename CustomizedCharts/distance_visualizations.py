import csv
from matplotlib import pyplot as plt
import pandas as pd

myfile = "C:\\Users\\einav\\Dropbox\\summer semester 2020\\Python in GIS\\Final Project\\dailyDistance.csv"

df = pd.read_csv(myfile)

## add km column
df['Distance_km'] = df.Distance / 1000
# print(df)



## plot by gender
ax = df.groupby('Gender')['Distance_km'].mean().plot(kind='barh',title='Average distance traveled - Gender',
                                                                    color=["b", "r"])
## male: 10.2, female: 7.139
ax.set_yticklabels(["Female", "Male"])
ax.set_xlabel('Distance in Kilometers')
plt.savefig('gender_dist.png', dpi=300, format='png')
plt.show()


## plot by season
ax1 = df.groupby('season')['Distance_km'].mean().plot(kind='bar', title='Average distance traveled - Season',
                                               color=['orange', 'green', 'yellow', 'cyan'] )
ax1.set_ylabel('Distance in Kilometers')
## summer : 8.689, autumn : 8.519, spring : 7.154, winter : 5.289
plt.savefig('season_dist.png', dpi=300,format='png')
plt.xticks(rotation=45)
plt.show()

## plot by owl
##df.groupby('tag_ident')['Distance_km'].agg(lambda x: sum(x)).plot(kind='bar',
##                                                                  title='Total distance traveled by each Eagle Owl')
##plt.savefig('owl_dist.png', dpi=300,format='png')
##plt.show()

