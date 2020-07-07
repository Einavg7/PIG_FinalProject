import csv
from matplotlib import pyplot as plt
import pandas as pd

myfile = "C:\\Users\\einav\\Dropbox\\summer semester 2020\\Python in GIS\\Final Project\\dailyDistance.csv"

df = pd.read_csv(myfile)

## add km column
df['Distance_km'] = df.Distance / 1000
# print(df)



## plot by gender
ax = df.groupby('Gender')['Distance_km'].agg(lambda x: sum(x)).plot(kind='barh',title='Total distance traveled - Gender',
                                                                    color=["b", "r"])
ax.set_yticklabels(["Female", "Male"])
ax.set_xlabel('Distance in Kilometers')
plt.savefig('gender_dist.png', dpi=300, format='png')
plt.show()


## plot by season
df.groupby('season')['Distance_km'].agg(lambda x: sum(x)).plot(kind='pie',
                                                               title='Total distance traveled - Season')
plt.savefig('season_dist.png', dpi=300,format='png')
plt.show()

## plot by owl
df.groupby('tag_ident')['Distance_km'].agg(lambda x: sum(x)).plot(kind='bar',
                                                                  title='Total distance traveled by each Eagle Owl')
plt.savefig('owl_dist.png', dpi=300,format='png')
plt.show()


