import glob
import os
import arcpy
import datetime
import pandas as pd

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
print("==========================================================================")

Mesilla_shapefile = r'E:\Aracely\Data\Mesilla_Riparian_Area.shp'

for year in range(2000 , 2016):
    for month in range(1, 13):
        month = "{0:0=2d}".format(month)
        tiff = r'E:\NMHW_PRISM\Precip\Monthly\\' + "PRISMD2_NMHW2mi_" + str(year) + str(month)  +".tif"
        table =r'E:\Scratch\\' + "PRISM" + str(year) + str(month) + ".dbf"
        arcpy.sa.ZonalStatisticsAsTable(Mesilla_shapefile, "ID", tiff, table, "DATA", "ALL")

print("Zonal Stats Complete")
    
