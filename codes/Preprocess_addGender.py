import ogr
import os
import csv
from datetime import datetime,timedelta
from qgis.core import *
import qgis.utils

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
    if fieldName.startswith('Gender'):
        fieldIndex=inShape.fields().indexFromName(fieldName)
        deleteFieldsIndex.append(fieldIndex)
#delete existing time_str fields
if caps&QgsVectorDataProvider.DeleteAttributes:
    inShape.dataProvider().deleteAttributes(deleteFieldsIndex)
    
#Update Attributes with gender
if caps&QgsVectorDataProvider.AddAttributes:
    inShape.dataProvider().addAttributes([QgsField('Gender',QVariant.String)])
    
# Get index of field to insert string
insertIndex=inShape.fields().indexFromName('Gender')

#Read tag and update gender field with corresponding gender
with edit(inShape):
    for feature in inShape.getFeatures():
        feature.setAttribute(insertIndex, gender.get(feature['tag_ident']))
        #print(feature.fieldNameIndex('Gender'),feature['tag_ident'])
        inShape.updateFeature(feature)
inShape.updateFields()