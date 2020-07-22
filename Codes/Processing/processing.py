import math
import pandas as pd
import os
from datetime import datetime, timedelta
import csv

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
    return df


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
    Interpolates the position or any value between two timestamps, if they are on different hour.The input data should be for a single bird.

    Parameters
    ----------
    df(pandas dataframe): Original dataframe to be interpolated
    timestampField(string) :The field containing timestamp to be used for interpolation
    fieldstoInterpolate (list): List of string containing field names to be interpolated.

    Returns
    -------
    df (pandads dataframe):Dataframe with interpolated values

    """
    #get datetime from timestamp string
    df['datetime']=df[timestampField].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    #sort by timestamp
    df=df.sort_values(by=timestampField,ascending=True).reset_index()
    #get the index for change in hour by iterating till the second last eleement of sorted timestamp
    for i in range(len(df)-1):
        thisTime, nextTime=df.iloc[i]['datetime'],df.iloc[i+1]['datetime']
        if thisTime.hour != nextTime.hour:
            #get the difference in their hour value and adjust for change of day
            differencehour=nextTime.hour -thisTime.hour
            #address for change of hour from 23 to 0 at midnight
            if differencehour<0:
                differencehour=24+differencehour
            #interpolate only for two successive hours
            if differencehour<=2:
                #Initiate first hour to start interpolation from
                initialtime=thisTime-timedelta(minutes=thisTime.minute,seconds=thisTime.second)
                #interpolate value for each full hour value between them
                for n in range(1,differencehour+1):
                    interpolateTime=initialtime+timedelta(hours=n)
                    #initiate dictionary to write to interpolated value
                    dictToWrite={timestampField:interpolateTime.strftime('%Y-%m-%d %H:%M:%S'),"tag_ident":df.iloc[i]['tag_ident'],"Gender":df.iloc[i]['Gender'],"datetime":interpolateTime}
                    #interpolate values
                    referenceInterval=nextTime-thisTime
                    interpolateInterval=interpolateTime -thisTime
                    #iterate through whole list of fields to be interpolated
                    for fieldtoInterpolate in fieldstoInterpolate:
                        interpolatedValue=(interpolateInterval/referenceInterval)*(df.iloc[i+1][fieldtoInterpolate]-df.iloc[i][fieldtoInterpolate])+df.iloc[i][fieldtoInterpolate]
                        #Update dictionary with interpolated value
                        dictToWrite.update({fieldtoInterpolate:interpolatedValue})
                    #Appedn data to the original dataframe
                    df=df.append(dictToWrite, ignore_index=True)
    #sort data with interpolated value and reset index
    df=df.sort_values(by="timestamp").reset_index(drop=True)
    return df

def dailyDistance(df,timestampField,outFields):
    """
    Generates a summary pandas dataframe with with 

    Parameters
    ----------
    df(pandas dataframe): Dataframe containing records from a single bird
    timestampField(string): Name of field containing timestamp data to be extract day from. For daily distance, use shifted timestamp instead of original timestamp
    outFields(list of strings): list containing name of fields to be included in output summary

    Returns
    -------
    dailysummary (pandas dataframe):the output pandas dataframe containing daily summary
    """
    #Create a blank dataframe to store daily summary
    dailysummary=pd.DataFrame(columns=outFields)
    #Get datetime from string field of timestamp
    df['datetime']=df[timestampField].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    df['date']=df[timestampField].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S').date())
    #Extract unique dates
    dates=df['date'].unique()
    #loop through each day to get bound of day
    for date in dates:
        startTimestamp=datetime.combine(date,datetime.min.time())
        endTimestamp=startTimestamp+timedelta(hours=24)
        #Mask data to the selected day
        dailyMask=(df['datetime']>=startTimestamp) & (df['datetime']<=endTimestamp)
        dailyData=df[dailyMask]
        dailyData.sort_values(by=timestampField)
        #Only select data for tracking of at least 4 hours
        lastTime=dailyData.iloc[-1]['datetime']
        firstTime=dailyData.iloc[0]['datetime']
        interval=(lastTime-firstTime).total_seconds()
        if interval>=4*3600:
            #Initiate the distance for that day and cumulate till end
            dailyDist=0
            #Append values from existing field whenever available
            dict={}
            for field in outFields:
                if field in df.columns:
                    dict.update({field:dailyData.iloc[0][field]})
            for i in range(len(dailyData)):
                if i==0:
                    dist=0
                else:
                    dist=distance(dailyData.iloc[i-1]['utm_east'], dailyData.iloc[i-1]['utm_north'], dailyData.iloc[i]['utm_east'], dailyData.iloc[i]['utm_north'])
                dailyDist+=dist
            #Update dictionary with date, distance and season information
            dict.update({'date':date.strftime('%Y-%m-%d'),'distance':dailyDist,'season':seasonFromDate(date.strftime('%Y-%m-%d')),'day-month':date.strftime('%Y-%m-%d')[5:10]})
            #append dictionary to dataframe
            dailysummary=dailysummary.append(dict, ignore_index=True)
    return dailysummary

def hourlyDistance(df,timestampField,outFields):
    """
    Generates a summary pandas dataframe with with 

    Parameters
    ----------
    df(pandas dataframe): Dataframe containing records from a single bird
    timestampField(string): Name of field containing timestamp data to be extract day from. For daily distance, use shifted timestamp instead of original timestamp
    outFields(list of strings): list containing name of fields to be included in output summary

    Returns
    -------
    dailysummary (pandas dataframe):the output pandas dataframe containing daily summary
    """
    #Create a blank dataframe to store daily summary
    hourlysummary=pd.DataFrame(columns=outFields)
    #Get datetime from string field of timestamp
    df['datetime']=df[timestampField].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    df['date']=df[timestampField].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S').date())
    #Extract unique dates
    dates=df['date'].unique()
    #loop through each day to get bound of day
    for date in dates:
        startTimestamp=datetime.combine(date,datetime.min.time())
        endTimestamp=startTimestamp+timedelta(hours=24)
        #Mask data to the selected day
        dailyMask=(df['datetime']>=startTimestamp) & (df['datetime']<=endTimestamp)
        dailyData=df[dailyMask]
        #Get unique hour values from the selected dayand filterdata for that particular hour
        selectedHours=dailyData['datetime'].apply(lambda x:math.floor((x-startTimestamp).total_seconds()/3600.0)).unique()
        selectedHours.sort()
        #eliminate last hour (24) for not belonging to the day
        hours=selectedHours[:-1]
        #Select data for each hour
        for hour in hours:
            startHour=startTimestamp+timedelta(hours=hour.item())
            endHour=startHour+timedelta(hours=1)
            hourlyMask=(dailyData['datetime']>=startHour) & (df['datetime']<=endHour)
            hourlyData=dailyData.loc[hourlyMask]
            #sort data by time and compute distance
            finaldata=hourlyData.sort_values(by=timestampField).reset_index(drop=True)
            #Get the time difference between first and last record of that hour
            lastTime=finaldata.iloc[-1]['datetime']
            firstTime=finaldata.iloc[0]['datetime']
            interval=(lastTime-firstTime).total_seconds()
            if interval>=40*60:
                #Initiate the distance for that day and cumulate till end
                hourlyDist=0
                #Append values from existing field whenever available
                dict={}
                for field in outFields:
                    if field in df.columns:
                        dict.update({field:finaldata.iloc[0][field]})
                for i in range(len(finaldata)):
                    if i==0:
                        dist=0
                    else:
                        dist=distance(finaldata.iloc[i-1]['utm_east'], finaldata.iloc[i-1]['utm_north'], finaldata.iloc[i]['utm_east'], finaldata.iloc[i]['utm_north'])
                    hourlyDist+=dist
                #print(date,hour,hourlyDist)
                #Update dictionary with date, distance and season information
                dict.update({'date':date.strftime('%Y-%m-%d'),'distance':hourlyDist,'hour':hour,'season':seasonFromDate(date.strftime('%Y-%m-%d')),'day-month':date.strftime('%Y-%m-%d')[5:10]})
                #append dictionary to dataframe
                hourlysummary=hourlysummary.append(dict, ignore_index=True)
    return hourlysummary

def GetHourlySummary(inFolder,timestampField,hourlySummaryFields):
    """
    Iterates over the shapefiles in specified folder and returns hourly summary for distances

    Parameters
    ----------
    inFolder(string): Path to the folder containing shapefiles to be summerized
    timestampField(string): name of field containing timestamp to be used 
    hourlySummaryFields(list of strings): the  list of fields to be included in hourly summary

    Returns
    -------
    hourlysummaryTable(pandas dataframe): dataframe with distance summarized on hourly basis

    """
    hourlysummaryCSV=os.path.join(inFolder,"../Processing/hourlySummary.csv")
    with open(hourlysummaryCSV,'a') as file:
        writer=csv.writer(file)
        writer.writerow(hourlySummaryFields)
    for file in os.listdir(inFolder):
        if file.endswith(".shp"):
            fullPath=os.path.join(inFolder,file)
            layer=OpenFile(fullPath)
            df=makeDataFrame(layer)
            interpolatedData=interpolate(df,timestampField,['utm_east',"utm_north","lat","long"])
            hourlyDist=hourlyDistance(interpolatedData,timestampField,hourlySummaryFields)
            hourlyDist.to_csv(hourlysummaryCSV,mode='a', index=False, header=False) 
            
def GetDailySummary(inFolder,timestampField,dailySummaryFields):
    """
    Gets the daily summary from birdwise data stored in a folder

    Parameters
    ----------
    inFolder(string): Path to the folder containing the shapefiles
    timestampField(string): field name containing timestamp to be used for daily summary. User converted data for daily summary
    dailySummaryFields(array of string): fields to be included in daily summary 

    Returns
    -------
    dailysummaryTable : TYPE
        DESCRIPTION.

    """
    dailysummaryCSV=os.path.join(inFolder,"../Processing/dailySummary.csv")
    with open(dailysummaryCSV,'a') as file:
        writer=csv.writer(file)
        writer.writerow(dailySummaryFields)
    for file in os.listdir(inFolder):
        if file.endswith(".shp"):
            fullPath=os.path.join(inFolder,file)
            layer=OpenFile(fullPath)
            df=makeDataFrame(layer)
            dailyDist=dailyDistance(df,timestampField,dailySummaryFields)
            dailyDist.to_csv(dailysummaryCSV,mode='a', index=False, header=False)

#Main Application
#Set project, input and output directory
projectDirectory="C:\\Users\\DELL\\Documents\\GitHub\\Project\\PIG_FinalProject"
tagwiseFolder=os.path.join(projectDirectory,"Outputs/Preprocessing")
csvDirectory=os.path.join(projectDirectory,"Outputs/Processing")

#Choose fields to include in daily and hourly summary
dailySummaryFields=["tag_ident","Gender","date","season","day-month","distance"]
hourlySummaryFields=["tag_ident","Gender","date","hour","season","day-month","distance"]

hourly=GetHourlySummary(tagwiseFolder, "timestamp", hourlySummaryFields)
daily=GetDailySummary(tagwiseFolder,'mod_time',dailySummaryFields)


