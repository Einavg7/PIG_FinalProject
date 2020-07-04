import os
from qgis.core import *
import qgis.utils
import ogr
import csv
from datetime import datetime,timedelta
import qgis.utils
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import operator

def FeatureByID(layer, featureid):
    """
    Get feature when reuested by feature ID 
    Parameters
    ----------
    layer(Vector) :The layer to be preprocessed
    featureid(Int): Feature ID
    Returns
    -------
    Feature.
    """
    iterator = layer.getFeatures(QgsFeatureRequest(featureid))
    feature = QgsFeature()
    if iterator.nextFeature(feature):
        return feature
    return None
    
def SortMovementDataByField(layer, sortAttributeName):
    """
    Sort and rearrange the entire dataset with the key given by attribute name
    Parameters
    ----------
    layer(Vector) :The layer to be preprocessed
    sortAttributeName(String): Field name to be sorted
    Returns
    -------
    None.
    """
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
               

    #write back to shape file with sorted features
    layer.startEditing()
    #with edit(layer):
    caps=layer.dataProvider().capabilities()
    if caps & QgsVectorDataProvider.ChangeAttributeValues:
        index = 0
        for feature in layer.getFeatures():
            print(feature.id())
            for c in range(colCount):
                print(feature_list[index][c])
                layer.changeAttributeValue(index,c, feature_list[index][c])
                layer.updateFeature(feature)
            index = index + 1
            print("\n")
    layer.commitChanges()          
    layer.updateFields()
    '''
    print("\n---------------- check shape file again! --------------")
    index = 0
    for feature in layer.getFeatures():
        print(feature.id())
        for c in range(colCount):
            print(feature_list[index][c])
        index += 1
        print("\n")
    '''
    
    
    
def CalculateDistanceBetweenConsecutivePoints(point1, point2):
    """
    Calculate distance between any given points
    Parameters
    ----------
    point1(List) : 0th index is longitude and 1st index is latitude of the first point 
    point2(List) : 0th index is longitude and 1st index is latitude of the second point 
    Returns
    -------
    distance
    """
    point1 = QgsPointXY(point1["long"],point1["lat"])
    point2 = QgsPointXY(point2["long"],point2["lat"])
    distance = QgsDistanceArea()
    distance = distance.measureLine(point1, point2)
    return distance
    
    
def AddConsecutiveDistances(layer):
    """
    Adding a field for consecutive distances by calculating distances between two consective points
    Parameters
    ----------
    layer(Vector) : :The layer to be preprocessed
    Returns
    -------
    None
    """
    distanceList  = []
    for feature in layer.getFeatures():
        if feature.id() != 0 and feature.id() > 0 :
            longCurrent = feature['long']
            latCurrent = feature['lat']
            pointCurrent = {"long" : longCurrent,"lat" : latCurrent}
            
            featureIDBefore = feature.id() - 1
            featureBefore = FeatureByID(layer, featureIDBefore)
            longBefore = featureBefore['long']
            latBefore = featureBefore['lat']
            pointBefore = {"long" : longBefore,"lat" : latBefore}
            
            distance = CalculateDistanceBetweenConsecutivePoints(pointCurrent,pointBefore)
            distanceList.append(distance)
        else:
            distance = 0
            distanceList.append(distance)
            
    caps=layer.dataProvider().capabilities()
    fieldName = "ConsDist"
    if caps&QgsVectorDataProvider.AddAttributes:
        layer.dataProvider().addAttributes([QgsField(fieldName,  QVariant.Double)])
   
    layer.startEditing()
    index = 0
    for feature in layer.getFeatures():
        feature[fieldName] = distanceList[index]
        print(distanceList[index])
        index = index + 1
        layer.updateFeature(feature)
        
    layer.commitChanges() 
    layer.updateFields()

def hourlyDistanceTableShape(layer, group_field, sum_field):
    """
    Parameters
    ----------
    layer (shapefile): layer
    group_field (String): Name of field to group by -> hours
    sum_field (String): Name of field to calculate sum from -> distance
    Returns
    -------
    Table(csv)
    """ 
    features = layer.getFeatures()
    hours = []
    distance = []
    for feature in features:
        hours.append(feature[group_field])
        distance.append(feature[sum_field])
    output_dict = dict()
    prev_hour = 0
    sum_value = 0
    length_layer = len(layer)
    for i in range(0,length_layer):  
        if i == 0 :
            prev_hour = hours[i]
            sum_value = distance[i]
            type(sum_value)
        elif i == length_layer:
            output_dict[hours[i-1]] = sum_value
        elif hours[i] == prev_hour: 
            sum_value = sum_value + distance[i]
        else : 
            output_dict[hours[i-1]]= sum_value 
            sum_value = 0
            prev_hour = hours[i] 
            sum_value = distance[i] 
            with open('C:\\Users\\einav\\Desktop\\Rannana\\test2.csv', 'w') as f: # change directory to save csv
                for key in output_dict.keys():
                    f.write("%s,%s\n"%(key, output_dict[key]))

def dailyDistanceTable(file_path, field, field2):
    output_dict = dict()
    """
    Parameters
    ----------
    file_path (path): path to the directory of shapefiles
    field (String): Name of field to calculate sum from
    field (String): Add gender field
    Returns
    -------
    Table(csv)
    """
    for files in os.listdir(file_path):
        # load only the shapefiles
        if files.endswith(".shp"):
    # create vector layer object
            vlayer = QgsVectorLayer(file_path + "/" + files, files, "ogr")
            features = vlayer.getFeatures()
            sum_distance = 0
            for feature in features:
                attr = feature[field]
                gender = feature[field2]
                if attr == NULL:
                    continue
                else:
                    sum_distance = sum_distance + attr
            output_dict[files] = [sum_distance, gender]
            #print(output_dict)
            #save dictionary to csv file
            with open('C:\\Users\\einav\\Desktop\\Rannana\\test.csv', 'w') as f: # change directory to save csv
                for key in output_dict.keys():
                    f.write("%s,%s\n"%(key, output_dict[key]))
    
    
#------------------------Main Program------------------------------------
layer = iface.activeLayer()
if layer is None:
    print("Empty layer")
else:
    SortMovementDataByField(layer, "timestamp")
    AddCumulativeDistances(layer)
    hourlyDistanceTable(layer, 'Hour', 'Distance')
    

dailyDistanceTable("C:\\Users\\einav\\Dropbox\\summer semester 2020\\Python in GIS\\Final Project", 'distance', 'Gender') # change directory to shapefiles 

