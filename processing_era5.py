# Python script that converts variables from era5 to forcing for FESOM2
# Based on work done by Lorenzo Zampieri

# Import modules

import sys
import os
import shutil
import logging
from rich.logging import RichHandler

log = logging.getLogger("rich")

# import xarray as xr

from cdo import *

cdo = Cdo()  # python version of cdo

# Some initial checks

if len(sys.argv) != 3:
    print("Error: check the number of input parameters")
    sys.exit(1)

# Read var and year as strings from input

var = str(sys.argv[1])
yyyy = str(sys.argv[2])

# List of variables

var_list = ["q", "u", "v", "t2m", "sp", "tcc", "ssrd", "strd", "sf", "rf"]

if int(yyyy) > 2023 or int(yyyy) < 1950:
    print("Error: year out of range [1950,2020]")
    sys.exit(1)

if var not in var_list:
    print("Error: inappropriate variable")
    sys.exit(1)

data_folder = "/pool/data/AWICM/FESOM2/FORCING/era5/data/"
forcing_folder = "/pool/data/AWICM/FESOM2/FORCING/era5/forcing/"

simple_vars = {"u": "165", "v": "166", "t2m": "167", "sp": "134"}
radiation_vars = {"ssrd": "169", "strc": "211", "strd": "175"}

if var in simple_vars:
    nvar = simple_vars[var]
    oldvar = "var" + nvar
    infile = f"{data_folder}/{yyyy}/{nvar}/var{nvar}.{yyyy}.nc"
    outfile = f"{forcing_folder}/inverted/{var}.{yyyy}.nc"
    cdo.setname(
        var,
        input="-invertlat -setreftime,1900-01-01,00:00:00,1day " + infile,
        output=outfile,
        options="-f nc4 -b F32 -P 8",
    )

if var == "q":
    nvar1 = "168"
    nvar2 = "134"
    log.info(f"Processing variable {var}")
    log.info(f"Source GRIB vars: {nvar1} and {nvar2}")
    tmp_folder = forcing_folder + "/tmp" + var + yyyy
    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)
    infile1 = f"{data_folder}/{yyyy}/{nvar1}/var{nvar1}.{yyyy}.nc"
    infile2 = f"{data_folder}/{yyyy}/{nvar2}/var{nvar2}.{yyyy}.nc"
    tmp1 = f"{forcing_folder}/tmp" + var + yyyy + "/tmp1.nc"
    tmp2 = tmp_folder + "/tmp2.nc"
    tmp3 = tmp_folder + "/tmp3.nc"  # e
    tmp4 = tmp_folder + "/tmp4.nc"
    outfile = f"{forcing_folder}/inverted/{var}.{yyyy}.nc"
    # dst = xr.open_dataset(infile1)
    # dsp = xr.open_dataset(infile2)
    a1, a3, a4, t0, Rdv, mRdv = 611.21, 17.502, 32.19, 273.16, 0.62198, 0.37802
    cdo.subc(t0, input=infile1, output=tmp1, options="-f nc4 -b F32 -P 8")
    cdo.subc(a4, input=infile1, output=tmp2, options="-f nc4 -b F32 -P 8")
    cdo.mulc(
        a1,
        input="-exp -mulc," + str(a3) + " -div " + tmp1 + " " + tmp2,
        output=tmp3,
        options="-f nc4 -b F32 -P 8",
    )
    cdo.setname(
        var,
        input="-invertlat -setreftime,1900-01-01,00:00:00,1day -mulc,"
        + str(Rdv)
        + " -div "
        + tmp3
        + " -sub "
        + infile2
        + " -mulc,"
        + str(mRdv)
        + " "
        + tmp3,
        output=outfile,
        options="-f nc4 -b F32 -P 8",
    )
    shutil.rmtree(tmp_folder)

if var in radiation_vars:
    log.info(f"Processing variable {var}")
    tmp_folder = forcing_folder + "/tmp" + var + yyyy
    outfile = f"{forcing_folder}/inverted/{var}.{yyyy}.nc"
    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)
    # Current year
    nvar1 = radiation_vars[var]
    infile1 = f"{data_folder}/{yyyy}/{nvar1}/var{nvar1}.{yyyy}.nc"
    outfile_p1 = f"{tmp_folder}/{var}.{yyyy}.nc"
    cdo.setname(
        var,
        input="-divc,3600 " + infile1,
        output=outfile_p1,
        options="-f nc4 -b F32 -P 8",
    )
    # Previous year
    infile2 = f"{data_folder}/{int(yyyy)-1}/{nvar1}/var{nvar1}.{int(yyyy)-1}.nc"
    if os.path.exists(infile2):
        log.info(f"Previous year available for variable {var}")
        outfile_p2 = f"{tmp_folder}/{var}.{int(yyyy)-1}.nc"
        cdo.setname(
            var,
            input="-divc,3600 " + infile2,
            output=outfile_p2,
            options="-f nc4 -b F32 -P 8",
        )
        cdo.selyear(
            yyyy,
            input="-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,"
            + yyyy
            + "-01-01,00:30:00,1hour -mergetime -seltimestep,8755/8760 "
            + outfile_p2
            + " "
            + outfile_p1,
            output=outfile,
            options="-f nc4 -b F32 -P 8",
        )
    else:
        # this is the first year of the time series
        print(f"File {infile2} does not exist, only using {infile1}")
        cdo.selyear(
            yyyy,
            input="-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,"
            + yyyy
            + "-01-01,00:30:00,1hour -seltimestep,8755/8760 "
            + outfile_p1,
            output=outfile,
            options="-f nc4 -b F32 -P 8",
        )

    shutil.rmtree(tmp_folder)


