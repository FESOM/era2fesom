#!/bin/bash

#SBATCH --job-name=ERA
#SBATCH -p compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --time=08:00:00
#SBATCH -o slurm-out.out
#SBATCH -e slurm-err.out
#SBATCH -A ab0995

# -------------------------------------------------------------------------
#
# Bash script that converts the era5 data to the right units
# So that FESOM2 or other ocen models can use it as forcing field
#
# Author: Lorenzo Zampieri (lorenzo.zampieri@awi.de)
# Date:   07/04/2020
#
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
#
# Definition section
#

# Years to be processed
# declare -a   year_array=("1950")
# declare -a   year_array=("1951" "1952" "1953" "1954" "1955")
declare -a   year_array=("2022")
#declare -a   year_array=("2010" "2011" "2012" "2013" "2014" "2015" "2016" "2017" "2018" "2019" "2020")

# Variable names
declare -a    var_array=("134" "142" "143" "144" \ 
                        "164" "165" "166" "167" \
                        "168" "169" "175" "205")
# declare -a    var_array=("211")

declare -a    frc_array=("t2m" "q" "u" "v" "sp" "sf" "rf" "ssrd" "strd")
# declare -a    frc_array=("rf")

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
#
# Loop section
#

#mkdir -p ${out_dir}

count=0
for var in ${frc_array[@]}; do
    echo " ---- Processing variable "${var_array[count]}" ---- "
    echo " ----                         ---- "
    for year in ${year_array[@]}; do
        echo " -- Processing year "$year
        python processing_era5.py $var $year
    done
    count=$((count + 1))
done



