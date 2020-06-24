import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import Select
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def girdsearch(raw_data):
    
    # create dataset
    def make_dataset(param, history_type):
        
        # list for storing selected signals data
        x = []
        y = []
        colors = []
        labels = []

        
        # get subset
        subset = raw_data[raw_data['id']==param]

        # if h_t==1, then get accuracy else get loss values
        if history_type==1:
            # add acc
            y.append(list(subset['accuracy']))
            y.append(list(subset['val_accuracy']))
            # add lables
            labels.append('acc')
            labels.append('val_acc')
            
        elif history_type==2:
            # add loss
            y.append(list(subset['loss']))
            y.append(list(subset['val_loss']))
            # add labels
            labels.append('loss')
            labels.append('val_loss')
            

        # add x-values
        x.append(list(np.arange(len(subset))))
        x.append(list(np.arange(len(subset))))

        # add the colors
        colors.append(param_colors[1])
        colors.append(param_colors[6])

        # create new data course
        new_data_source = ColumnDataSource(data={'x': x, 'y': y, 
                                   'color': colors, 'label': labels})

        return new_data_source
    
    
    # create plot
    def make_plot(data_source, title):
        
        # init plot
        plt = figure(plot_width = 900, plot_height = 400,
                   title = title,
                   x_axis_label = 'epoch', y_axis_label = '')

        # add m-lines
        plt.multi_line('x', 'y',  color = 'color', legend = 'label', 
                     line_width = 3,
                     source = data_source)


        # create hoover tool
        hover = HoverTool(tooltips=[('signal', '@label'), ('epoch', '$x'), ('values', '$y')], line_policy = 'next')
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
        
        # get the value of selection
        new_param_name = param_selection.value
        
        # get data for updated list
        new_data_source = make_dataset(new_param_name, history_type=1)
        new_data_source2 = make_dataset(new_param_name, history_type=2)

        # update data and plot new data soruce
        data_source.data.update(new_data_source.data)
        data_source2.data.update(new_data_source2.data)
        
        
    # ---- MAIN ----

    # get unique param combinations
    available_params = list(np.unique(raw_data['id']))
    
    param_colors = Category20_16
    param_colors.sort()

    # create selection menu for given available_params and set on change
    param_selection =  Select(value=available_params[0], title='Gird-search params', options=available_params)
    param_selection.on_change('value', update)

    # initial selected data source to plot 
    initial_params = param_selection.value
    
    # create data scources for plot 1 and 2
    data_source = make_dataset(initial_params, history_type=1)
    data_source2 = make_dataset(initial_params, history_type=2)
    
    # plot 1 and 2
    plot = make_plot(data_source, title='Train and 10-fold validation accuracy')
    plot2 = make_plot(data_source2, title='Train and 10-fold validation loss')

    # add style to the plots
    plot = style(plot)
    plot2 = style(plot2)

    # put controls in a single element
    controls = WidgetBox(param_selection)
    
    # create row layout for controller and plot
    layout = column(controls, plot, plot2)
 
    # add layout to the tab
    tab = Panel(child=layout, title = 'Gird-Search History')

    return tab