from source.calculate_spi import calculate_spi_matrix
from source.data_processing import XarrayDataset
from source.config import Configuration
from source.data_ingesting import load_dataset
from utils.utils import read_json
from source.prob_drought import calculate_percentage_occurance
from source.calculate_dhi import calculate_dhi
from utils.saving_experiment import save_experiment

def run_experiment():

    #load configuration experiment
    config = read_json("C:/Users/62812/Documents/Kerjaan Meteorologi/SPI/Standard-Precipitation-Index/config.json")
    config_class = Configuration(config)

    #load dataset
    data = load_dataset(config_class.get_path_dataset())
    
    #creata a class dataset
    xr_data = XarrayDataset(data)

    #get monthly_precipitation and its date
    monthly_precip = xr_data.get_monthly_prec().values
    monthly_date = xr_data.get_monthly_date()

    #calculate spi values
    spi_scale = config_class.get_spi_scale()
    spi_result = calculate_spi_matrix(monthly_precip,monthly_date,spi_scale)

    print("Calculating SPI DONE")

    #Calculate Percentage of Occurance
    percentage_occurance = calculate_percentage_occurance(spi_result,spi_scale)

    print("Calculating Percentage of Occurance DONE")

    #calculate DHI
    percentage_occurance_class = config_class.get_percentage_occurance_class()
    dhi = calculate_dhi(percentage_occurance,percentage_occurance_class)

    print("Calculating DHI DONE")

    #Saving Experiment
    save_experiment(config_class = config_class,
                    spi_scale= spi_scale,
                    xr_data = xr_data,
                    spi_result=spi_result,
                    dhi=dhi,
                    percentage_occurance=percentage_occurance)
    print("Saving Experiment DONE")

if __name__ == "__main__":
    run_experiment()