import numpy as np
import pandas as pd
from .config import Configuration
class XarrayDataset:
    def __init__(self, dataset, config):
        self.config = config
        self.dataset = dataset

    def get_array(self):
        return self.dataset[self.config['precipitation variable']].values

    def get_lat(self):
        return self.dataset[self.config['latitude variable']].values

    def get_lon(self):
        return self.dataset[self.config['longitude variable']].values
    
    def get_date(self):
        return self.dataset[self.config['time variable']]
    
    def get_monthly_date(self):
        monthly_prec = self.get_monthly_prec()
        monthly_date = monthly_prec.indexes['time'].to_datetimeindex()
        return monthly_date

    def get_monthly_prec(self):
        # Resample daily precipitation to monthly
        monthly_precip = self.dataset['pr'].resample(time='1M').sum(dim='time')
        return monthly_precip
        
def process_dataset(dataset):
    date = pd.date_range(start='6/1/2000', end='9/1/2021', freq = 'MS')
    class_dataset = XarrayDataset(dataset)
    monthly_precip = class_dataset.get_monthly_prec()
    pass