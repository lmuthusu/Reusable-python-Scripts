# Author : Lalitha Muthu Subramanian
# NMWRRI Scripts using arcpy module

#Import Modules
import os
import arcpy
import glob

# Enable Overwrite as True here
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

#Initialize the HDF Bands here
hdf_list = glob.glob(r'E:\NDVI\HDF\*.hdf')

# Define O/p folder
outws = r'E:\NDVI\EXTRACTED_NDVI\\'

# Extract Subset Data from HDF files into tiffs

print()

# For Loop to go through all the files and extract Bands
for hdf in hdf_list:

    # Extract Band Numbers (Variables of HDFs)
    MODIS_Product = os.path.basename(hdf).split(".")[0]
    A = os.path.basename(hdf).split(".")[1]
    modis_grid_code = os.path.basename(hdf).split(".")[2]
    version = os.path.basename(hdf).split(".")[3]
    B = os.path.basename(hdf).split(".")[4]
    name = MODIS_Product + "_" + A + "_" + modis_grid_code + "_" + version + ".tif"

    print()
    print("\t - Extracting NDVI from... " + MODIS_Product + " " + B )
    arcpy.ExtractSubDataset_management( hdf, outws + name , "0")
    print("\t\t - Successful")

print()
print("HDF DATA EXTRACTING SUCCESSFUL...")
print()


# Rasters to same day mosaics

print("Commencing Stiching of MOODIS tiles...")
print()

extracted_NDVI = r'E:\NDVI\EXTRACTED_NDVI\\'
outws1 = r'E:\NDVI\MODIS_stiched\\'

for year in range(2014, 2017):
    for doy in range(1, 367):
        DOY_str = "{0:0=3d}".format(doy)
        H09V05 = "MOD13Q1_A" + str(year) + str(DOY_str) + "_h09v05_005.tif"
        H08V05 = "MOD13Q1_A" + str(year) + str(DOY_str) + "_h08v05_005.tif"

        if arcpy.Exists(extracted_NDVI + H09V05):
            try:
                outloc = r'E:\NDVI\MODIS_stiched\\'
                name = r'MOD13Q1_A' + str(year) + str(DOY_str) + r'_005.tif'
                print()
                print("\t - Stiching NDVI " + str(year)+ str(DOY_str) + "...")
                arcpy.MosaicToNewRaster_management(extracted_NDVI + H09V05 + r';' + extracted_NDVI + H08V05, outloc, name, "#", "16_BIT_SIGNED", "#", "1", "MEAN", "FIRST")
                print("\t\t - Successful")

            except:
                print("\t\t- Error")
                print(arcpy.GetMessages())

        else:
            print()
            print("\t - NDVI MODIS image for " +str(year)+ str(DOY_str) + " does not exist.")


# Project MODIS Tiffs into WGS 84

print()
print("Commencing Re-Projection of MODIS Tiffs...")
print()

tiff_list = glob.glob(r'E:\NDVI\MODIS_stiched\*.tif')
outws2 = r'E:\\NDVI\\WGS_MODIS_NDVI\\'

for tiff in tiff_list:
    name = r'WGS_' + os.path.basename(tiff).split(".")[0]

    #Projection: From MODIS nadir into WGS
    out_tiff = outws2 + name + ".tif"
    print()
    print("\t - Projecting... " + name)
    arcpy.ProjectRaster_management(tiff, out_tiff,\
                                   # Out Coordinate System
                                   "GEOGCS['CGS_WGS_1984',\
                                   DATUM['D_WGS_1984',\
                                   SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                                   PRIMEM['Greenwich',0.0],\
                                   UNIT['Degree',0.0174532925199433],\
                                   METADATA['World',-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]",\
                                   # Sampling Method
                                   "NEAREST",\
                                   # Cell Size
                                   "#",\
                                   # Geographic Transformation
                                   "",\
                                   # Registration Point
                                   "",\
                                   # In Coordinate System
                                   "PROJCS['Unknown_datum_based_upon_the_custom_spheroid_Sinusoidal',\
                                   GEOGCS['GCS_Unknown_datum_based_upon_the_custom_spheroid',\
                                   DATUM['D_Not_specified_based_on_the_custom_spheroid',\
                                   SPHEROID['Custom_spheroid',6371007.181,0.0]],\
                                   PRIMEM['Greenwich',0.0],\
                                   UNIT['Degree',0.0174532925199433]],\
                                   PROJECTION['Sinusoidal'],\
                                   PARAMETER['false_easting',0.0],\
                                   PARAMETER['false_northing',0.0],\
                                   PARAMETER['central_meridian',0.0],\
                                   UNIT['Meter',1.0]]")
    print("\t\t - Successful")

print()
print("MODIS DATA REPROJECTION SUCCESSFUL...")
print()


# Clip Raster to New Mexico Boundaries

print()
print("Commencing Clipping of MODIS Tiffs into New Mexico...")
print()

wgs_list = glob.glob(r'E:\NDVI\WGS_MODIS_NDVI\*.tif')
outws3 = r'E:\\NDVI\\NM_NDVI\\'
nm_shapefile = r'E:\ClimateChange\CC.gdb\WGS84_NM'

