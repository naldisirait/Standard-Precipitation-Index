import numpy as np
import pandas as pd
class Configuration:
    def __init__(self, config):
        self.config = config
    def get_start_date(self):
        return self.config['data_start_date']
    
    def get_end_date(self):
        return self.config['data_end_date']
    
    def get_spi_scale(self):
        return self.config['skala_spi']
    
    def get_path_dataset(self):
        return self.config['path_dataset']
    
    def get_path_shp(self):
        return self.config['path_shp']
    
    def get_percentage_occurance_class(self):
        return self.config['Percentage of Occurance']
    
    def get_experiment_path_result(self):
        return self.config["experiment_result_path"]
    
    def get_experiment_name(self):
        return self.config['experiment_name']
    
    def get_coordinat_order(self):
        return self.config['data_coord_order']