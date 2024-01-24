import numpy as np

def calculate_dhi(prob_result, percentage_occurance_class):
    dhi_spi = {}
    for sc in prob_result:
        md_val = prob_result[sc]['moderate']
        sd_val = prob_result[sc]['severe']
        vsd_val = prob_result[sc]['very severe']

        prob_md = prob_result[sc]['moderate'].copy()
        prob_sd = prob_result[sc]['moderate'].copy()
        prob_vsd = prob_result[sc]['moderate'].copy()
        
        rating_md = percentage_occurance_class["moderate"]
        rating_sd = percentage_occurance_class["severe"]
        rating_vsd = percentage_occurance_class["very severe"]
        
        prob_md[np.where(md_val<= rating_md[0])] = 1
        prob_md[np.where((md_val > rating_md[0]) & (md_val <= rating_md[1]))] = 2
        prob_md[np.where((md_val > rating_md[1]) & (md_val <= rating_md[2]))] = 3
        prob_md[np.where(md_val>rating_md[2])] = 4
        
        prob_sd[np.where(sd_val<=rating_sd[0])] = 1
        prob_sd[np.where((sd_val > rating_sd[0]) & (sd_val <= rating_sd[1]))] = 2
        prob_sd[np.where((sd_val > rating_sd[1]) & (sd_val <= rating_sd[2]))] = 3
        prob_sd[np.where(sd_val>rating_sd[2])] = 4

        prob_vsd[np.where(vsd_val<=rating_vsd[0])] = 1
        prob_vsd[np.where((vsd_val > rating_vsd[0]) & (vsd_val <= rating_vsd[1]))] = 2
        prob_vsd[np.where((vsd_val > rating_vsd[1]) & (vsd_val <= rating_vsd[2]))] = 3
        prob_vsd[np.where(vsd_val>rating_vsd[2])] = 4
        
        dhi = (prob_md * 1) + (prob_sd * 2) + (prob_vsd * 3)
        dhi_spi[sc] = dhi

    return dhi_spi
