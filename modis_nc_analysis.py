#!/usr/bin/env python
# -*- coding: utf-8 -*- 

###import packages
import netCDF4 as nc
import xarray as xr
import numpy as np


'''
modis_nc_analysis.py

Purpose:

Script for analysis forest cover change through time based on the 0.05 degree MCD12C1 land cover product.
The data has been previously converted from hdf to nc, including addition of coordinates.
    
'''

__author__ = "E Sands"
__email__ = "e.g.sands@ed.ac.uk"



#### data preparation ####

### load data
fn = '../landclassdata_modis/mcd12c1_2001-2019.nc' # provide file path and name
ds = xr.open_dataset(fn)                              # load file

# uncomment to check info on variables and dimensions
# print(ds)

# get variables with subsetting option
lc = ds['lc'][:]  # or subset e.g. ds['lc'][0, 3000:3100, 5000:5200] = (data for 2001 in a given region)

# or subset using lat lon
min_lon = -15
max_lon = 70
min_lat = 35
max_lat = 73
mask_lon = (lc.lon >= int(min_lon)) & (lc.lon <= int(max_lon))
mask_lat = (lc.lat >= int(min_lat)) & (lc.lat <= int(max_lat))    
#lc_crop = lc.where(mask_lon & mask_lat, drop=True)
    

# uncomment to check variables
# print(lc)
# print(lc_crop)

### any quality checks?

### categorise as forest/non forest areas, produce new file for future analyses
# identify forest
#forest_mask = lc.isin([1,2,3,4,5])
#forest_mask = lc_crop.isin([1,2,3,4,5]) # uncomment to work on subset
#print(forest_mask)
#forest = xr.ones_like(lc)
forest = lc
forest.where(forest.isin([1,2,3,4,5]), 0)
forest.where(forest.isin([0]),1)
print(forest)
print(np.unique(forest.values))
# save new forest/not forest file
#forest_mask.to_netcdf('../mcd12c1_forest_boolean.nc', mode='w', format = 'NETCDF4_CLASSIC')

#### change through time ####

### get annual values for e.g. 5x5 squares (converted to km2?)

### trend for each 5x5 square over time 

### display 