for tiff in wgs_list:
    name = r'NM_' + os.path.basename(tiff).split(".")[0]
    out_tiff = outws3 + name + r'.tif'
    print()
    print("\t - Clipping MODIS File: " + name)
    arcpy.Clip_management(tiff, "-109.050173 31.332177 -103.001973 37.000293", out_tiff, nm_shapefile, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
    print("\t\t - Successful")

print()
print("MODIS DATA CLIPPING SUCCESSFUL...")
print()


# Project Raster to UTM ZONE 13N

print()
print("Commencing Projection of Clipped MODIS Tiffs into UTM ZONE 13N...")
print()

utm_list = glob.glob(r'E:\NDVI\NM_NDVI\*.tif')
outws4 = r'E:\\NDVI\\UTM_NDVI\\'

for tiff in utm_list:
    name = r'UTM_' + os.path.basename(tiff).split(".")[0]
    out_tiff = outws4 + name + ".tif"


    if arcpy.Exists(tiff):
        try:
            prj = r'C:\Users\fochoa\AppData\Roaming\ESRI\Desktop10.4\ArcMap\Coordinate Systems\NAD 1983 UTM Zone 13N.prj'
            incs = r'C:\Users\fochoa\AppData\Roaming\ESRI\Desktop10.4\ArcMap\Coordinate Systems\GCS_WGS_1984.prj'
            print()
            print("\t - Projecting to UTM ZONE 13N MODIS File: " + name)
            arcpy.ProjectRaster_management(tiff,out_tiff,prj,"NEAREST","231.6563583","WGS_1984_(ITRF00)_To_NAD_1983","",incs)
            print("\t\t - Successful")

        except:
            print("\t\t- Error")
            print(arcpy.GetMessages())
            print()

    else:
        print()
        print("\t\t - " + tiff + "does not exist...")

print()
print("PROJECTION OF MODIS DATA TO UTM ZONE 13N SUCCESSFUL...")
print()

# Apply Mathematical Correction to TIFF

print()
print("Commencing Mathematical Corrections of MODIS Files...")
print()


tiff_list = glob.glob(r'E:\NDVI\UTM_NDVI\*.tif')
outws5 = r'E:\NDVI\CORRECTED_NDVI\\'

for tiff in tiff_list:
    name = r'NM_UTM_' + os.path.basename(tiff).split(".")[0]
    out_tiff = outws5 + name + ".tif"
    print()
    print("\t - Applying Mathematical Correction to MODIS File: " + name)
    ndvi = arcpy.Raster(tiff) * 0.0001
    ndvi.save(out_tiff)
    print("\t\t - Successful")

print()
print("MATHEMATICAL CORRECTION OF MODIS FILES COMPLETE...")
print()


# Adjust Columns Rows to ETRM

print()
print("Adjusting Columns and Rows...")
print()

etrm_list = glob.glob(r'E:\NDVI\CORRECTED_NDVI\\*.tif')
outws7 = r'E:\NDVI\ADJ_CR\\'

for tiff in etrm_list:
    name = r'UTM_NM' + os.path.basename(tiff).split(".")[0]
    out_tiff = outws7 + name + ".tif"


    if arcpy.Exists(tiff):
        try:
            print()
            print("\t - Adjusting Columns and Rows on..." + name)
            Spatial_ext = "114807 3471163 682757 4102413"
            nm_polygon =  r'E:\ETRM_Inputs\NM_Geo_Shapes\NM_State_Polygons\NM_State.shp'
            arcpy.Clip_management(tiff, Spatial_ext, out_tiff, nm_polygon, "#", "ClippingGeometry", "MAINTAIN_EXTENT")
            print("\t\t - Successful")

        except:
            print("\t\t- Error")
            print(arcpy.GetMessages())
            print()
    else:
        print()
        print("\t\t - " + tiff + "does not exist...")

# Resample to ETRM Resolution


print()
print("Commencing MODIS Resampling into ETRM Resolution...")
print()

NDVI_list = glob.glob(r'E:\NDVI\ADJ_CR\\*.tif')
outws6 = r'E:\NDVI\ETRM_NDVI\\'

for tiff in NDVI_list:
    name = r'ETRM_NDVI_' + os.path.basename(tiff).split(".")[0]
    out_tiff = outws6 + name + ".tif"
    print()
    print("\t - Resampling to ETRM Resolution.... " + name)
    arcpy.Resample_management(tiff, out_tiff, "250", "CUBIC")
    print("\t\t - Successful")

print()
print("MODIS RESAMPLING COMPLETE...")
print()


# Readjust Columns and Rows

print()
print("Adjusting Columns and Rows...")
print()

etrm_list1 = glob.glob(r'E:\NDVI\ETRM_NDVI\*.tif')
outws8 = r'E:\NDVI\FINAL_ETRM_NDVI\\'

for tiff in etrm_list1:
    name = os.path.basename(tiff).split(".")[0]
    out_tiff = outws8 + name + ".tif"


    if arcpy.Exists(tiff):
        try:
            print()
            print("\t - Adjusting Columns and Rows on..." + name)
            Spatial_ext = "114807 3471163 682757 4102413"
            nm_polygon =  r'E:\ETRM_Inputs\NM_Geo_Shapes\NM_State_Polygons\NM_State.shp'
            arcpy.Clip_management(tiff, Spatial_ext, out_tiff, "#", "#", "#", "MAINTAIN_EXTENT")
            print("\t\t - Successful")

        except:
            print("\t\t- Error")
            print(arcpy.GetMessages())
            print()

    else:
        print()
        print("\t\t - " + tiff + "does not exist...")

print()
print("Geoprocessing complete...")
