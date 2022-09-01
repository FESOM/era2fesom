# Python script that converts variables from era5 to forcing for FESOM2 

# Import modules

import sys
import os
import shutil
import numpy  as np
import xarray as xr

from cdo import *
cdo = Cdo()         # python version of cdo

# Some initial checks

if len(sys.argv) != 3:
	print("Error: check the number of input parameters")
	sys.exit(1)

# Read var and year as strings from input

var  = str(sys.argv[1])
yyyy = str(sys.argv[2])

# List of variables 

var_list = ['q', 'u', 'v', 't2m', 'sp', 'tcc', 'ssrd', 'strd', 'sf', 'rf']

if int(yyyy) > 2020 or int(yyyy) < 1979:
	print('Error: year out of range [1979,2020]')
	sys.exit(1)

if var not in var_list:
	print('Error: inappropriate variable')
	sys.exit(1)	

if var == 'q':
	os.mkdir('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)
	infile1  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, 168, yyyy)
	infile2  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, 134, yyyy)
	tmp1 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/tmp1.nc'
	tmp2 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/tmp2.nc'
	tmp3 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/tmp3.nc' # e
	tmp4 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/tmp4.nc'
	outfile = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/inverted/{}.{}.nc'.format(var, yyyy)
	#dst = xr.open_dataset(infile1)
	#dsp = xr.open_dataset(infile2)
	a1, a3, a4, t0, Rdv, mRdv = 611.21, 17.502, 32.19, 273.16, 0.62198, 0.37802
	cdo.subc(t0, input=infile1, output=tmp1, options='-f nc4 -b F32 -P 8')
	cdo.subc(a4, input=infile1, output=tmp2, options='-f nc4 -b F32 -P 8')
	cdo.mulc(a1, input='-exp -mulc,' + str(a3) + ' -div ' + tmp1 + ' ' + tmp2, output=tmp3, options='-f nc4 -b F32 -P 8')
	cdo.setname(var, input='-invertlat -setreftime,1900-01-01,00:00:00,1day -mulc,' + str(Rdv) + ' -div ' + tmp3 + ' -sub ' + infile2 + ' -mulc,' + str(mRdv) + ' ' + tmp3, output=outfile, options='-f nc4 -b F32 -P 8') 
	shutil.rmtree('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)

if var == 'u':
	nvar = '165'
	oldvar = 'var' + nvar
	infile  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, nvar, yyyy)
	outfile = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/inverted/{}.{}.nc'.format(var, yyyy)
	cdo.setname(var, input='-invertlat -setreftime,1900-01-01,00:00:00,1day ' + infile, output=outfile, options='-f nc4 -b F32 -P 8' )

if var == 'v':
	nvar = '166'
	oldvar = 'var' + nvar
	infile  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, nvar, yyyy)
	outfile = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/inverted/{}.{}.nc'.format(var, yyyy)
	cdo.setname(var, input='-invertlat -setreftime,1900-01-01,00:00:00,1day ' + infile, output=outfile, options='-f nc4 -b F32 -P 8' )

if var == 't2m':
	nvar = '167'
	oldvar = 'var' + nvar
	infile  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, nvar, yyyy)
	outfile = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/inverted/{}.{}.nc'.format(var, yyyy)
	cdo.setname(var, input='-invertlat -setreftime,1900-01-01,00:00:00,1day ' + infile, output=outfile, options='-f nc4 -b F32 -P 8' )

if var == 'sp':
	nvar = '134'
	oldvar = 'var' + nvar
	infile  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, nvar, yyyy)
	outfile = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/inverted/{}.{}.nc'.format(var, yyyy)
	cdo.setname(var, input='-invertlat -setreftime,1900-01-01,00:00:00,1day ' + infile, output=outfile, options='-f nc4 -b F32 -P 8' )

