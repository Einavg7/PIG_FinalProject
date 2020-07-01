import os
from qgis.core import *
import qgis.utils
import operator

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
                feature.setAttributes([c,feature_list[index][c]])
                layer.updateFeature(feature)
            index = index + 1
            print("\n")
    layer.commitChanges()          

    print("\n---------------- check shape file again! --------------")
    index = 0
    for feature in layer.getFeatures():
        print(feature.id())
        for c in range(colCount):
            print(feature_list[index][c])
        index += 1
        print("\n")
            
    
layer = iface.activeLayer()
SortMovementDataByTime(layer, "timestamp")
