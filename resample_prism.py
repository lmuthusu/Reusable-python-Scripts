# Author : Lalitha Muthu Subramanian
# NMWRRI Scripts using arcpy module
# This Script calculates the Tmax(Maximum Temperature) and Tmin value (Minimum Temperature) for
# DSWB model from the PRISM data


import os
import glob

#added a new line
# Script projects PRISM 800m to ETRM Resolution
# Check Out Spatial License & Enable Overwrite

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True


prism_variab = ["Tmin"] #hello

for variable in prism_variab:
    if variable == r'Precip':
        print("Geoprocessing PRISM PRECIP Data...")
        for year in range(2014, 2019):
            path = r'E:\\PRISM\\PRISM\\Daily\\ppt\BEST\\' + str(year) + r'\\'

            prism_precip_list = glob.glob(path + '*.bil')

            for precip in prism_precip_list:
                tiff_name = os.path.basename(precip).split(".")[0]
                date = os.path.basename(tiff_name).split("_")[4]

                # Clip CONUS to NMHW Mask
                Spatial_ext = r'-109.339129 38.494207 -102.957079 31.296145'
                clip_outraster = r'E:\\Scratch\\NMHW_Precip_' + date + ".tif"
                nmhw =  r'E:\Reference_ET\Verification\GCS_PRISM_4km.shp'

                arcpy.Clip_management(precip, Spatial_ext, clip_outraster, nmhw, "#", "ClippingGeometry", "MAINTAIN_EXTENT")

                # Project to UTM Zone 13N
                prj_outraster = r'E:\\NMHW_PRISM\\Precip\\Daily\\' + str(year) + r'\\' + r'PRISMD2_NMHW2mi_' + date + r'.tif'
                prj = r'E:\ETRM_Inputs\NM_Geo_Shapes\NM_State_Polygons\NM_State.prj'
                arcpy.ProjectRaster_management(clip_outraster, prj_outraster, prj, "NEAREST", "861.012439489016", "#", "#", "#")

                # Clip to NM Boundaries
                Spatial_ext = "114807 3471163 682757 4102413"
                clip_outraster = r'E:\\Scratch\\UTM_PRISM_PRECIP_' + date + ".tif"
                nm_polygon =  r'E:\ETRM_Inputs\NM_Geo_Shapes\NM_State_Polygons\NM_State.shp'

                arcpy.Clip_management(prj_outraster, Spatial_ext, clip_outraster, nm_polygon, "#", "ClippingGeometry", "MAINTAIN_EXTENT")

                # Resample to ETRM Spatial Resolution
                resample_outraster = r'E:\\ETRM_Inputs\\PRISM\\precip\\800m_std_all\\PRISMD2_NMHW2mi_' + date + r'.tif'
                arcpy.Resample_management(clip_outraster, resample_outraster, "250", "CUBIC")

                os.remove(clip_outraster)
        print("\t - PRISM PRECIP DATA PROCESS COMPLETE...")
        print()

    elif variable == "Tmax":
        print("Geoprocessing PRISM Tmax Data...")
        for year in range(2014, 2019):
            path = r'E:\\NMHW_PRISM\\Tmax\\' + str(year) + r'\\'

            prism_tmax_list = glob.glob(path + '*.tif')

            for tmax in prism_tmax_list:
                tiff_name = os.path.basename(tmax).split(".")[0]
                date = os.path.basename(tiff_name).split("_")[2]

                # Project to UTM Zone 13N
                prj_outraster = r'E:\\NMHW_PRISM\\UTM_Tmax\\' + str (year) + r'\\' + r'PRISM_Tmax_' + date + r'.tif'
                prj = r'E:\ETRM_Inputs\NM_Geo_Shapes\NM_State_Polygons\NM_State.prj'
                arcpy.ProjectRaster_management(tmax, prj_outraster, prj, "NEAREST", "861.012439489016", "#", "#", "#")

                # Clip to NM Boundaries
                Spatial_ext = "114807 3471163 682757 4102413"
                clip_outraster = r'E:\\Scratch\\UTM_PRISM_Tmax_' + date + ".tif"
                nm_polygon =  r'E:\ETRM_Inputs\NM_Geo_Shapes\NM_State_Polygons\NM_State.shp'

                arcpy.Clip_management(prj_outraster, Spatial_ext, clip_outraster, nm_polygon, "#", "ClippingGeometry", "MAINTAIN_EXTENT")

                # Resample to ETRM Spatial Resolution
                resample_outraster = r'E:\\ETRM_Inputs\\PRISM\\Temp\\Maximum_standard\\TempMax_NMHW2Buff_' + date + r'.tif'
                arcpy.Resample_management(clip_outraster, resample_outraster, "250", "CUBIC")

        print("\t - PRISM TMAX DATA PROCESS COMPLETE...")
        print()

    elif variable == "Tmin":
        print("Geoprocessing PRISM Tmin Data...")
        for year in range(2014, 2015):
            path = r'E:\\NMHW_PRISM\\Tmin\\' + str(year) + r'\\'

            prism_tmin_list = glob.glob(path + '*.tif')

            for tmin in prism_tmin_list:
                tiff_name = os.path.basename(tmin).split(".")[0]
                date = os.path.basename(tiff_name).split("_")[2]

                # Project to UTM Zone 13N
                prj_outraster = r'E:\\NMHW_PRISM\\UTM_Tmin\\' + str (year) + r'\\' + r'PRISM_Tmin_' + date + r'.tif'
                prj = r'E:\ETRM_Inputs\NM_Geo_Shapes\NM_State_Polygons\NM_State.prj'
                arcpy.ProjectRaster_management(tmin, prj_outraster, prj, "NEAREST", "861.012439489016", "#", "#", "#")

                #Clip to NM Boundaries
                Spatial_ext = "114807 3471163 682757 4102413"
                clip_outraster = r'E:\\Scratch\\UTM_PRISM_Tmin_' + date + ".tif"
                nm_polygon =  r'E:\ETRM_Inputs\NM_Geo_Shapes\NM_State_Polygons\NM_State.shp'

                arcpy.Clip_management(prj_outraster, Spatial_ext, clip_outraster, nm_polygon, "#", "ClippingGeometry", "MAINTAIN_EXTENT")

                # Resample to ETRM Spatial Resolution
                resample_outraster = r'E:\\ETRM_Inputs\\PRISM\\Temp\\Minimum_standard\\cai_tmin_us_us_30s_' + date + r'.tif'
                arcpy.Resample_management(clip_outraster, resample_outraster, "250", "CUBIC")

        print("\t - PRISM TMIN DATA PROCESS COMPLETE...")
        print()
