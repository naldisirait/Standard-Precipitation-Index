#!/usr/bin/env python
# coding: utf-8

# In[46]:


import numpy as np
import pandas as pd
import xarray as xr
from standard_precip import spi
import jenkspy
import json
import warnings
warnings.filterwarnings("ignore")

with open("drought_config.json") as json_file:
    conf = json.load(json_file)
    
path = conf['Directory_Data']
file_name = conf['File_name']

data = xr.open_dataset(path+file_name)

prec_val = data['prec'].values
latitude = data['latitude'].values
longitude = data['longitude'].values
data_time = data.indexes['time'].to_datetimeindex()

spi_scale = conf['spi_scale']
spi_result = {}
for sc in spi_scale: 
    spi_val = np.zeros(prec_val.shape)
    for x in range(spi_val.shape[1]):
        for y in range(spi_val.shape[2]):
            precip_grid = prec_val[:,x,y]
            if np.isnan(np.sum(precip_grid)) != True:
                df_precip = pd.DataFrame({"Date": data_time,"precip":precip_grid})
                spi_prc = spi.SPI()
                spi_grid = spi_prc.calculate(df_precip, 'Date', 'precip', freq = 'M', scale = sc, fit_type ="lmom", dist_type="gam")
                spi_grid_val = spi_grid['precip_scale_{}_calculated_index'.format(sc)].values
                spi_val[:,x,y] = spi_grid_val
            else:
                spi_val[:,x,y] = np.nan
    spi_result[str(sc)] = spi_val
               
def prob_drought(data_spi,skala):
    if skala > 0:
        data_nan = skala - 1
    elif skala == 0:
        data_nan = 0
    spi_val = data_spi[data_nan:,:,:]
    
    shape_1 = spi_val.shape[1]
    shape_2 = spi_val.shape[2]
    
    prob_md = np.zeros((shape_1,shape_2)) # md (moderate drought)
    prob_sd = np.zeros((shape_1,shape_2)) # sd (severe drought)
    prob_vsd = np.zeros((shape_1,shape_2)) # vsd (very severe drought)
    
    for x in range(shape_1):
        for y in range(shape_2):
            if np.isnan(np.sum(spi_val[:,x,y])) != True:
                prob_md[x,y] = 100 * len(np.where((spi_val[:,x,y]<-1) & (spi_val[:,x,y]>-1.49))[0])/len(spi_val)
                prob_sd[x,y] = 100 * len(np.where((spi_val[:,x,y]<-1.5) & (spi_val[:,x,y]>-1.99))[0])/len(spi_val)
                prob_vsd[x,y] = 100 *len(np.where(spi_val[:,x,y]<-2)[0])/len(spi_val)
            else:
                prob_md[x,y] = np.nan
                prob_sd[x,y] = np.nan
                prob_vsd[x,y] = np.nan
    return prob_md,prob_sd,prob_vsd
               
prob_result = {}
for sc in spi_scale:
    prob_md,prob_sd,prob_vsd = prob_drought(spi_result[str(sc)],sc)
    prob_result[str(sc)] = [prob_md,prob_sd,prob_vsd]
    
dhi_spi = {}
for sc in prob_result:
    md_val = prob_result[sc][0]
    sd_val = prob_result[sc][1]
    vsd_val = prob_result[sc][2]

    prob_md = prob_result[sc][0].copy()
    prob_sd = prob_result[sc][1].copy()
    prob_vsd = prob_result[sc][2].copy()
    
    rating_md = jenkspy.jenks_breaks(np.reshape(prob_md,(-1)), nb_class=4)
    rating_sd = jenkspy.jenks_breaks(np.reshape(prob_sd,(-1)), nb_class=4)
    rating_vsd = jenkspy.jenks_breaks(np.reshape(prob_vsd,(-1)), nb_class=4)
    
    prob_md[np.where(md_val<=rating_md[1])] = 1
    prob_md[np.where((md_val > rating_md[1]) & (md_val <= rating_md[2]))] = 2
    prob_md[np.where((md_val > rating_md[2]) & (md_val <= rating_md[3]))] = 3
    prob_md[np.where(md_val>rating_md[3])] = 4
    
    prob_sd[np.where(sd_val<=rating_sd[1])] = 1
    prob_sd[np.where((sd_val > rating_sd[1]) & (sd_val <= rating_sd[2]))] = 2
    prob_sd[np.where((sd_val > rating_sd[2]) & (sd_val <= rating_sd[3]))] = 3
    prob_sd[np.where(sd_val>rating_sd[3])] = 4

    prob_vsd[np.where(vsd_val<=rating_vsd[1])] = 1
    prob_vsd[np.where((vsd_val > rating_vsd[1]) & (vsd_val <= rating_vsd[2]))] = 2
    prob_vsd[np.where((vsd_val > rating_vsd[2]) & (vsd_val <= rating_vsd[3]))] = 3
    prob_vsd[np.where(vsd_val>rating_vsd[3])] = 4
    
    dhi = (prob_md * 1) + (prob_sd * 2) + (prob_vsd * 3)
    dhi_spi[sc] = dhi

def make_nc2d(data,lon,lat,variable,output_name):
    encode = {variable: {"zlib":True, "complevel":9}}
    dxr = xr.Dataset(
    {variable: (("longitude", "latitude"), data)},
    coords={
        "longitude": lon,
        "latitude": lat,
        })
    dxr.to_netcdf("{}.nc".format(output_name),encoding = encode)
    
#Funtion to make nc file
def make_nc3D(data,time,lon,lat,variable,output_name):
    encode = {variable: {"zlib":True, "complevel":9}}
    dxr = xr.Dataset(
    {"{}".format(variable): (("time","longitude", "latitude"), data)},
    coords={
        "time" : time,
        "longitude": lon,
        "latitude": lat,
        })
    dxr.to_netcdf("{}.nc".format(output_name),encoding = encode)
    
for sc in prob_result:
    make_nc3D(spi_result[sc],data_time,longitude,latitude,"spi","SPI {} - {}".format(sc,file_name[:-3]))
    make_nc2d(dhi_spi[sc],longitude,latitude,"dhi","DHI SPI {} - {}".format(sc,file_name[:-3]))
    make_nc2d(prob_result[sc][0],longitude,latitude,"prob","Probability SPI {} MD- {}".format(sc,file_name[:-3]))
    make_nc2d(prob_result[sc][1],longitude,latitude,"prob","Probability SPI {} SD- {}".format(sc,file_name[:-3]))
    make_nc2d(prob_result[sc][2],longitude,latitude,"prob","Probability SPI {} VSD- {}".format(sc,file_name[:-3]))

