import os
from qgis.core import *
import qgis.utils
import ogr
import csv
from datetime import datetime,timedelta
import qgis.utils
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import random

def sumField(layer, field):
    """  
    Parameters
    ----------
    layer (vector layer): The layer to compute on
    field (String):Name of field to calculate sum from
    Returns
    -------
    Value
    """
    features = layer.getFeatures()
    sum_distance = []
    for feature in features:
        attr = feature[field]
        if attr == NULL:
            continue
        else:
            sum_distance.append(attr)
    print(sum(sum_distance))

def dailyDistanceTable(file_path, field, field2):
    output_dict = dict()
    """
    Parameters
    ----------
    file_path (path): path to the directory of shapefiles
    field (String): Name of field to calculate sum from
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
            with open('C:\\Users\\einav\\Desktop\\Rannana\\test.csv', 'w') as f:
                for key in output_dict.keys():
                    f.write("%s,%s\n"%(key, output_dict[key]))

dailyDistanceTable("C:\\Users\\einav\\Dropbox\\summer semester 2020\\Python in GIS\\Final Project", 'distance', 'Gender')

##### issues #####
# 1. add field names to csv table
# 2. remove [] from the keys
# 3. try 'test.csv' without file path


