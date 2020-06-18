'''
this class contains signal transformation between time and frequency domains
and autocorrelation caculations with lagged signal
'''

import numpy as np
from scipy.fftpack import fft
from scipy.signal import welch

class SignalCaculations(object):
    
    
    def __init__(self, N, F, t):
        '''
        @params:
            N: reading size for given window
            F: sampling rate with Hz
            t: size of fixed-width sliding wondow in seconds
            *T: peroid of the signal
            
        '''
        self.N = N
        self.F = F
        self.T = t/N
        

    # perform Fourier Transform
    def fft_transform(self, signal):
        '''    
        input: 
            signal: given signal
        output:
            f_domain: frequency domain of the signal
            FFT: FFT of the signal

        '''
        # create f_domain maunally for given T and N
        f_domain = np.linspace(0, 1/(2*self.T), self.N//2)
        
        # get the hafl of the fft signal as values after half way are redundant
        FFT = 2.0/self.N * np.abs(fft(signal)[0:self.N//2])

        return f_domain, FFT

    # perform Power Spectral Density Transform
    def psd_transform(self, signal):
        '''
        in(out)put description is the same with the previous one
        '''
        f_domain, PSD = welch(signal, self.F)
        return f_domain, PSD
    
    
    # perform autocorrelation, caculates the serial correlation of a signal with its lagged signal
    def aCorr_values(self, signal):
        '''
        in(out)put description is the same with the previous one
        '''
        # calculate time domain manually for gien T and n-th reading
        t_domain = np.array([self.T*reading for reading in range(self.N)])
        
        # "full" mode correlates signals for every t where both have some overlap.
        # autocorrelation is calculated for 0 <= t < ∞, thus for getting corelation
        # at 0 <= t < ∞, we'll get halp of it. 
        aCORR = np.correlate(signal, signal, mode='full')

        return t_domain, aCORR[len(aCORR)//2:]
        
        