if var == 'ssrd':
	os.mkdir('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)
	# Current year
	nvar1 = '169'
	infile1  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, nvar1, int(yyyy))
	outfile_p1 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/{}.{}.nc'.format(var, int(yyyy))
	cdo.setname(var, input="-divc,3600 " + infile1, output=outfile_p1, options='-f nc4 -b F32 -P 8' )
	# Previous year
	#nvar1 = '169'
	#infile1  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(int(yyyy)-1, nvar1, int(yyyy)-1)
	#outfile_p2 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/{}.{}.nc'.format(var, int(yyyy)-1)
	#cdo.setname(var, input="-divc,3600 " + infile1, output=outfile_p2, options='-f nc4 -b F32 -P 8' )
	# Combining time steps and setting correctly the time axis
	outfile = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/inverted/{}.{}.nc'.format(var, int(yyyy))   
	cdo.selyear(yyyy, input='-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,' + yyyy + '-01-01,00:30:00,1hour ' + outfile_p1, output=outfile, options='-f nc4 -b F32 -P 8' )     
	shutil.rmtree('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)


if var == 'strd':
	os.mkdir('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)
	# Current year
	nvar1 = '175'
	infile1  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, nvar1, int(yyyy))
	outfile_p1 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/{}.{}.nc'.format(var, int(yyyy))
	cdo.setname(var, input="-divc,3600 " + infile1, output=outfile_p1, options='-f nc4 -b F32 -P 8' )
	# Previous year
	#nvar1 = '175'
	#infile1  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(int(yyyy)-1, nvar1, int(yyyy)-1)
	#outfile_p2 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/{}.{}.nc'.format(var, int(yyyy)-1)
	#cdo.setname(var, input="-divc,3600 " + infile1, output=outfile_p2, options='-f nc4 -b F32 -P 8' )
	# Combining time steps and setting correctly the time axis
	outfile = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/inverted/{}.{}.nc'.format(var, int(yyyy))   
	cdo.selyear(yyyy, input='-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,' + yyyy + '-01-01,00:30:00,1hour ' + outfile_p1, output=outfile, options='-f nc4 -b F32 -P 8' )     
	shutil.rmtree('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)


if var == 'rf':
	os.mkdir('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)
	# Current year
	nvar1 = '142'
	infile1  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, nvar1, int(yyyy))
	nvar2 = '143'
	infile2  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, nvar2, int(yyyy))
	outfile_p1 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/{}.{}.nc'.format(var, int(yyyy))
	cdo.setname(var, input="-divc,3.6 -add " + infile1 + " " + infile2, output=outfile_p1, options='-f nc4 -b F32 -P 8' )
	# Previous year
	#nvar1 = '142'
	#infile1  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(int(yyyy)-1, nvar1, int(yyyy)-1)
	#nvar2 = '143'
	#infile2  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(int(yyyy)-1, nvar2, int(yyyy)-1)
	#outfile_p2 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/{}.{}.nc'.format(var, int(yyyy)-1)
	#cdo.setname(var, input="-divc,3.6 -add " + infile1 + " " + infile2, output=outfile_p2, options='-f nc4 -b F32 -P 8' )
	# Combining time steps and setting correctly the time axis
	outfile = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/inverted/{}.{}.nc'.format(var, int(yyyy))   
	cdo.selyear(yyyy, input='-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,' + yyyy + '-01-01,00:30:00,1hour ' + outfile_p1, output=outfile, options='-f nc4 -b F32 -P 8' )     
	shutil.rmtree('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)

if var == 'sf':
	os.mkdir('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)
	# Current year
	nvar1 = '144'
	infile1  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(yyyy, nvar1, int(yyyy))
	outfile_p1 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/{}.{}.nc'.format(var, int(yyyy))
	cdo.setname(var, input="-divc,3.6 " + infile1, output=outfile_p1, options='-f nc4 -b F32 -P 8' )
	# Previous year
	#nvar1 = '144'
	#infile1  = '/mnt/lustre01/work/ba1138/a270099/era5/data/{}/var{}.{}.nc'.format(int(yyyy)-1, nvar1, int(yyyy)-1)
	#outfile_p2 = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy+'/{}.{}.nc'.format(var, int(yyyy)-1)
	#cdo.setname(var, input="-divc,3.6 " + infile1, output=outfile_p2, options='-f nc4 -b F32 -P 8' )
	# Combining time steps and setting correctly the time axis
	outfile = '/mnt/lustre01/work/ba1138/a270099/era5/forcing/inverted/{}.{}.nc'.format(var, int(yyyy))   
	cdo.selyear(yyyy, input='-invertlat -setreftime,1900-01-01,00:00:00,1day -settaxis,' + yyyy + '-01-01,00:30:00,1hour ' + outfile_p1, output=outfile, options='-f nc4 -b F32 -P 8' )     
	shutil.rmtree('/mnt/lustre01/work/ba1138/a270099/era5/forcing/tmp'+var+yyyy)

#ds = xr.open_dataset(infile, chunks={'time': 1})
#ds = ds.rename({oldvar: varprint(ds)
#print(ds)
#ds.to_netcdf(outfile2, encoding={var:{'dtype' : 'f4', 'zlib' : True, 'complevel' : 9}})
