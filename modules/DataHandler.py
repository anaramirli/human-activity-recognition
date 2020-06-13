'''
# HandleData: used for downloading dataset (txt) files and handle the data we get
'''

import os
import numpy as np
from pandas import read_csv

class DataHandler(object):
       
    
    # load a single txt file as a dataframe
    def load_txt(self, filedir):
        '''
        input:
            filedir: file full path
        
        output: returns numpy array
        '''
        data = read_csv(filedir, header=None, delim_whitespace=True)
        return data

    
    # load the files in the parnet dir and stack them together as numpy arrays
    def load_files(self, parentdir=''):
        '''
        input:
            parnetdir: parent directory of the target files
        
        output: returns stacked numpy arrays
        '''
        
        # get the name of files in the parent dir
        filelist = os.listdir(parentdir)
        
        # accumulator: list for stroing loaded lifes
        loadedfiles = []
        
        for file in filelist:
            data = self.load_txt(parentdir + file)
            loadedfiles.append(data)
            
        return np.dstack(loadedfiles)