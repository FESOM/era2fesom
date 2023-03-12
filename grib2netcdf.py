# Python script that converts the ERA5 reanalysis from GRIB2 to netCDF
# So that FESOM2 or other ocen models can use it as forcing field
#
# At the moment, different branches at DKRZ (sf00, sf12, etc.)
# must be processed separately
#
# Based on bash script by Lorenzo Zampieri (lorenzo.zampieri@awi.de)
#
from tqdm import tqdm
import os
import glob
from joblib import Parallel, delayed

month_array = [str(x).zfill(2) for x in range(1, 13)]

in_dir = "/pool/data/ERA5/"
out_dir = "/pool/data/AWICM/FESOM2/FORCING/era5/data/"


def era2fesom(var, year, dataset, level, dtype, data_freq):
    print(f" --- Processing variable {var}")
    workdir = os.path.join(out_dir, year, var, "tmp")
    destdir = os.path.join(out_dir, year, var)
    if not os.path.exists(workdir):
        os.makedirs(workdir)
    os.chdir(workdir)
    grib_folder = os.path.join(in_dir, dataset, level, dtype, data_freq, var)
    print(grib_folder)
    # we don't have to do it over months, but it's here for historical reasons
    for month in month_array:
        grib_files = glob.glob(f"{grib_folder}/*{year}-{month}*.grb")
        grib_files.sort()

        for grib_file in grib_files:
            netcdf_name = os.path.basename(grib_file).replace(".grb", ".nc")
            netcdf_path = os.path.join(workdir, netcdf_name)

            if not os.path.exists(netcdf_path):
                os.system(
                    f"cdo -P 8 -O -f nc setgridtype,regular {grib_file} {netcdf_path}"
                )

    netcdf_month = os.path.join(destdir, f"var{var}.{year}.nc")
    if not os.path.exists(netcdf_month):
        os.system(f"cdo -P 8 -O -f nc mergetime *.nc {netcdf_month}")
        print(netcdf_month)
    os.system(f"rm  {workdir}/*.nc")


## First select those (located in fc directory)
# var_array = ["142", "143", "144", "169", "175", "205"]
# dtype = "fc"  # can be fc or an

## Then select those (located in an directory)
var_array = ["134", "164", "165", "166", "167", "168"]
dtype = "an"


dataset = "EB"
level = "sf"
# year = "1950"
data_freq = "1H"

# era2fesom(
#     "144", year=year, dataset=dataset, level=level, dtype=dtype, data_freq=data_freq
# )

for var in var_array:
    r = Parallel(n_jobs=9)(
        delayed(era2fesom)(
            var=var,
            year=str(i),
            dataset=dataset,
            level=level,
            dtype=dtype,
            data_freq=data_freq,
        )
        for i in range(1950, 1959)
    )
