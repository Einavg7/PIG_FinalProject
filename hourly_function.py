import os
from qgis.core import *
import qgis.utils
import ogr
import csv
from datetime import datetime,timedelta
import qgis.utils
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import operator

shape_file = os.path.join('C:\\', 'Users', 'einav', 'Dropbox', \
'summer semester 2020', 'Python in GIS', \
'Final Project', '40442016_04_19.shp')
layer = QgsVectorLayer(shape_file, "shp_layer", "ogr")
if not layer.isValid():
    print("Layer failed to load!")
    

def FeatureByID(layer, featureid):
    iterator = layer.getFeatures(QgsFeatureRequest(featureid))
    feature = QgsFeature()
    if iterator.nextFeature(feature):
        return feature
        return None
    
def SortMovementDataByTime(layer, sortAttributeName):
    if layer == None:
        print("No Layer")
        return
    #find the index of sorting attribute
    sortIndex = layer.fields().indexFromName(sortAttributeName)
    print("sort index"+str(sortIndex))
    
    if sortIndex < 0:
        print("Invalid sort field Name " + sortAttributeName)
        return
      
    #create a list having fature id and attribute value which need to be sorted    
    table = []
    for index, feature in enumerate(layer.getFeatures()):
        #print(index, feature[sortIndex])
        record = feature.id(), feature.attributes()[sortIndex]
        #print(record)
        table.append(record)
    
    #sort the table with attribute values
    table.sort(key = operator.itemgetter(1))

    #store each sorted feature of layer in a 2D array
    feature_list = []
    colCount = len(layer.fields())
    for index, record in enumerate(table):
        # find the features in order of sorted indices
        feature = FeatureByID(layer,record[0])
        attrs = feature.attributes()
        attr_list = []
        for c in range(colCount):
            attr_list.append(c)
            attr_list.insert(c,attrs[c])
            
        feature_list.insert(index, attr_list)
        index = index +1
    
    #check values
    for r in feature_list:
        count = 0 
        for c in r: 
            if count == sortIndex:
                print(c,end = " ")
            count = count + 1


def hourlyDistanceTableShape(shape_path, group_field, sum_field):
    """
    Parameters
    ----------
    shape_path (path): path to the directory of shape files
    group_field (String): Name of field to group by -> hours
    sum_field (String): Name of field to calculate sum from -> distance
    Returns
    -------
    Table(csv)
    """ 
    #name_of_table = []
    layer = QgsVectorLayer(shape_path, "shp_layer", "ogr")
    if not layer.isValid():
        print("Layer failed to load!")
    features = layer.getFeatures()
    for feature in features: 
        hours = feature[group_field]
        distance = feature[sum_field]
    output_dict = dict()
    prev_hour = 0
    sum_value = 0
    length_layer = len(layer)
    length_layer_1 = length_layer + 1
    for i in range(0,length_layer_1):  
        if i == 0 :
            prev_hour = hours[i]
            sum_value = [distance[i]]
        elif i == length_layer_1:
            output_dict[hours[i-1]] = sum_value  
        elif hours[i] == prev_hour: 
            sum_value = sum_value + distance[i]
        else : 
            output_dict[hours[i-1]]= sum_value 
            sum_value = 0
            prev_hour = hours[i] 
            sum_value = [distance[i]] 
            with open('C:\\Users\\einav\\Desktop\\Rannana\\test2.csv', 'w') as f:
                for key in output_dict.keys():
                    f.write("%s,%s\n"%(key, output_dict[key]))

SortMovementDataByTime(layer, 'Hour')
hourlyDistanceTableShape(shape_file, 'Hour', 'Distance')

path = 'C:\\Users\\einav\\Dropbox\\summer semester 2020\\Python in GIS\\Final Project\\csv'

def hourlyDistanceTableCSV(file_path, column, column2):
    output_dict = dict()
    """
    Parameters
    ----------
    file_path (path): path to the directory of csv
    column (String): Name of column to calculate sum from
    column (String): Add gender column
    Returns
    -------
    Table(csv)
    """
    for files in os.listdir(file_path):
        # load only the shapefiles
        if files.endswith(".csv"):
    # create vector layer object
            with open (files) as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                print(reader)
                data = {}
                sum_distance = 0
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]
                        attr = data[column]
                        gender = data[column2]
                    if attr == NULL:
                        continue
                    else:
                        sum_distance = sum_distance + attr
                output_dict[files] = [sum_distance, gender]
            #print(output_dict)
            #save dictionary to csv file
            with open('C:\\Users\\einav\\Desktop\\Rannana\\test2.csv', 'w') as f:
                for key in output_dict.keys():
                    f.write("%s,%s\n"%(key, output_dict[key]))

hourlyDistanceTableCSV(path, 'lat', 'Gender') 


#### issues & comments ####
# 1. still not finished - first function by shp
# 2. first function takes shapefiles and second takes csv files
# 3. shapefile funciton - sort by hours first!