# Human Activity Recognition Using Smartphones Dataset for Customer Behaviour (multivariate time-series classification)

This project concerns multivariate time-series classification for human activity recognition. Target activities are compromised of 'Walking', 'Upstairs', 'Downstairs', 'Sitting', 'Standing', 'Lying'. 

Here we implement Fast Fourier, Spectral density, Autocorrelation signal processing techniques on raw activity signals for additional feature extraction. Then utilizing both transformed and normal signals, we classify activities using conventional Multilayer Perceptron and LSTM. 

Used Dataset: [Human Activity Recognition Using Smartphone](https://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones)

#### Dir description
1. **UCI HAR Dataset**: Original (PrädBioSys → Customer Behavior ) dataset files. Description of the dataset can be found in README.md. For this project, we don't use ready-to-fit dataset, instead, we carry out feature engineering on raw data and use it.
2. **bokeh dashboard**: Contains bokeh dashboard scripts for raw data and training result visualization. For activating, go into the directory and run ```bokeh serve --show main.py``` in command prompt.

    ```
    +-- data
    |   +-- nn_param_search.csv 
    |   +-- raw_daa_of_a_subject 
    +-- plots
    |   +-- gridsearch.py
    |   +-- histogram.py 
    |   +-- signals.py
    +--- main.py
    ``` 
    - ```nn_param_search.csv```: history of of acc, val_acc, loss, val_loss results for grid-search on normal nn model wtk 10-fold validaation.
    - ```raw_data_of_a_sbuject.csv```: raw data without overlaps for a given subject, contains 9 different signals
    - ```gridsearch.py```: visualises grid-search results
    - ```histogram.py```: visualises raw signals as time series
    - ```signals.py```: visualises histogram for raw signals upon each activity
    - ```main.py```: the main file to run bokeh dashboard
3. **dataset**: has train/test.csv files that we formed doing feature engineering.
4. **modules**: contains our classes and utlity functions.
    - ```DataHandler.py```: used for downloading raw dataset (txt) files and handle the data we get
    - ```FeatureBuilder.py```: used in feature generation for feature engineering part, contains methods to handle feature list/values and caculation them.
    - ```SignalTransforms.py```: contains implementaion of signal transformation between time and frequency domains and autocorrelation caculations with lagged signal.
    - ```utils.py```: has some utulity functions such as figure ploting.
