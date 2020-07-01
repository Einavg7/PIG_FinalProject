import os
from qgis.core import *
import qgis.utils
import operator

def CalculateDistanceBetweenConsecutivePoints(point1, point2):
    point1 = QgsPointXY(point1["long"],point1["lat"])
    point2 = QgsPointXY(point2["long"],point2["lat"])
    distance = QgsDistanceArea()
    m = distance.measureLine(point1, point2)
    return m

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
            
            print(pointCurrent)
            print(pointBefore)
            print(feature.id(),)
            distance = CalculateDistanceBetweenConsecutivePoints(pointCurrent,pointBefore)
            distanceList.append(distance)
            
        else:
            print(feature.id())
            distance = 0
            distanceList.append(feature.id(),distance)
            
        caps=layer.dataProvider().capabilities()
        if caps&QgsVectorDataProvider.AddAttributes:
            layer.dataProvider().addAttributes([QgsField('ConsecutiveDistance', QVariant.float)])
            
        layer.startEditing()
            for feature in layer.Getfeatures():
                feature.fields().indexFromName('ConsecutiveDistance',distanceList[feature.id()])
                layer.updateFeature()
        layer.commitChanges() 
        layer.updateFiels()
                
            
  
        
#SortMovementDataByTime(layer, "timestamp")
