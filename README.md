# Human Activity Recognition Using Smartphones Dataset for Customer Behaviour

In this project, we use Fast Fourier, Spectral density, Autocorrelation signal processing techniques along with normal domain feature extraction for predicting human activity recognition with neural networks.

Used Dataset: [PrädBioSys → Customer Behavior](https://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphone)

#### Dir description
1. **UCI HAR Dataset**: Original (PrädBioSys → Customer Behavior ) dataset files. Description of the dataset can be found in README.md. For this project, we don't use ready-to-fit dataset, instead, we carry out feature engineering on raw data and use it.
2. **bokeh dashboard**: Contains bokeh dashboard scripts for raw data and training result visualization. For activating, go into the directory and run ```bokeh serve --show main.py``` in command prompt.

    ```
    +-- data
    |   +-- nn_param_search.csv 
    |   +-- raw_daa_of_a_subject 
    +-- plots
    |   +-- gridsearch.py (histogram of )
    |   +-- histogram.py 
    |	+-- signals.py
    +--- main.py
    ``` 
    - ```nn_param_search.csv```: history results of acc, val_acc, loss, val_loss for grid-search on normal nn model
    - ```raw_data_of_a_sbuject```: raw data without overlaps for a given subject, contains 9 different signals
    - ```gridsearch.py```: for visualises grid-search results
    - ```histogram.py```: visualises raw signals as time series
    - ```signals.py```: visualises histogram for raw signals upon each activity
    - ```main.py```: the main file to run bokeh visualization
3. **dataset**: has train/test.csv files that we formed doing feature engineering.
4. **modules**: contains our classes and utlity functions.
    - ```DataHandler.py```: used for downloading dataset (txt) files and handle the data we get
    - ```FeatureBuilder.py```: used in feature generation in for feature engineering part, contains methods to handle feature list/values and caculation them.
    - ```SignalTransforms.py```: contains implementaion of signal transformation between time and frequency domains and autocorrelation caculations with lagged signal.
    - ```utils.py```: has some utulity functions such as figure ploting.
