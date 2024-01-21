import numpy as np
import xarray as xr

def load_dataset(path:str):
    """
    Function to load dataset using xarray packages

    Args:
        path: pathh to a dataset
    
    returns: xarray dataset
    """
    dataset = xr.open_dataset(path)
    return dataset