import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, Select
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def histogram(raw_data):

    # function that makes dataset for histogram
    # proportion: proporti
    def make_dataset(signals_list, activity, bins = 150):

        # create data frame for plot
        df_histogram = pd.DataFrame(columns=['hist_values', # proportional values
                                           'left', # left bound
                                           'right', # right bound
                                           'bins_interval', # bin interval
                                           'name', # name of histogram
                                           'color']) # color for histogram
        
        colour_count=0
        
        # iterate through different signal types 
        for i, signal in enumerate(signals_list):
            
            # iterate over each axis for a given signal type
            for j, axes in enumerate(['_x', '_y', '_z']):

                # Subset to the carrier
                subset = raw_data[raw_data['activity']==int(activity)][signal+axes]

                # create hist with given bins
                hist_values, hist_edges = np.histogram(subset, bins = bins)

                # divide the counts by the total to get a proportion
                tmp_df = pd.DataFrame({'hist_values': hist_values, 'left': hist_edges[:-1], 'right': hist_edges[1:] })

                # format the interval
                tmp_df['bins_interval'] = ['%d - %d bins' % (left, right) for left, right in zip(tmp_df['left'], tmp_df['right'])]

                # assign labels for histogram
                tmp_df['name'] = signal+axes
                
                # get different color
                tmp_df['color'] = signal_colors[colour_count]

                # add to the overall dataframe
                df_histogram = df_histogram.append(tmp_df)
                
                colour_count+=1
            colour_count+=1

        # sort overall dataframe by names and left bound
        df_histogram = df_histogram.sort_values(['name', 'left'])

        return ColumnDataSource(df_histogram)

    # create plot
    def make_plot(data_source):
        
        # init plot
        plt = figure(plot_width = 700, plot_height = 900, 
                  title = 'Histogram of different signals on each x,y,z-axis for a given activties',
                  x_axis_label = 'signal bins', y_axis_label = 'hist')

        # create histogram
        plt.quad(source = data_source, bottom = 0, top = 'hist_values', left = 'left', right = 'right',
               color = 'color', fill_alpha = 0.6, hover_fill_color = 'color', legend = 'name',
               hover_fill_alpha = 1.0, line_color = 'black')

        # create hover tool
        hover = HoverTool(tooltips=[('signal', '@name'), ('bins', '@bins_interval'), ('hitogram', '@hist_values')],
                          mode='vline')
        plt.add_tools(hover)

        # styling
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

    # plot update if widgebox changes
    def update(attr, old, new):
        
        # get the checked signals names
        new_signals = [signal_selection.labels[i] for i in signal_selection.active]

        
        new_data_source = make_dataset(new_signals,
                               activity=activity_selection.value,
                               bins = bins_select.value)

        data_source.data.update(new_data_source.data)
        
        
    # ---- MAIN ----
        
    # define signals names manually
    available_signals = ['body_acc', 'body_gyro', 'total_acc']
    
    # get unique activites
    available_activity = list(np.unique(raw_data['activity']))
    available_activity = [str(i) for i in available_activity ]

    
    # define colours manually
    signal_colors = Category20_16
    signal_colors.sort()
    
    
    # create selection for activities
    activity_selection = Select(value=available_activity[0], title='Select activity type', options=available_activity)
    activity_selection.on_change('value', update)

    # create checkbox selection for signalss
    signal_selection = CheckboxGroup(labels=available_signals, active = [0])
    signal_selection.on_change('active', update)

    # create slider for bins
    bins_select = Slider(start = 20, end = 200, step = 20, value = 100, title = 'Bins')
    bins_select.on_change('value', update)


    # get initial signals
    initial_signals = [signal_selection.labels[i] for i in signal_selection.active]

    # create data_source for initial signals
    data_source = make_dataset(initial_signals,
                       activity_selection.value,
                       bins = bins_select.value)
    
    # make plot
    plot = make_plot(data_source)

    # put controls widgetbox
    controls = WidgetBox(signal_selection, activity_selection, bins_select)

    # add controls and plot to same row
    layout = row(controls, plot)

    # make a tab with the layout 
    tab = Panel(child=layout, title = 'Raw Data-Histogram')
    
    return tab