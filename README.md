Steps of conversion

- We have to convert data from GRIB to netCDF (`process_era5.bash`)
- We have to convert netCDF files to right units (`era5_forcing.bash` and `processing.py`)


Variables are located in two different branches `sf12` and `sf00`, so the conversion to netCDF should be done separatelly for each of the branches.

