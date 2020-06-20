'''
some feature generation and handling for feature engineering part
'''

import numpy as np
from scipy import stats
from scipy.signal import find_peaks

class FeatureBuilder(object):

    def __init__(self, n_peaks=5):
        '''
        @params:
            n_peaks: number of the first n peaks to be selected from transformation signals
            
        '''
  
        self.n_peaks = n_peaks 
        
    def init_features(self):
        '''
        initialize feature dictionaries
        '''
        
        # variables for given signal itslef
        # this fatures will be calculated on the raw signal itself
        main_features = {
            'std': 0.0, # standart deviation
            'mean': 0.0, # mean vale
            'mad': 0.0, # median absolute deviation
            'max': 0.0, # larget value in array
            'min': 0.0, # smallest value in array
            'iqr': 0.0, # interquartile range
            'correlation-1': 0.0, # correlation
            'correlation-2': 0.0, # correlation
        }

        # varaibles for freq-domain (FFT, PSD) or autocorellation signals
        # we'll create dynamic dictionary for n-peaks
        domain_features = {

        'aCORR':  {'peaks-mean': 0, # mean of the first n selected peaks-value (not domains)
                  'peak-value':{}, # for 2 peak it will be like {'1':0, '2':0} 
                  'peak-domain': {}}, # for 2 peak it will be like {'1':0, '2':0} 

        'PSD':   {'peaks-mean': 0,
                  'peak-value': {},
                  'peak-domain': {}},

        'FFT':   {'peaks-mean': 0,
                  'peak-value': {},
                  'peak-domain':{}}
        }

        # create n-items dict for the first n-peaks values/domains 
        for signal in ['FFT', 'PSD', 'aCORR']:
            temp_dict = {}
            for i_peak in range(self.n_peaks):
                temp_dict[str(i_peak)]=0

            domain_features[signal]['peak-value'] = temp_dict
            domain_features[signal]['peak-domain'] = temp_dict.copy()
            
        # save our featue dictionaries
        self.main_features = main_features
        self.domain_features = domain_features
       
        
    # get domain_features values/ key names 
    def get_main_features(self, return_values=False):
        '''
        convert main_features dict values to list
        
        input:
            return_values: boolen variable - if it's ture then return
                           every single dict values, otherwise return
                           existing feature (key) names
                           
        output: 1D np.array
        '''
        # temporary list
        output = []

        for key, value in self.main_features.items():
            
            # if return_values==true add value, otherwise add name
            if return_values:
                output.append(value)
            else:
                output.append(key)
        
        return output
    
   
   # get domain_features values/ key names
    def get_domain_features(self, return_values=False):
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

        # as we have 3 nested dict for domain_features, first iterate over signals [FFT, PSD, aCORR]
        for signal in self.domain_features.keys():

            # iterate over the second nested dict [max, min, mean, peak-values, peak-domains] 
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
                    # iterate over third nested dict ['0': 0, '1': 0, ...]
                    for peaks, p_val in f_val.items():

                        # if return_values==true add value, otherwise add name
                        if return_values==True:
                            output.append(p_val)
                        else:
                            output.append(signal+'-'+feature+'-'+peaks)

        return output
    
    
    # caculate the features for given ararys
    def calculate_main_features(self, signal, corr_signals):
        '''
        input: 
            signal: signal array for a axis in which caculation is will be done
            corr_signals: list that contains signal arrays for other two axes,
                         these will be used for calculation correlations.
                         
        output: return 1D array
        '''

        # do simple assertation on inputs
        if type(signal)!=np.ndarray or signal.ndim!=1:
            assert False, 'signal must be ndarray type with dimension 1'

        if type(corr_signals)!=list or len(corr_signals)!=2:
            assert False, 'corr_signals must be list with length 2'

            
        # calculate features
        self.main_features['std'] = np.std(signal)
        self.main_features['mean'] = np.mean(signal)
        self.main_features['mad'] = np.median(signal)
        self.main_features['max'] = np.max(signal)
        self.main_features['min'] = np.min(signal)
        self.main_features['iqr'] = stats.iqr(signal)
        self.main_features['correlation-1'] = np.corrcoef(signal, corr_signals[0])[0,1]
        self.main_features['correlation-2'] = np.corrcoef(signal, corr_signals[1])[0,1]


    # caculate the features for given ararys
    def calculate_domain_features(self, domain, signal, t_name=None):

        '''
        input:
            domain: frequency/time domain of the signal
            signal: transformed signal
            t_name: name of signal transformation ('FFT', 'PSD', 'aCORR')
        '''
        # simple assertation for transform_name
        if type(t_name)!=str or t_name.upper() not in ['FFT', 'PSD', 'ACORR']:
            assert False, 'transform_name must be str type and can get one of (FFT, PSD or aCORR)'


        # FIND THE PEAKS FROM TRANSFORMED SIGNAL
        # define required minimum height for determining peaks in the signal.
        QR_5 = np.nanpercentile(signal, 5)
        QR_95 = np.nanpercentile(signal, 95)
        height = QR_5 + (QR_95 - QR_5)/10
        # get peak indices and peaks based on given height
        indices_peaks, peak_values = find_peaks(signal, height=height)

        # CALCULATE/ASSIGN VALUES
        # iterate over peak-value/domain: if first n-peaks exist then assign them, else break
        for i, key in enumerate(self.domain_features[t_name]['peak-value'].keys()):    
                try:
                    self.domain_features[t_name]['peak-value'][key] = signal[indices_peaks[i]]
                    self.domain_features[t_name]['peak-domain'][key] = domain[indices_peaks[i]]
                except:
                    break

        # if found peaks bigger than n_peaks then mean of the first n-peak,
        # else get them what you have at the hand
        if len(indices_peaks) >= self.n_peaks:
            self.domain_features[t_name]['peaks-mean'] = np.mean(peak_values['peak_heights'][:self.n_peaks])
        elif len(indices_peaks)!=0:
            self.domain_features[t_name]['peaks-mean'] = np.mean(peak_values['peak_heights'])