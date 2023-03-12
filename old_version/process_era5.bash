#!/bin/bash
#SBATCH --job-name=ERA5_proc
#SBATCH -p compute
#SBATCH --ntasks-per-node=128
#SBATCH --nodes=1
#SBATCH --switches=1
#SBATCH --time=08:00:00
#SBATCH -o slurm-out-sf12.out
#SBATCH -e slurm-err-sf12.out
#SBATCH -A ab0995

# -------------------------------------------------------------------------
#
# Bash script that converts the ERA5 reanalysis from GRIB2 to netCDF
# So that FESOM2 or other ocen models can use it as forcing field
# 
# At the moment, different branches at DKRZ (sf00, sf12, etc.) 
# must be processed separately 
#
# Author: Lorenzo Zampieri (lorenzo.zampieri@awi.de) 
# Date:   02/04/2020
#
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
#
# Definition section
#

# Variable names
# declare -a    var_array=("211")
declare -a    var_array=("142" "143" "144" "169" "175" "205") 
#declare -a    var_array=("134" "164" "165" "166" "167" "168")

# ERA5 branch where to find the variable (must have the same size as var_array)
# declare -a branch_array=("sf12")
declare -a branch_array=("sf12" "sf12" "sf12" "sf12" "sf12" "sf12")
#declare -a branch_array=("sf00" "sf00" "sf00" "sf00" "sf00" "sf00")

# Years to be processed 
#declare -a   year_array=(                                                        "1979" "1980" \
#                         "1981" "1982" "1983" "1984" "1985" "1986" "1987" "1988" "1989" "1990" \
#                         "1991" "1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" \
#                         "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009" "2010" \
#                         "2011" "2012" "2013" "2014" "2015" "2016" "2017" "2018" "2019"        )
#declare -a   year_array=(                                                                "2010" \
#                          "2011" "2012" "2013" "2014" "2015" "2016" "2017" "2018" "2019" "2020" )
declare -a   year_array=("2021")
# Months to be preocessed
declare -a  month_array=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12")

# Data frequency (01 = houly for sf12; 1H = hourly for sf00; MM = monthly)
data_freq="01" 

# ERA5 folder
in_dir="/pool/data/ERA5/"

# Folder for storing processed data
out_dir="/pool/data/AWICM/FESOM2/FORCING/era5/data/" 

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
#
# Loop section
#

count=0
# For each variable
for var in ${var_array[@]}; do
    echo " --- Processing variable "${var_array[count]}
    echo " --- from branch "${branch_array[count]}
    # For each year
    for year in ${year_array[@]}; do
        # Create and move to the right target directory
        mkdir -p $out_dir"/"$year"/tmp"
        cd $out_dir"/"$year"/tmp" 
        # For each month
        for month in ${month_array[@]}; do
            grib=${in_dir}${branch_array[count]}"_"${data_freq}"/"$year"/E5"${branch_array[count]}"_"${data_freq}"_"$year"-"$month"_"$var
            echo " <- Input file:  "$grib
            ncdf="var"$var"."$year$month".nc"
            echo " -> Output file: "${out_dir}$year"/tmp/"$ncdf
            # cdo part
            if [ ! -f ${out_dir}$year"/tmp/"$ncdf ] && [ ! -f ${out_dir}$year"/var"$var"."$year".nc" ]; then # Do not overwrite
                cdo -P 8 -O -f nc setgridtype,regular $grib $ncdf
            fi
        done
        if [ ! -f ${out_dir}$year"/var"$var"."$year".nc" ]; then # Do not overwrite
            cdo -P 8 -O mergetime ${out_dir}$year"/tmp/""var"$var"."$year"*.nc" ${out_dir}$year"/var"$var"."$year".nc"
        fi
        # Remove monthly files
        rm -r ${out_dir}$year"/tmp/""var"$var"."$year"*.nc"
    done
    count=$((count + 1))
done

# -------------------------------------------------------------------------
