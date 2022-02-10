#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import sys
import xarray as xr
import rioxarray as rio 
from shapely.geometry import mapping 
import numpy as np
import geopandas

'''
legal_amazon_change_esa.py

Purpose:

	Calculate forest area change between 2 years (from the period 2001-2019)
    in the Legal Amazon as used here: http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/prodes
    
    Returns total change in forest area in km2.
'''

__author__ = "E Sands"
__email__ = "e.g.sands@ed.ac.uk"



def load_esa(year):
    ''' 
    Function to load global ESA CCI data
    for a given year. Expected netCDF format.
    
    Data previously downloaded from teh ESA CCI website.
    
    Year must be between 2001 and 2019.
    '''
    if int(year) < 2016:
        file_path = f"../landclassdata_esa/ESACCI-LC-L4-LCCS-Map-300m-P1Y-{year}-v2.0.7cds.nc"
    else:
        file_path = f"../landclassdata_esa/C3S-LC-L4-LCCS-Map-300m-P1Y-{year}-v2.1.1.nc"
    
    data = xr.open_dataset(file_path)
    
    data = data['lccs_class'].squeeze('time') # removing unnecessary time dimension
    
    return data
    
    

def clip_legal_amazon(year):
    ''' 
    Function to clip ESA LC CCI data to Brazilian Legal Amazon boundaries.
    '''
    # keep track when run from command line
    print('clipping esa data for', year)
    
    # load data for clipping
    data=load_esa(year)
    data_crs = data.rio.write_crs(4326) # esa cci lc data provided in WGS84/Plate Carree
    
    # load legal amazon shapefile. Available for download here: 
    # http://terrabrasilis.dpi.inpe.br/geonetwork/srv/eng/catalog.search#/metadata/d6289e13-c6f3-4103-ba83-13a8452d46cb
    brazil = geopandas.read_file('../shapefiles/brazilian_legal_amazon.shp', crs = 'epsg:4674')
    
    # clip
    esa_clipped = data_crs.rio.clip(brazil.geometry.apply(mapping), brazil.crs) # mapping required as projections are different
    
    print('Clip succesful')
    
    return esa_clipped 



# identify forest in clipped data
def forest_esa(lc):
    ''' 
    Function to identify cells classified as forest in  ESA LC CCI data and calculate their total area.
    
    Input: ESA LC 
    
    Output: 
    - array classified as forest (1) and non forest (0)
    - sum of forest area in km^2 
    '''
    
    forest = np.where(np.logical_or(np.logical_and(lc >=50, lc <=100), np.logical_and(lc >= 160, lc <= 170)), 1, 0)
    
    area = np.sum(forest, axis=(0,1)) * 0.09
    
    print(f'forest area in legal amazon = {area} km2')
    
    return forest, area


### to run from command line with arguments (start year and end year):
def main(start_y, end_y):
   lc1 = clip_legal_amazon(start_y)
   lc2 = clip_legal_amazon(end_y)
   
   forest1, area1 = forest_esa(lc1)
   forest2, area2 = forest_esa(lc2)
   
   change = area2 - area1 
   
   print(f'Total forest area change in the legal amazon\nbetween {start_y} and {end_y} was {change} km2')
   
   return change

if __name__ == "__main__":
   main(sys.argv[1], sys.argv[2])
    

### to print out forest area for each year for 2001-2019 uncomment following lines and comment if __name__ section

# for y in range(2009, 2019):
    # lc = clip_legal_amazon(y)
    # forest, area = forest_esa(lc)
    # print(f'Forest area in {y} = {area} km^2')
