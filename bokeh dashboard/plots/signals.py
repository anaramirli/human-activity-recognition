import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def signals(raw_data):
    
    # create dataset
    def make_dataset(signal_list):
        
        # get signal names and activities
        if not not signal_list:
            signal_list.insert(0, 'activity')

        # list for storing selected signals data
        x = []
        y = []
        colors = []
        labels = []

        # iterate through signals
        for i, signal in enumerate(signal_list):
            
            # get subset
            subset = raw_data[signal]
            
            # substract -9 from original values of activity
            # don't overlap it with signals values
            if signal=='activity':
                subset=subset-9

            
            # add the values/color/label
            y.append(list(subset))
            x.append(list(np.arange(len(subset))))
            colors.append(signal_colors[i])
            labels.append(signal)

            
        # create new data source
        new_data_source = ColumnDataSource(data={'x': x, 'y': y, 
                                   'color': colors, 'label': labels})

        return new_data_source
    
    
    # create plot 
    def make_plot(data_source):
        
        # init plot
        plt = figure(plot_width = 900, plot_height = 400,
                   title = 'Time series of different signals for a subject',
                   x_axis_label = 'f/t domain', y_axis_label = '')

        # add m-lines
        plt.multi_line('x', 'y',  color = 'color', legend = 'label', 
                     line_width = 3, source = data_source)


        # create hoover tools
        hover = HoverTool(tooltips=[('signal', '@label'), ('f/t domain', '$x'), ('values', '$y')], line_policy = 'next')
        plt.add_tools(hover)

        # do styling
        plt = style(plt)

        return plt
    
    
    # style plot
    def style(plt):
        
        # title 
        plt.title.align = 'center'
        plt.title.text_font_size = '20pt'

        # axis titles
        plt.xaxis.axis_label_text_font_size = '14pt'
        plt.xaxis.axis_label_text_font_style = 'bold'
        plt.yaxis.axis_label_text_font_size = '14pt'
        plt.yaxis.axis_label_text_font_style = 'bold'

        return plt
    
    
    # update plot if widgebox changes
    def update(attr, old, new):
        
        
        # get signals names from selector
        new_signals = [signal_selection.labels[i] for i in signal_selection.active]

        # get data for updated list
        new_data_source = make_dataset(new_signals)

        # update data and plot new data soruce
        data_source.data.update(new_data_source.data)
        

    # ---- MAIN ----
        
    # get unique signal names
    available_signals = list(raw_data.columns[1:])
    available_signals.sort()
    
    signal_colors = Category20_16
    signal_colors.sort()

    # create checkbox for signal names
    signal_selection = CheckboxGroup(labels=available_signals, active = [0])
    signal_selection.on_change('active', update)

    # initial selected data source
    initial_signals = [signal_selection.labels[i] for 
                        i in signal_selection.active]    
    
    # create data source
    data_source = make_dataset(initial_signals) 

    # plot aand style
    plot = make_plot(data_source)
    plot = style(plot)

    # place control in widgetbox
    controls = WidgetBox(signal_selection)
    
    # create row layout for controller and plot
    layout = row(controls, plot)
 
    # add layout to the tab
    tab = Panel(child=layout, title = 'Raw Data - Time Series Plot')

    return tab