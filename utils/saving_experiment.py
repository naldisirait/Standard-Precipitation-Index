import numpy as np
import pandas as pd
import xarray as xr
from .utils import make_nc2d_latlon, make_nc2d_lonlat, make_nc3D_latlon, make_nc3D_lonlat, create_folder

def save_experiment(config_class, spi_scale, xr_data, spi_result, dhi, percentage_occurance):
    path_result = config_class.get_experiment_path_result()
    monthly_date = xr_data.get_monthly_date()
    latitude = xr_data.get_lat()
    longitude = xr_data.get_lon()
    exp_name = config_class.get_experiment_name()
    data_coor_order = config_class.get_coordinat_order()

    if data_coor_order =="lonlat":
        make_nc2d = make_nc2d_lonlat
        make_nc3d = make_nc3D_lonlat
    else:
        make_nc2d = make_nc2d_latlon
        make_nc3d = make_nc3D_latlon

    create_folder(path_result,exp_name)

    for sc in spi_scale:
        sc = str(sc)

        #save spi results
        make_nc3D_latlon(data = spi_result[sc],time = monthly_date,
                         lat = latitude,lon = longitude,variable = "spi",
                         output_name = f"{path_result}/{exp_name}/SPI {sc}")

        #save dhi results
        make_nc2d_latlon(data = dhi[sc], 
                  lon = longitude,
                  lat = latitude,
                  variable= "dhi", 
                  output_name= f"{path_result}/{exp_name}/DHI SPI {sc}")
        
        #save probability results
        make_nc2d_latlon(data = percentage_occurance[sc]["moderate"],
                  lon = longitude,
                  lat = latitude,
                  variable= "prob",
                  output_name=f"{path_result}/{exp_name}/Probability SPI {sc} MD")
        
        make_nc2d_latlon(data=percentage_occurance[sc]["severe"],
                  lon=longitude,
                  lat=latitude,
                  variable="prob",
                  output_name=f"{path_result}/{exp_name}/Probability SPI {sc} SD")
        
        make_nc2d_latlon(data=percentage_occurance[sc]["very severe"],
                  lon = longitude,
                  lat = latitude,
                  variable="prob",
                  output_name=f"{path_result}/{exp_name}/Probability SPI {sc} VSD")
