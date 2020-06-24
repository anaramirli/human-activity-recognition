# Human Activity Recognition Using Smartphones Dataset for Customer Behaviour

In this project, we use Fast Fourier, Spectral density, Autocorrelation signal processing techniques along with normal domain feature extraction for predicting human activity recognition with neural networks.

Used Dataset: [PrädBioSys → Customer Behavior](https://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphone)

#### Dir description
1. **UCI HAR Dataset**: Original (PrädBioSys → Customer Behavior ) dataset files. Description of the dataset can be found in README.md. For this project, we don't use ready-to-fit dataset, instead, we carry out feature engineering on raw data and use it.
2. **bokeh dashboard**: Contains bokeh dashboard scripts for raw data and training result visualization. For activating, go into files and run ```bokeh serve --show main.py```.
3. **dataset**: train/test.csv files that we formed doing feature engineering.
4. **modules**: contains classes and utlity fucntions we built.
