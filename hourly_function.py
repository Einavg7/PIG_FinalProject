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
    

def hourlyDistanceTable(layer, group_field, sum_field):
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
            with open('C:\\Users\\einav\\Desktop\\Rannana\\test2.csv', 'w') as f:
                for key in output_dict.keys():
                    f.write("%s,%s\n"%(key, output_dict[key]))

hourlyDistanceTable(layer, 'Hour', 'Distance')




#### issues & comments ####
# Has to take the same hours one after the other 
