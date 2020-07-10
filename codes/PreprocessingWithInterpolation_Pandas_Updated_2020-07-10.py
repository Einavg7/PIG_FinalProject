"""" Processing for eagle owl data in arcgis pro
Performs the following:
    - Interpolate data hourly at hour values using existing observations
    -Compute daily and hourly distance for each bird and write it as a single csv"""
#Import packages    
import math
import pandas as pd
import os
from datetime import datetime, timedelta

def distance(e1,n1,e2,n2):
    """
    Computed planimetric distance from given Easting and northing of two points

    Parameters
    ----------
    e1 : NUMERIC
        Easting of first point
    n1 : NUMERIC
        Northing of first point.
    e2 : NUMERIC
        Easting of Second Point
    n2 : NUMERIC
        Northing of second point.

    Returns
    -------
    distance : Numeric
        Computed Planimetric Distance between two points

    """
    import math
    deltaE=e2-e1
    deltaN=n2-n1
    distance=math.sqrt((deltaE)**2+(deltaN)**2)
    return distance
    
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
    

def interpolate(df,timestampField,fieldstoInterpolate):
    """
    Interpolates the position or any value between two timestamps, if they are on different hour.

    Parameters
    ----------
    df : PANDAS DATAFRAME
        DESCRIPTION.
    timestampField : STRING
        The field containing timestamp to be used for interpolation
    fieldstoInterpolate : List of fields
        A list containing field names to be interpolated.

    Returns
    -------
    df : PANDAS DATAFRAME
        Dataframe with interpolated values

    """
    #get datetime from timestamp string
    df['datetime']=df[timestampField].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    #sort by timestamp
    df=df.sort_values(by=timestampField,ascending=True).reset_index()
    #get the index for change in hour by iterating till the second last eleement of sorted timestamp
    for i in range(len(df)-1):
        if df.iloc[i]['datetime'].hour != df.iloc[i+1]['datetime'].hour:
            #get the difference in their hour value and adjust for change of day
            differencehour=df.iloc[i+1]['datetime'].hour -df.iloc[i]['datetime'].hour
            if differencehour<0:
                differencehour=24+differencehour
            if differencehour<=2:
                #Initiate first hour to start interpolation from
                initialtime=df.iloc[i]['datetime']-timedelta(minutes=df.iloc[i]['datetime'].minute,seconds=df.iloc[i]['datetime'].second)
                #interpolate value for each full hour value between them
                for n in range(1,differencehour+1):
                    interpolateTime=initialtime+timedelta(hours=n)
                    #initiate dictionary to write to interpolated value
                    dictToWrite={timestampField:interpolateTime.strftime('%Y-%m-%d %H:%M:%S'),"tag_ident":df.iloc[i]['tag_ident'],"Gender":df.iloc[i]['Gender'],"datetime":interpolateTime}
                    #interpolate values
                    referenceInterval=df.iloc[i+1]['datetime']-df.iloc[i]['datetime']
                    interpolateInterval=interpolateTime -df.iloc[i]['datetime']
                    #iterate through whole list of fields to be interpolated
                    for fieldtoInterpolate in fieldstoInterpolate:
                        interpolatedValue=(interpolateInterval/referenceInterval)*(df.iloc[i+1][fieldtoInterpolate]-df.iloc[i][fieldtoInterpolate])+df.iloc[i][fieldtoInterpolate]
                        dictToWrite.update({fieldtoInterpolate:interpolatedValue})
                    df=df.append(dictToWrite, ignore_index=True)
    #sort data with interpolated value and reset index
    df=df.sort_values(by="timestamp").reset_index(drop=True)
    return df

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
    df=pd.DataFrame(columns=["timestamp","tag_ident","Gender","utm_east","utm_north","trueDate","Hour"])
    for feature in layer.getFeatures():
        dict={}
        for column in df.columns:
            dict.update({column:feature[column]})
        df = df.append(dict, ignore_index=True)
    return df

def getHourlyDistance(df,summaryDataFrame):
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
    dates=(df['datetime'].apply(lambda x:x.date())).unique()
    #Get unique dates  and filter by them
    for date in dates:
        startTimestamp=datetime.combine(date,datetime.min.time())
        endTimestamp=startTimestamp+timedelta(hours=24)
        #Mask data to the selected day
        dailyMask=(df['datetime']>=startTimestamp) & (df['datetime']<=endTimestamp)
        dailyData=df[dailyMask]
        #Get unique hour values from the selected dayand filterdata for that particular hour
        selectedHours=dailyData['datetime'].apply(lambda x:math.floor((x-startTimestamp).total_seconds()/3600.0)).unique()
        selectedHours.sort()
        hours=selectedHours[:-1]
        #Select data for each hour
        for hour in hours:
            startHour=startTimestamp+timedelta(hours=hour.item())
            endHour=startHour+timedelta(hours=1)
            hourlyMask=(dailyData['datetime']>=startHour) & (df['datetime']<=endHour)
            hourlyData=dailyData.loc[hourlyMask]
            #sort data by time and compute distance
            finaldata=hourlyData.sort_values(by="timestamp").reset_index(drop=True)
            distList=[]
            for i in range(len(finaldata)):
                if i==0:
                    dist=0
                else:
                    dist=distance(finaldata.iloc[i-1]['utm_east'],finaldata.iloc[i-1]['utm_north'],finaldata.iloc[i]['utm_east'],finaldata.iloc[i]['utm_north'])
                distList.append(dist)
            finaldata['distance']=distList
            summaryDataFrame=summaryDataFrame.append({"tag_ident":finaldata.iloc[0]['tag_ident'],"Gender":finaldata.iloc[0]['Gender'],"Date":date,"Hour":hour,'Distance':finaldata['distance'].sum(),"Season":seasonFromDate(finaldata.iloc[0]['timestamp']),"month-day":finaldata.iloc[0]['timestamp'][5:10]}, ignore_index=True)
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
    hourlysummary=pd.DataFrame(columns=["tag_ident","Gender","Date","Hour", "Distance","Season","month-day"])
    for file in os.listdir(inFolder):
        if file.endswith(".shp"):
            fullPath=os.path.join(inFolder,file)
            layer=OpenFile(fullPath)
            df=makeDataFrame(layer)
            interpolatedData=interpolate(df,'timestamp',['utm_east','utm_north'])
            hourlysummary=getHourlyDistance(interpolatedData,hourlysummary)
    #Export daily summary to csv
    outcsv=os.path.join(inFolder,"hourly.csv")
    hourlysummary.to_csv(outcsv,index=False)
    print ("Summary file written to {path}".format(path=outcsv))
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
infolder="E:\\Outputs\\trial"
#Create daily summary table
#summary=dailyDistance(infolder)
#Create hourly distance table
hourlydistance=createHourlyTable(infolder)
dailydistance=dailyDistance(infolder)

