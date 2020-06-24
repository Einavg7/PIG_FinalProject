import os
from qgis.core import *
import qgis.utils

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
def RemoveFields(layer):
#    #fields = layer.dataProvider().fields()
    caps = layer.dataProvider().capabilities()
        
    if caps & QgsVectorDataProvider.DeleteAttributes:
        fieldNamesToRemove = ['battery_vo','fix_batter','horizontal', 'key_bin_ch','speed_accu','status','temperatur',
                                'type_of_fi', 'speed','heading','height','outlier_ma','visible','sensor_typ','individual',
                                'ind_ident','study_name']
        fields = layer.dataProvider().fields()
           
        for i in range(len(fieldNamesToRemove)):
            index = 0
            for field in fields:
                print(fieldNamesToRemove[i])
                if field.name() == fieldNamesToRemove[0]:
                    res = layer.dataProvider().deleteAttributes([index])
                    break
                index += 1
                
        layer.updateFields()

fileDir = 'c:/wwu/movebank/eagle_owl/points.shp'
layer = OpenFile(fileDir)

if layer is not None:
    print (layer)
    RemoveFields(layer)