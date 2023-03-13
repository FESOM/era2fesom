## ERA2FESOM

Converts ERA5 data located on DKRZ to netCDF, that can be used as FESOM2 forcing.
Work mainly done by Lorenzo Zampieri @lzampier, and then adapted by @koldunovn, so all mistakes are on him :)

Steps of conversion

- We have to convert data from GRIB to netCDF (`grib2netcdf.py`). This can be done simply by allocating an interactive node and running the script.
- We have to convert netCDF files to the right units. We submit the job with `era5_forcing.bash`, that will call the `processing_era5.py` script.


