import json
import xarray as xr
import os
import logging

def read_json(path):
    with open(path, 'r') as file:
    # Load the JSON data from the file
        data = json.load(file)
    return data

def make_nc2d_lonlat(data,lon,lat,variable,output_name):
    dxr = xr.Dataset(
    {f"{variable}": (["longitude", "latitude"], data)},
    coords={
        "longitude": lon,
        "latitude": lat,
        })
    dxr.to_netcdf("{}.nc".format(output_name))

def make_nc2d_latlon(data,lon,lat,variable,output_name):
    dxr = xr.Dataset(
    {f"{variable}": (["latitude", "longitude"], data)},
    coords={"latitude": lat, 
            "longitude": lon})
    dxr.to_netcdf("{}.nc".format(output_name))
    
def make_nc3D_lonlat(data,time,lon,lat,variable,output_name):
    dxr = xr.Dataset(
    {f"{variable}": (("time","longitude", "latitude"), data)},
    coords={
        "time" : time,
        "longitude": lon,
        "latitude": lat,
        })
    dxr.to_netcdf("{}.nc".format(output_name))

#Funtion to make nc file
def make_nc3D_latlon(data,time,lon,lat,variable,output_name):
    dxr = xr.Dataset(
    {f"{variable}": (("time","latitude", "longitude"), data)},
    coords={
        "time" : time,
        "latitude": lat,
        "longitude": lon,
        })
    print("BERHASILLLLLLLLL")
    dxr.to_netcdf("{}.nc".format(output_name))

def create_folder(path:str, folder_name: str):
    """
    Function to create folder

    Args:
        path: path to folder
        folder_name: name of the folder
    """
    # Create the folder
    fullpath = f"{path}/{folder_name}"
    os.makedirs(fullpath, exist_ok=True)
    logging.info(f"Folder '{folder_name}' created at: {os.path.abspath(path)}")