import pandas as pd
import os
def distance(e1,n1,e2,n2):
    import math
    deltaE=e2-e1
    deltaN=n2-n1
    distance=math.sqrt((deltaE)**2+(deltaN)**2)
    return distance
    
def OpenFile(filePath):
    layer = iface.addVectorLayer(filePath,"shape","ogr")
   
    if not layer:
        print ('Could not open %s' % (filePath))
        return None
    else:      
        print ('Opened %s' % (filePath))
        return layer
    
def seasonFromDate(date):
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
    Prepared pandas dataframe from layer, containing specified field in the dataframe

    Parameters
    ----------
    layer(string): layer to covert to dataframe

    Returns
    -------
    df (pandas dataframe)

    """
    df=pd.DataFrame(columns=["timestamp","tag_ident","Gender","utm_east","utm_north","trueDate","Hour","arbDate","arbHour"])
    for feature in layer.getFeatures():
        dict={}
        for column in df.columns:
            dict.update({column:feature[column]})
        df = df.append(dict, ignore_index=True)
    return df

def getHourlyData(df,summaryDataFrame):
    """
    Generates hourly summary of distance from pandas dataframe and append record to summaryDataFrame

    Parameters
    ----------
    df(pandas dataframe): the dataframe to extract hourly distance from
    summaryDataFrame(pandas dataframe): The summary dataframe to which the record is to be appended

    Returns
    -------
    summaryDataFrame(pandas Dataframe):pandas dataframe with hourly distance from df appended to it.

    """
    dates=df['trueDate'].unique()
    #Get unique dates  and filter by them
    for date in dates:
        dateFiltered=df[df['trueDate']==date]
        #Get unique hours within dateFiltered
        hours=dateFiltered['Hour'].unique()
        for myhour in hours:
            finaldata=dateFiltered[dateFiltered['Hour']==myhour]
            finaldata=finaldata.sort_values(by="timestamp").reset_index()
            distList=[]
            for i in range(len(finaldata)):
                if i==0:
                    dist=0
                else:
                    dist=distance(finaldata.iloc[i-1]['utm_east'],finaldata.iloc[i-1]['utm_north'],finaldata.iloc[i]['utm_east'],finaldata.iloc[i]['utm_north'])
                distList.append(dist)
            finaldata['distance']=distList
            summaryDataFrame=summaryDataFrame.append({"tag_ident":finaldata['tag_ident'][0],"Gender":finaldata['Gender'][0],"trueDate":date,"Hour":myhour,'Distance':finaldata['distance'].sum()}, ignore_index=True)
    return summaryDataFrame
    
def createHourlyTable(inFolder):
    """
    Creates hourly distance table from all shapefiles inside a given folder. Also creates csv of it.

    Parameters
    ----------
    inFolder(string): path to the folder containing all shapefiles to be aggregated

    Returns
    -------
    hourlysummary(pandas dataframe): The pandas dataframe containing hourly distance for each day, each hour for each bird.

    """
    hourlysummary=pd.DataFrame(columns=["tag_ident","Gender","trueDate","Hour", "Distance"])
    for file in os.listdir(inFolder):
        if file.endswith(".shp"):
            fullPath=os.path.join(inFolder,file)
            layer=OpenFile(fullPath)
            df=makeDataFrame(layer)
            hourlysummary=getHourlyData(df,hourlysummary)
    #Enrich data with season information
    hourlysummary['season']=hourlysummary['trueDate'].apply(lambda thisDate:seasonFromDate(thisDate))
    #Extract date without year for plotting purpose
    hourlysummary['day-month']=hourlysummary['trueDate'].apply(lambda thisDate:thisDate[5:10])
    #Export daily summary to csv
    outcsv=os.path.join(inFolder,"hourly.csv")
    hourlysummary.to_csv(outcsv,index=False)
    return hourlysummary

def dailyDistance(inFolder):
    """
    Creates daily distance summary data for each shapefile containing birdwise data for each day.Also writes data in the folder containing data. The input data needs to be daily data

    Parameters
    ----------
    inFolder(String): The folder containing bird-wise data

    Returns
    -------
    dailySummary(pandas dataframe) :pandas dataframe for daily summarized distance for each bird per day

    """
    dailySummary=pd.DataFrame(columns=["tag_ident","Gender","arbDate", "Distance"])
    for file in os.listdir(inFolder):
        if file.endswith(".shp"):
            df=pd.DataFrame(columns=["timestamp","tag_ident","Gender","utm_east","utm_north","arbDate"])
            fullpath=os.path.join(inFolder,file)
            layer=OpenFile(fullpath)
            for feature in layer.getFeatures():
                dict={}
                for column in df.columns:
                    dict.update({column:feature[column]})
                df = df.append(dict, ignore_index=True)
            df=df.sort_values(by="timestamp").reset_index()
            distList=[]
            for i in range(len(df)):
                if i==0:
                    dist=0
                else:
                    dist=distance(df.iloc[i-1]['utm_east'],df.iloc[i-1]['utm_north'],df.iloc[i]['utm_east'],df.iloc[i]['utm_north'])
                distList.append(dist)
            df['distance']=distList
            dailySummary=dailySummary.append({"tag_ident":df['tag_ident'][0],"Gender":df['Gender'][0],"arbDate":df['arbDate'][0],'Distance':df['distance'].sum()}, ignore_index=True)
            #Enrich data with season information
            dailySummary['season']=dailySummary['arbDate'].apply(lambda thisDate:seasonFromDate(thisDate))
            #Extract date without year for plotting purpose
            dailySummary['day-month']=dailySummary['arbDate'].apply(lambda thisDate:thisDate[5:10])
            #Export daily summary to csv
            filename="dailySummary.csv"
            dailySummary.to_csv(os.path.join(inFolder,filename),index=False)
    return dailySummary
            


#Main program          
#Iterate over the daily distance data and compute daily distance
infolder="E:\\Outputs\\daily"
#Create daily summary table
summary=dailyDistance(infolder)
#Create hourly distance table
hourlydistance=createHourlyTable(infolder)