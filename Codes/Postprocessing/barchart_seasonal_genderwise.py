"""
Creates grouped bar diagram  with season as groups and each male and female  birds average daily distance in kilometers
"""

## Create data
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



#Set project, input and output directory
projectDirectory="C:\\Users\\DELL\\Documents\\GitHub\\Project\\PIG_FinalProject"
inputCSV=os.path.join(projectDirectory, "Outputs/Processing/dailySummary.csv")
outputPath=os.path.join(projectDirectory, "Outputs/Postprocessing")
#Open csv file
dailyData=pd.read_csv(inputCSV)

#calculate distance in km
dailyData['kilometers']=dailyData['distance']/1000
#retain only non-zero distances
dailyData=dailyData[dailyData['kilometers']>0]
#get season and sort them in order of their occurence
seasons=list(dailyData['season'].unique())
sort_order={"Winter":0,"Spring":1,"Summer":2,"Autumn":3}
seasons.sort(key=lambda val:sort_order[val])
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

# Make the plot
plt.bar(r1, maleDistances, color='navy', width=barWidth, edgecolor='white', label='male owl')
plt.bar(r2, femaleDistances, color='orange', width=barWidth, edgecolor='white', label='female owl')

# Add xticks on the middle of the group bars
plt.xlabel('Season', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(femaleDistances))], seasons)
plt.title("Gender-wise Average Daily Distance Travelled by Season")
plt.ylabel("Average Daily Distance(km)")

# Create legend & Show graphic
plt.legend(loc=2)
plt.savefig(os.path.join(outputPath,"bar_gender_season"),dpi=600)
plt.show()

