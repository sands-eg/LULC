from netCDF4 import Dataset
import numpy as np
from osgeo import gdal
import xarray as xr
import datetime as dt
from netCDF4 import date2num, num2date

# code adapted from: https://unidata.github.io/python-training/workshop/Bonus/netcdf-writing/

# falesafe to not overwrite data
try: ncfile.close()
except: pass

# creating new empty netCDF file
ncfile = Dataset('mcd12c1_2001-2019.nc', mode='w', format='NETCDF4_CLASSIC')
print(ncfile)

# define MODIS latitude and longitude
rows = np.arange(89.975, -90.01, -0.05) # latitude values
columns = np.arange(-179.975, 180.01, 0.05) # longitude values

# creating dimensions
lat_dim = ncfile.createDimension('lat', len(rows))     # lat axis
lon_dim = ncfile.createDimension('lon', len(columns))  # lon axis
time_dim = ncfile.createDimension('time', None)        # unlimited axis (enables appending)

for dim in ncfile.dimensions.items():
	print(dim)

# defining variables
# Define two variables with the same names as dimensions,
# a conventional way to define "coordinate variables".
lat = ncfile.createVariable('lat', np.float32, ('lat',))
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lon = ncfile.createVariable('lon', np.float32, ('lon',))
lon.units = 'degrees_east'
lon.long_name = 'longitude'
time = ncfile.createVariable('time', np.float64, ('time',))
time.units = 'hours since 1800-01-01'
time.long_name = 'time'

# Define a 3D variable to hold the data
lc = ncfile.createVariable('lc',np.float64,('time','lat','lon')) # note: unlimited dimension is leftmost
lc.units = 'categorical' # full legend in MCD12C1 user guide
lc.standard_name = 'land_cover' # check if there is a CF standard name
print(lc)

# dates
years = np.arange(2001, 2020)
dates =[None]*19
for i,y in enumerate(years):
	dates[i] = dt.datetime(y, 12,31,0,0)
#print(dates)


### adding lc data
for i, y in enumerate(years):
	file_path = f'../landclassdata_modis/MCD12C1.A{y}001.006.hdf' 
	modis_pre = gdal.Open(f"HDF4_EOS:EOS_GRID:{file_path}:MOD12C1:Majority_Land_Cover_Type_1")
	ann_lc = modis_pre.ReadAsArray()
	lc_ref = xr.DataArray(data=ann_lc, coords={'lat': rows, 'lon': columns})
	lc_ref = lc_ref.expand_dims('time', axis=0)
	lc[i,:,:] = lc_ref
	
print('Data added, lc.shape is now ', lc.shape)
print('min/mas value:', lc[:,:,:].min(), lc[:,:,:].max())

# assigning data to time variable
times = date2num(dates, time.units)
time[:]=times
print(time[:])
print(time.units)
print(num2date(time[:], time.units))

# checking final file
print(ncfile)

# close Dataset
ncfile.close()
print('Dataset is closed')
