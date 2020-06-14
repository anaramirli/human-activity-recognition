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
        
        # accumulator: a list for stroing loaded files
        loadedfiles = []
        
        for file in filelist:
            data = self.load_txt(parentdir + file)
            loadedfiles.append(data)
            
        return np.dstack(loadedfiles)
    
    
    
    def get_subject_data(self, data, subject_indices, subject_id):

        '''
        input:
            data: main dataset
            subject_indices: index map corresponds to the occurrence of each subject in the main dataset
            subject_id: id of the subject we're looking for

        output:
            returns subset of data for a given subect_id (retrive all the occurrences of given id)

        '''

        if len(data)!=len(subject_indices): assert False, \
            ('lengths are not equal: data={}, subject_indices={}'.format(len(data), len(subject_indices)))

        # get indices of the value
        indices = [index for index, s_id in enumerate(np.array(subject_indices)) if s_id==subject_id]
        
        if len(indices)==0: assert False, ('there is no observation for subject {}'.format(subject_id))


        return data[indices]
    
    
    def remove_overlap(self, data, overlap_per=0.5):
        
        '''
        Pre-processed raw data had fixed windows of 2.56 seconds (128 data points) with a 50% overlap.
        For avoiding duplications due to overlapping in plotting or normalization steps, using this 
        function we'll remove overlap and squash data frames it to the series. 
        
        input:
            data: dataset (e.g X_train or X_test)
            overlap_per: overlapping percentage (default is 0.5, as data has an overlap of 50% )
            
        output: squashed NumPy data
        '''
        
        # accumulator: a list for stroing squashed data
        series_data = []

        for frame in data:

            # get the overlap index  
            overlap_index = int(len(frame)* overlap_per) - 1
            # remove the overlap from the data frame
            series_data.append(frame[0:overlap_index])

        return np.concatenate(np.array(series_data))