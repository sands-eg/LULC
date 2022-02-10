#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

'''
map_esa.py

Purpose:

	Create map of ESA CCI land cover classification
	for a given year and region.
    
    Code currently applicable to small regions
    due to time required to run/limited memory
    for loading the high res array.
'''

__author__ = "E Sands"
__email__ = "e.g.sands@ed.ac.uk"

def load_esa(year):
    ''' 
    Function to load global ESA CCI data
    for a given year.
    Data previously downloaded.
    
    Year must be between 2001 and 2019.
    '''
    if int(year) < 2016:
        file_path = f"../landclassdata_esa/ESACCI-LC-L4-LCCS-Map-300m-P1Y-{year}-v2.0.7cds.nc"
    else:
        file_path = f"../landclassdata_esa/C3S-LC-L4-LCCS-Map-300m-P1Y-{year}-v2.1.1.nc"
    
    data = xr.open_dataset(file_path)
    
    data = data['lccs_class'].squeeze('time') # removing unnecessary time dimension
    
    return data-
    
    

def map_esa(year, min_lon, max_lon, min_lat, max_lat):
    ''' 
    Function to create a land cover map for a given year and region.
    '''
    
    data = load_esa(year)
    
    ### create mask for region of interest and crop data
    # mask code based on 
    # https://gis.stackexchange.com/questions/353698/how-to-clip-an-xarray-to-a-smaller-extent-given-the-lat-lon-coordinates
    mask_lon = (data.lon >= int(min_lon)) & (data.lon <= int(max_lon))
    mask_lat = (data.lat >= int(min_lat)) & (data.lat <= int(max_lat))    
    data_crop = data.where(mask_lon & mask_lat, drop=True)
    
    lcm = data_crop 		  # land cover map
    lat = data_crop['lat']        # latitude
    lon = data_crop['lon']        # longitude
    
    ### creat colormap
    esa_colours = ['000000', '#ffff64', '#ffff64', '#ffff00', '#aaf0f0', '#dcf064',\
    '#c8c864', '#006400', '#00a000', '#00a000', '#aac800', '#003c00', '#003c00', '#005000',\
    '#285000', '#285000', '#286400', '#788200', '#8ca000', '#be9600', '#966400', '#966400',\
    '#966400', '#ffb432', '#ffdcd2', '#ffebaf', '#ffc864', '#ffd278', '#ffebaf', '#00785a',\
    '#009678', '#00dc82', '#c31400', '#fff5d7', '#dcdcdc', '#fff5d7', '#0046c8', '#ffffff']
    
    flag_values = np.array([0, 10, 11, 12, 20, 30, 40, 50, 60, 61, 62, 70, 71, 72, 80, 81, 82, 90, 100, 110, 120, 121, 122, 130, 140, 150, 151, 152, 153, 160, 170, 180, 190, 200, 201, 202, 210, 220])
    nodes = flag_values/220
    
    cmap = LinearSegmentedColormap.from_list("ESAcmap", list(zip(nodes, esa_colours)))
 
    ### mapping using contourf - not efficient
    #projection = ccrs.PlateCarree()
    #transform = ccrs.PlateCarree()
    
    #fig = plt.figure(figsize=(12,8))
    #ax = plt.axes(projection=ccrs.Robinson())
    #ax.set_extent([int(min_lon), int(max_lon), int(min_lat), int(max_lat)], crs = ccrs.PlateCarree())
    #ax.coastlines()
    #ax.contourf(lon, lat, lcm, vmin = 0, vmax = 220, cmap = cmap, transform=ccrs.PlateCarree())
    #fig.savefig(f'../figures/test_{year}_{min_lon}_{max_lon}_{min_lat}_{max_lat}.png', dpi=300, bbox_inches='tight')
    
    
    ### basic map/image created using imsave - fast but not elegant
    plt.imsave(f'../figures/esa_lc_map_{year}_{min_lon}_{max_lon}_{min_lat}_{max_lat}.png', lcm, vmin = 0, vmax = 220, cmap = cmap, format = 'png')
	
    
	
def main(year, min_lon, max_lon, min_lat, max_lat):
    map_esa(year, min_lon, max_lon, min_lat, max_lat)

# to execute when run as script
if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
