import ogr
import os
import csv
from datetime import datetime,timedelta
from qgis.core import *
import qgis.utils
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

#############
# Read the shapefile
data_dir = os.path.join("E:\\","Masters","Notes","Sem2","Python","Project","movebank","eagle_owl")
in_path = os.path.join(data_dir,"demodata2.shp")
metadata=os.path.join(data_dir,"metadata.csv")
#
#Create dictionary for genders
gender={}
with open(metadata, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['animal-sex']!="":
            gender.update({row['tag-id']:row['animal-sex']})

inShape=iface.addVectorLayer(in_path,'demopoints','ogr')

#Find existing fields starting with Gender
deleteFieldsIndex=[]
for field in inShape.fields():
    fieldName=field.name()
    if fieldName.startswith('Gender') or fieldName.startswith('Adj') :
        fieldIndex=inShape.fields().indexFromName(fieldName)
        deleteFieldsIndex.append(fieldIndex)
#Read capabilities of shapefile
caps=inShape.dataProvider().capabilities()

if caps&QgsVectorDataProvider.DeleteAttributes:
    inShape.dataProvider().deleteAttributes(deleteFieldsIndex)
    
#Update Attributes with gender
if caps&QgsVectorDataProvider.AddAttributes:
    inShape.dataProvider().addAttributes([QgsField('Gender',QVariant.String)])
    inShape.dataProvider().addAttributes([QgsField('Adj_Date',QVariant.Date)])
    inShape.dataProvider().addAttributes([QgsField('Adj_Hour',QVariant.Int)])
# Get index of field to insert string
insertIndex=inShape.fields().indexFromName('Gender')

#Read tag and incorporate.Shift the time by 19 hours, as we are using 19:00 hours as the start of origin
with edit(inShape):
    for feature in inShape.getFeatures():
        feature.setAttribute(feature.fields().indexFromName('Gender'), gender.get(feature['tag_ident']))
        regularTimeStamp=datetime.strptime(feature['timestamp'], '%Y-%m-%d %H:%M:%S')
        adjustedTimeStamp=regularTimeStamp-timedelta(hours=19)
        feature.setAttribute(inShape.fields().indexFromName('Adj_Date'),adjustedTimeStamp.strftime('%Y-%m-%d'))
        feature.setAttribute(inShape.fields().indexFromName('Adj_Hour'),adjustedTimeStamp.hour)
        inShape.updateFeature(feature)
inShape.updateFields()
