import numpy as np

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

def calculate_percentage_occurance(spi_result,spi_scale):
    prob_result = {}
    for sc in spi_scale:
        prob_md,prob_sd,prob_vsd = prob_drought(spi_result[str(sc)],sc)
        prob_drougth_severity = {"moderate" : prob_md, "severe":prob_sd, "very severe":prob_vsd}
        prob_result[str(sc)] = prob_drougth_severity
        
    return prob_result
