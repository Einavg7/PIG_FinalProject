import os
import qgis
from qgis.core import (
    QgsVectorLayer
)
import fnmatch
import re
import ogr
import csv
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
import matplotlib.dates as mdates
from math import floor

def OpenFile(filePath):
    """
    Opens a shapefile in QGIS

    Parameters
    ----------
    filePath :STRING
        Path to the shapefile to open

    Returns
    -------
    layer : QgsVectorLayer

    """
    layer = iface.addVectorLayer(filePath,"shape","ogr")
    if not layer:
        print ('Could not open %s' % (filePath))
        return None
    else:      
        print ('Opened %s' % (filePath))
        return layer
def seasonFromDate(date):
    """
    Returns the value of season from month and day data of the timestamp

    Parameters
    ----------
    date : String
        Timestamp or date string in format of YYYY-MM-DD or followed by timestamp

    Returns
    -------
    season : STRING
        Season corresponding to the date

    """
    dayMonth=date[5:10]
    if dayMonth<"03-21"or dayMonth>"12-21":
        season="Winter"
    elif dayMonth<"06-22":
        season="Spring"
    elif dayMonth<"09-21":
        season="Summer"
    else:
        season="Autumn"
    return season

def makeDataFrame(layer):
    """
    Prepare pandas dataframe from layer, containing specified field in the dataframe

    Parameters
    ----------
    layer(string): layer to covert to dataframe

    Returns
    -------
    df (pandas dataframe)

    """
    columns=[]
    caps = layer.dataProvider().capabilities()
    if caps & QgsVectorDataProvider.DeleteAttributes: 
        fields = layer.dataProvider().fields()
        for field in fields:
            columns.append(field.name())
    df=pd.DataFrame(columns=columns)
    for feature in layer.getFeatures():
        dict={}
        for column in df.columns:
            dict.update({column:feature[column]})
        df = df.append(dict, ignore_index=True)
    df['season']=df['timestamp'].apply(lambda x:seasonFromDate(x))
    return df


def PlotDataOnMap(birdDataFrame,tagID,gender):
    """
    Plot movements of birds during seasons
    Parameters
    ----------
    birdDataFrame(string): dataframe contains bird movement
    tagID(string): Tag ID of the bird
    gender(string):Gender of the bird
    Returns
    -------
    None
    """
    df = birdDataFrame
    BBox = (df.long.min(),df.long.max(),df.lat.min(), df.lat.max())
    print(BBox)

    maskSpring = df['season']== 'Spring'
    filterSpring = df.loc[maskSpring]

    maskSummer = df['season']== 'Summer'
    filterSummer = df.loc[maskSummer]

    maskAutumn = df['season']== 'Autumn'
    filterAutumn = df.loc[maskAutumn]

    maskWinter = df['season']== 'Winter'
    filterWinter = df.loc[maskWinter]

    imagePath = 'C:\\Users\\DELL\\Desktop\\map\\map\\map'+tagID+'.png'
    print(imagePath)

    ruh_m = plt.imread(imagePath)

    fig, ax = plt.subplots(1,1)
    ax.scatter(filterSpring.long, filterSpring.lat, zorder=1, alpha= 0.4, c='g', s=10, label='Spring')
    ax.scatter(filterSummer.long, filterSummer.lat, zorder=1, alpha= 0.4, c='y', s=10, label='Summer')
    ax.scatter(filterAutumn.long, filterAutumn.lat, zorder=1, alpha= 0.4, c='r', s=10, label='Autumn')
    ax.scatter(filterWinter.long, filterWinter.lat, zorder=1, alpha= 0.4, c='b', s=10, label='Winter')
    ax.legend()
    ax.set_title(gender+' Bird -'+tagID)
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.show()
#Main program
#Get the tags from the folder
shpFolder="C:\\Users\\DELL\\Documents\\GitHub\\Project\\PIG_FinalProject\\Outputs\\Preprocessing"
tagslist=['1753,3893']
gender=['female','male']
for i in range(len(tagslist)):
    filepath=os.path.join(shpFolder,"pointstag_ident"+tagslist[i]+".shp")
    layer=OpenFile(filepath)
    df=makeDataFrame(layer)
    PlotDataOnMap(df, tagslist[i], gender[i])