if var == "rf":
    nvar1 = "142"
    nvar2 = "143"
    log.info(f"Processing variable {var}")
    log.info(f"Source GRIB vars: {nvar1} and {nvar2}")

    tmp_folder = forcing_folder + "/tmp" + var + yyyy
    outfile = f"{forcing_folder}/inverted/{var}.{yyyy}.nc"
    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)
    # Current year
    infile1 = f"{data_folder}/{yyyy}/{nvar1}/var{nvar1}.{yyyy}.nc"
    infile2 = f"{data_folder}/{yyyy}/{nvar2}/var{nvar2}.{yyyy}.nc"
    outfile_p1 = f"{tmp_folder}/{var}.{yyyy}.nc"
    cdo.setname(
        var,
        input="-divc,3.6 -add " + infile1 + " " + infile2,
        output=outfile_p1,
        options="-f nc4 -b F32 -P 8",
    )
    # Previous year
    infile11 = f"{data_folder}/{int(yyyy)-1}/{nvar1}/var{nvar1}.{int(yyyy)-1}.nc"
    infile22 = f"{data_folder}/{int(yyyy)-1}/{nvar2}/var{nvar2}.{int(yyyy)-1}.nc"
    if os.path.exists(infile11) and os.path.exists(infile22):
        log.info(f"Previous year available for variable {var}")
        outfile_p2 = f"{tmp_folder}/{var}.{int(yyyy)-1}.nc"
        cdo.setname(
            var,
            input="-divc,3.6 -add " + infile11 + " " + infile22,
            output=outfile_p2,
            options="-f nc4 -b F32 -P 8",
        )
        cdo.selyear(
            yyyy,
            input="-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,"
            + yyyy
            + "-01-01,00:30:00,1hour -mergetime -seltimestep,8755/8760 "
            + outfile_p2
            + " "
            + outfile_p1,
            output=outfile,
            options="-f nc4 -b F32 -P 8",
        )
    else:
        print("Previous year not available")
        cdo.selyear(
            yyyy,
            input="-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,"
            + yyyy
            + "-01-01,00:30:00,1hour "
            + outfile_p1,
            output=outfile,
            options="-f nc4 -b F32 -P 8",
        )
    shutil.rmtree(tmp_folder)


if var == "sf":
    log.info(f"Processing variable {var}")
    tmp_folder = forcing_folder + "/tmp" + var + yyyy
    outfile = f"{forcing_folder}/inverted/{var}.{yyyy}.nc"
    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)
    # Current year
    nvar1 = "144"
    infile1 = f"{data_folder}/{yyyy}/{nvar1}/var{nvar1}.{yyyy}.nc"
    outfile_p1 = f"{tmp_folder}/{var}.{yyyy}.nc"
    cdo.setname(
        var,
        input="-divc,3.6 " + infile1,
        output=outfile_p1,
        options="-f nc4 -b F32 -P 8",
    )
    # Previous year
    infile11 = f"{data_folder}/{int(yyyy)-1}/{nvar1}/var{nvar1}.{int(yyyy)-1}.nc"
    if os.path.exists(infile11):
        log.info(f"Previous year available for variable {var}")
        outfile_p2 = f"{tmp_folder}/{var}.{int(yyyy)-1}.nc"
        cdo.setname(
            var,
            input="-divc,3.6 " + infile11,
            output=outfile_p2,
            options="-f nc4 -b F32 -P 8",
        )
        cdo.selyear(
            yyyy,
            input="-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,"
            + yyyy
            + "-01-01,00:30:00,1hour -mergetime -seltimestep,8755/8760 "
            + outfile_p2
            + " "
            + outfile_p1,
            output=outfile,
            options="-f nc4 -b F32 -P 8",
        )
    else:
        print("Previous year not available")
        cdo.selyear(
            yyyy,
            input="-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,"
            + yyyy
            + "-01-01,00:30:00,1hour "
            + outfile_p1,
            output=outfile,
            options="-f nc4 -b F32 -P 8",
        )
    shutil.rmtree(tmp_folder)
