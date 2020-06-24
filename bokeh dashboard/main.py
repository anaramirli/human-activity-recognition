# imports 
import pandas as pd
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# import plot utils
from plots.histogram import histogram
from plots.signals import signals
from plots.girdsearch import girdsearch


# Load data 
raw_data = pd.read_csv('data/raw_data_of_a_subject.csv')
gs_data = pd.read_csv('data/nn_param_search.csv')

# create tabs
histogram_tab = histogram(raw_data)
time_series_tab = signals(raw_data)
gird_search_tab = girdsearch(gs_data)

# plot  tabs
tabs = Tabs(tabs = [histogram_tab, time_series_tab, gird_search_tab])
curdoc().add_root(tabs)