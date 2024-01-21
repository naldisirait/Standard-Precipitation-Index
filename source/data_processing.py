import numpy as np
import pandas as pd

class XarrayDataset:
    def __init__(self, dataset):
        self.dataset = dataset

    def get_array(self):
        return self.dataset['prec']

    def get_lat(self):
        return self.dataset['latitude']

    def get_lon(self):
        return self.dataset['longitude']
    
    def get_time(self):
        return self.dataset['time']
    
    def get_monthly_prec(self):
        # Resample daily precipitation to monthly
        monthly_precip = self.dataset['prec'].resample(time='1ME').sum(dim='time')
        return monthly_precip
        
def process_dataset(dataset):
    class_dataset = XarrayDataset(dataset)
    monthly_precip = class_dataset.get_monthly_prec()
    pass