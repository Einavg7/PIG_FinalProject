
import os
import pandas as pd
import fnmatch
import re
import ogr,csv,sys
import matplotlib.pyplot as plt



def OpenFile(filePath):
    layer = iface.addVectorLayer(filePath,"shape","ogr")
  
    #ds=ogr.Open(filePath)
    #layer=ds.GetLayer()
    if not layer:
        print ('Could not open %s' % (filePath))
        return None
    else:      
        print ('Opened %s' % (filePath))
        return layer

def makeDataFrameForMap(layer):
    """
    Prepared pandas dataframe from layer, containing specified field in the dataframe
    Parameters
    ----------
    layer(string): layer to covert to dataframe
    Returns
    -------
    df (pandas dataframe)
    """
    df=pd.DataFrame(columns=["timestamp","tag_ident","Gender","utm_east","utm_north","long","lat","arbDate","arbHour"])
    for feature in layer.getFeatures():
        dict={}
        for column in df.columns:
            dict.update({column:feature[column]})
        df = df.append(dict, ignore_index=True)
    return df

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

pd.set_option('display.max_columns', None)
def CreateTagwiseDataFrame(inFolder,shapeFileName):
    """
    Creates dataframe from tagwise shapeFile and calculate season where ach point belongs to
    Parameters
    ----------
    inFolder(string): path to the folder containing all tagwise shapefiles
    shapeFileName(string):tagwise shapefile name
    Returns
    -------
    df(pandas dataframe): The pandas dataframe containing flying details for each bird
    """
     
    for file in os.listdir(inFolder):
        if file.endswith(shapeFileName):
            fullPath=os.path.join(inFolder,file)
            layer=OpenFile(fullPath)
            df=makeDataFrameForMap(layer)
            df['season'] = df.timestamp.map(seasonFromDate)
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

    imagePath = 'C:\\WWU\\movebank\\map'+tagID+'.png'
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
    
def FindLongestFlyingBirds(filePath,infolder):
    """
    Finds longest flying birds (2 each from Males and Females)
    Parameters
    ----------
    filePath(string): path to the daily distance csv to find maximum lengths 
    inFolder(string): path to the folder containing all tagwise shapefiles
    Returns
    -------
    None
    """
    daily_df = pd.read_csv(filePath)
    season = daily_df.groupby(['tag_ident','Gender','season'])['Distance'].agg('sum') 
    print(season)

    maskFemales = (daily_df['Gender']=='f')
    filterFemale = daily_df.loc[maskFemales]
    groupedFemales = filterFemale.groupby(['tag_ident','Gender']).agg({'Distance': ['sum']})
    groupedFemales.columns = ['sum']      
    flyingHeighestFemale =  groupedFemales.nlargest(2,'sum') 
    flyingHeighestFemale = flyingHeighestFemale.reset_index()  
    print(flyingHeighestFemale)    

    maskMales = (daily_df['Gender']=='m')
    filterMale = daily_df.loc[maskMales]
    groupedMales = filterMale.groupby(['tag_ident','Gender']).agg({'Distance': ['sum']})
    groupedMales.columns = ['sum']      
    flyingHeighestMale =  groupedMales.nlargest(2,'sum')   
    flyingHeighestMale = flyingHeighestMale.reset_index()
 
    print(flyingHeighestFemale['tag_ident'].values[0])
    print(flyingHeighestFemale['tag_ident'].values[1])
    print(flyingHeighestMale['tag_ident'].values[0])
    print(flyingHeighestMale['tag_ident'].values[1])

    tagID = str(flyingHeighestFemale['tag_ident'].values[0])
    shapeFileName = tagID + ".shp"
    gender = "Female"
    birdDataFrame=CreateTagwiseDataFrame(infolder,shapeFileName)
    PlotDataOnMap(birdDataFrame,tagID,gender)
        
    tagID = str(flyingHeighestFemale['tag_ident'].values[1])
    shapeFileName = tagID + ".shp"
    gender = "Female"
    birdDataFrame=CreateTagwiseDataFrame(infolder,shapeFileName)
    PlotDataOnMap(birdDataFrame,tagID,gender)
    
    tagID = str(flyingHeighestMale['tag_ident'].values[0])
    shapeFileName = tagID + ".shp"
    gender = "Male"
    birdDataFrame=CreateTagwiseDataFrame(infolder,shapeFileName)
    PlotDataOnMap(birdDataFrame,tagID,gender)
 
    tagID = str(flyingHeighestMale['tag_ident'].values[1])
    shapeFileName = tagID + ".shp"
    gender = "Male"
    birdDataFrame=CreateTagwiseDataFrame(infolder,shapeFileName)
    PlotDataOnMap(birdDataFrame,tagID,gender)
    
filePath = "C:\WWU\FinalProject\summaryCSVs\\dailyDistances.csv"
infolder="C:\\WWU\\movebank\\Outputs\\tagwise\\"
FindLongestFlyingBirds(filePath,infolder)
