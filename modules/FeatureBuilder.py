import numpy as np


'''
some feature generation and handling for feature engineering part
'''

class FeatureBuilder(object):
    
    
    
    def __init__(self, n_peaks=5):
        
        
        '''
        @params:
            n_peaks: number of first n peaks that'll selected from transformation signals
            
        '''
        
        self.n_peaks = n_peaks 
        
    def init_features(self):
    
        '''
        initialize feature dictionaries
        '''
    
        # set of variables for given signal itslef
        # this fatures will be calculated on the raw signal itself
        main_features = {

            'mean': 0.0, # mean vale
            'std': 0.0, # standart deviation
            'mad': 0.0, # median absolute deviation
            'max': 0.0, # larget value in array
            'min': 0.0, # smallest value in array
            'iqr': 0.0, # interquartile range
            'entropy': 0.0, # entropy of signal
            'correlation-1': 0.0, # correlation
            'correlation-2': 0.0, # correlation
        }

        # set of varaibles for freq-domain (FFT, PSD) or autocorellation signals
        '''
        For each transformation, we'll look at the first n peaks in the signal. 
        We're not only the interested in the amplitude of these peaks happened 
        also where/when this peaks happened in the t/f-domains. Thus we'll not only
        take first n peaks of transformations but also their t/f-domains.

        Thus, we'll create dynamic dic for n-peaks
        '''
        domain_features = {

        'FFT':   {'min': 0, # smallest peak
                  'max': 0, # largest peak
                  'mean': 0, # mean of the peaks
                  'peak-values':{}, # for 2 peak it will be like {'1':0, '2':0} 
                  'peak-domains': {}}, # for 2 peak it will be like {'1':0, '2':0} 

        'PSD':   {'min': 0,
                  'max': 0,
                  'mean': 0,
                  'peak-values': {},
                  'peak-domains': {}},

        'aCORR': {'min': 0,
                  'max': 0,
                  'mean': 0,
                  'peak-values': {},
                  'peak-domains':{}}
        }

        # create n-items dict for n-peaks values/domains 
        for signal in ['FFT', 'PSD', 'aCORR']:

            temp_dict = {}

            for i_peak in range(self.n_peaks):
                temp_dict[str(i_peak)]=0

            domain_features[signal]['peak-values'] = temp_dict
            domain_features[signal]['peak-domains'] = temp_dict.copy()

            
        # save our featue dicts
        self.main_features = main_features
        self.domain_features = domain_features
        
        
        
        
        
    # get domain_features values/ key names 
    def get_main_features(self):
        '''
        convert main_features dict values to list
        
        input:
            return_values: boolen variable - if it's ture then return
                           every single dict values, otherwise return
                           existing feature (key) names
                           
        output: 1D np.array
        '''
        output = []

        for key, value in self.main_features.items():
            
            # if return_values==true add value, otherwise add name
            if return_values:
                output.append(value)
            else:
                output.append(key)
            
                
        return np.array(output)
    
   
   # get domain_features values/ key names
    def get_domain_features(self, return_values=True):

        '''
        it runs over the dict and get's the required info.
        convert domain_features dict values and keys to list

        input:
            return_values: boolen variable - if it's ture then return
                           every single dict values, otherwise return
                           existing feature (key) names

        output: 1D np.array
        '''

        # temporary list
        output = []

        # we have 3-d dict, first iterate over signal names [FFT, PSD, aCORR]
        for signal in self.domain_features.keys():

            # itterate over the first nested dict [max, min, mean, peak-values, peak-domains] 
            for feature, f_val in self.domain_features[signal].items():

                # chekc if the value of the first nested dict is itself a dict.
                # if yes, then that means it contains the second nested dict 
                if type(f_val)!=dict:

                    # if return_values==true add value, otherwise add name
                    if return_values==True:
                        output.append(f_val)
                    else:
                        output.append(signal+'-'+feature)

                else:
                    # iterate over second nested dict ['0': 0, '1': 0, ...]
                    for peaks, p_val in f_val.items():

                        # if return_values==true add value, otherwise add name
                        if return_values==True:
                            output.append(p_val)
                        else:
                            output.append(signal+'-'+feature+'-'+peaks)


        return np.array(output)