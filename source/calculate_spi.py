import numpy as np
import pandas as pd
from standard_precip import spi

def calculate_spi(data, date, scale):
    """
    Function to calculate SPI value

    Args:
        data: vector of monthly precipitation data
        date: monthly date
        scale: integer value (3 or 6 or 9)
    Returns:
        
    """
    df_precip = pd.DataFrame({"Date":date,"precip":data})
    spi_prc = spi.SPI()
    df_spi = spi_prc.calculate(df_precip, 'Date', 'precip', freq = 'M', 
                                 scale = scale, fit_type ="lmom", dist_type="gam")
    spi_val = df_spi['precip_scale_{}_calculated_index'.format(scale)].values
    
    return spi_val

def calculate_spi_matrix(prec_val, date, spi_scale) -> dict:
    spi_result = {}
    for sc in spi_scale: 
        spi_val = np.zeros(prec_val.shape)
        for x in range(spi_val.shape[1]):
            for y in range(spi_val.shape[2]):
                precip_grid = prec_val[:,x,y]
                if np.isnan(np.sum(precip_grid)) != True:
                    spi_val[:,x,y] = calculate_spi(precip_grid,date,sc)
                else:
                    spi_val[:,x,y] = np.nan
        spi_result[str(sc)] = spi_val
    return spi_result
    
