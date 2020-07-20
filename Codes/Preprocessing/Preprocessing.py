"""
Performs following preprocessing activity from bird movement data
-Add gender information from metadata file in csv
-Remove unnecessary fields
-Convert date by shifting 17 hours foreward for daily purpose
-Split data by tag identity to generate bird-wise data
"""
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

def preprocess(inFolder,metadataDir):
    """
    Performs preprocesing such as manipulating time fields, deleting unncessary field, avoiding repeatedly created fields on multiple execution.

    Parameters
    ----------
    layer(Vector) :The layer to be preprocessed

    Returns
    -------
    None.

    """
    for file in os.listdir(inFolder):
        if file.endswith(".shp"):
            fullPath=os.path.join(inFolder,file)
            layer=OpenFile(fullPath)
            #Remove Fields
            RemoveFields(layer)
            #Create dictionary for genders    
            gender=createDictionaryFromCSV(metadataDir,'tag-id','animal-sex')
            RemoveFields(layer,['Gender','trueDate','Hour','arbDate','arbHour'])
            #add fields for gender and modified time for daily analysis
            caps=layer.dataProvider().capabilities()
            if caps&QgsVectorDataProvider.AddAttributes:
                layer.dataProvider().addAttributes([QgsField('Gender',QVariant.String)])
                layer.dataProvider().addAttributes([QgsField('mod_time',QVariant.String)])
            
            #Read tag and incorporate.Shift the time by 19 hours, as we are using 19:00 hours as the start of origin
            
            with edit(layer):
                for feature in layer.getFeatures():
                    feature.setAttribute(feature.fields().indexFromName('Gender'), gender.get(feature['tag_ident']))
                    regularTimeStamp=datetime.strptime(feature['timestamp'], '%Y-%m-%d %H:%M:%S')
                    adjustedTimeStamp=regularTimeStamp-timedelta(hours=17)
                    feature.setAttribute(layer.fields().indexFromName('mod_time'),adjustedTimeStamp.strftime( '%Y-%m-%d %H:%M:%S'))
                    layer.updateFeature(feature)
            layer.updateFields()

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
    """
    Returns the unique values from the list containing no. of items""

    Parameters
    ----------
    inlist (list): List containing  items to get unique values from

    Returns
    -------
    values(list): list containing unique values sorted in order

    """
    values=[]
    for feature in inlist:
        if feature not in values:
            values.append(feature)
    return values
    
def splitData(inFolder,outFolder,splitField):
    """
        Allows the user to split data based on a field/atttibute

    Parameters
    ----------
    inFolder(String): the folder containing the shapefiles to be splitted
    outFolder(String): the folder to store splitted contents
    splitField(String): field to split data based on

    Returns
    -------
    None.

    """
    #Get unique value for tags
    for file in os.listdir(inFolder):
        if file.endswith(".shp"):
            fullPath=os.path.join(inFolder,file)
            layer=OpenFile(fullPath)
            caps = layer.dataProvider().capabilities()
            if caps & QgsVectorDataProvider.ChangeAttributeValues:
                tags=getUniqueValues(layer,splitField)
                for tag in tags:
                    outputfilename=file.split(".")[0]+splitField+str(tag)+".shp"
                    outputshp=os.path.join(outFolder,outputfilename)
                    #build expression for selecting features
                    expres=' \"{field}\" = \'{tag}\' '.format(field=splitField,tag=tag)
                    #select by expression
                    processing.run('qgis:selectbyexpression',{ 'EXPRESSION' : expres, 'INPUT' : layer, 'METHOD' : 0 })
                    #save selected features as shp
                    processing.run('native:saveselectedfeatures',{'INPUT':layer,'OUTPUT':outputshp})
                    print("{output} file written to {folder}".format(output=outputfilename,folder=outFolder))

##Main Program
#fileDir = "E:\\Masters\\Notes\\Sem2\\Python\\Project\\Data\\demopoints.shp"
#Set project directory
projectDirectory="C:\\Users\\DELL\\Documents\\GitHub\\Project\\PIG_FinalProject"
print (projectDirectory)
metadataDir=os.path.join(projectDirectory,"DataSource/metadata.csv")
print(metadataDir)
#Split whole dataset by tag
sourceFolder=os.path.join(projectDirectory,"DataSource")
tagwiseFolder=os.path.join(projectDirectory,"Outputs/Preprocessing")
splitData(sourceFolder,tagwiseFolder,"tag_ident")
#Preprocess data
#preprocess(tagwiseFolder,metadataDir)