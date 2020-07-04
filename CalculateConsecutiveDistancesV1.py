import os
from qgis.core import *
import qgis.utils
import operator

def CalculateDistanceBetweenConsecutivePoints(point1, point2):
    point1 = QgsPointXY(point1["long"],point1["lat"])
    point2 = QgsPointXY(point2["long"],point2["lat"])
    distance = QgsDistanceArea()
    distance = distance.measureLine(point1, point2)
    return distance

def FeatureByID(layer, featureid):
    iterator = layer.getFeatures(QgsFeatureRequest(featureid))
    feature = QgsFeature()
    if iterator.nextFeature(feature):
        return feature

    return None

layer = iface.activeLayer()
if layer is None:
    print("Empty layer")
else:
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
