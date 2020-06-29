import os
from qgis.core import *
import qgis.utils
import ogr
import csv
from datetime import datetime,timedelta
import qgis.utils
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

#Open the movebank point shapefile
def OpenFile(filePath):
    layer = iface.addVectorLayer(filePath,"shape","ogr")
   
    if not layer:
        print ('Could not open %s' % (filePath))
        return None
    else:      
        print ('Opened %s' % (filePath))
        return layer
    
#Remove unnecessary fields 
def RemoveFields(layer,fieldNamesToRemove = ['battery_vo','fix_batter','horizontal', 'key_bin_ch','speed_accu','status','temperatur',
                                'type_of_fi', 'speed','heading','height','outlier_ma','visible','sensor_typ','individual',
                                'ind_ident','study_name','date','time']):
    """
    Removes the unnecessary fields before processing

    Parameters
    ----------
    layer (QgsVectorLayer): Layer to remove fields from 
        DESCRIPTION.
    fieldNamesToRemove(list) : List of fields to be removed.
        DESCRIPTION. The default is ['battery_vo','fix_batter','horizontal', 'key_bin_ch','speed_accu','status','temperatur',                                'type_of_fi', 'speed','heading','height','outlier_ma','visible','sensor_typ','individual',                                'ind_ident','study_name'].

    Returns
    -------
    None.

    """
    caps = layer.dataProvider().capabilities()
    if caps & QgsVectorDataProvider.DeleteAttributes: 
        fields = layer.dataProvider().fields()
        for field in fields:
           if field.name() in fieldNamesToRemove:
               layer.dataProvider().deleteAttributes([layer.fields().indexFromName(field.name())])
               layer.updateFields()
     
def createDictionaryFromCSV(metadata,keyField,valueField):
    """
    Creates dictionary from csv to generate dictionary that extracts gender by animal tag do relate it to shapefile

    Parameters
    ----------
    metadata(String) :Path to metadata file
    keyField (String): Name of field in csv containing tag id
    valueField(String): Name of field in csv containing gender of animal

    Returns
    -------
    gender(Dictionary): Pair of all  tag ids with their corresponding gender
    """
    gender={}
    with open(metadata, newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:
             if row[valueField]!="":
                 gender.update({row[keyField]:row[valueField]})
    return gender  

def getUniqueValues(layer,field):
    """  

    Parameters
    ----------
    layer (vector layer): The layer to compute on
    field (String):Name of field to calculate unique values from

    Returns
    -------
    List

    """
    
    values=[]
    for feature in layer.getFeatures():
        if feature[field] not in values:
            values.append(feature[field])
    values.sort()
    return values
     
def getUniqueValuesFromList(inlist):
    values=[]
    for feature in inlist:
        if feature not in values:
            values.append(feature)
    return values
    
#Main Program
#Add vector data   
fileDir = "E:\\Masters\\Notes\\Sem2\\Python\\Project\\Data\\demopoints.shp"
metadataDir="E:\\Masters\\Notes\\Sem2\\Python\\Project\\Data\\metadata.csv"
layer = OpenFile(fileDir)
#Remove Fields
RemoveFields(layer)
#Create dictionary for genders    
gender=createDictionaryFromCSV(metadataDir,'tag-id','animal-sex')

#Add fields
#Remove existing fields first
RemoveFields(layer,['Gender','trueDate','Hour','arbDate','arbHour'])
#add fields
caps=layer.dataProvider().capabilities()
if caps&QgsVectorDataProvider.AddAttributes:
    layer.dataProvider().addAttributes([QgsField('Gender',QVariant.String)])
    layer.dataProvider().addAttributes([QgsField('trueDate',QVariant.Date)])
    layer.dataProvider().addAttributes([QgsField('Hour',QVariant.Int)])
    layer.dataProvider().addAttributes([QgsField('arbDate',QVariant.String)])
    layer.dataProvider().addAttributes([QgsField('arbHour',QVariant.Int)])

#Read tag and incorporate.Shift the time by 19 hours, as we are using 19:00 hours as the start of origin

with edit(layer):
    for feature in layer.getFeatures():
        feature.setAttribute(feature.fields().indexFromName('Gender'), gender.get(feature['tag_ident']))
        regularTimeStamp=datetime.strptime(feature['timestamp'], '%Y-%m-%d %H:%M:%S')
        adjustedTimeStamp=regularTimeStamp-timedelta(hours=19)
        feature.setAttribute(layer.fields().indexFromName('arbDate'),adjustedTimeStamp.strftime('%Y-%m-%d'))
        feature.setAttribute(layer.fields().indexFromName('trueDate'),regularTimeStamp.strftime('%Y-%m-%d'))
        feature.setAttribute(layer.fields().indexFromName('Hour'),regularTimeStamp.hour)
        feature.setAttribute(layer.fields().indexFromName('arbHour'),adjustedTimeStamp.hour)
        layer.updateFeature(feature)
layer.updateFields()

#Get unique value for tags
if caps & QgsVectorDataProvider.ChangeAttributeValues:
    tags=getUniqueValues(layer,'tag_ident')
    for tag in tags:
        selected=processing.run('qgis:selectbyattribute',{'INPUT':layer,'FIELD':'tag_ident','OPERATOR':0,'VALUE':tag,'METHOD':0})
        selection = layer.selectedFeatures()
        dates=list()
        for features in selection:
            dates.append(features['arbDate'])
        #Get Unique Values for arbitrary Date
        datelist=getUniqueValuesFromList(dates)
        for mydate in datelist:
            print(tag,mydate)
            expres=' \"tag_ident\" = \'{v01}\' AND \"arbDate\" = \'{v02}\' '.format(v01=tag,v02=mydate)
            selecteds=processing.run('qgis:selectbyexpression',{ 'EXPRESSION' : expres, 'INPUT' : 'E:/Masters/Notes/Sem2/Python/Project/Data/demopoints.shp', 'METHOD' : 0 })
            #saved=processing.run('native:saveselectedfeatures',{'INPUT':layer,'OUTPUT':'memory'})