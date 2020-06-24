'''
some utility functions here
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools


def plot_model_history(values, legend, title, ylabel='Accuracy', xlabel='Epoch', figure_size=(15,7)):
    
    '''
    Plot history values
    
    Parameters
    ----------
    history: python keras traning history
    ylabel&xlabel: labels for figure
    legend: legend labels for figure
    title: title of the figure
    val_label: labels for each data unit stored in the history  
    
    '''
    
    plt.figure(figsize=figure_size)
    
    
    if (type(title)!=str or title==None):
        raise ValueError
        
    if (values==None):
        raise ValueError
        
    if (type(legend)!=list or legend==None):
        raise ValueError
    
    for val_i in values:
        plt.plot(val_i)
        
    plt.title(title)
    
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend(legend, loc='upper left')
    plt.show()
    

def plot_confusion_matrix(cm,
                          classes,
                          xlabel,
                          ylabel,
                          normalize=False,
                          cmap=plt.cm.Blues):
    """
    Plot the given confusion matrix cm as a matrix using and return the
    resulting axes object containing the plot.
    Parameters
    ----------
    cm : ndarray
        Confusion matrix as a 2D numpy.array.
    classes : list of str
        Names of classified classes.
    xlabel : str
    Label of the horizontal axis.
    ylabel : str
    Label of the vertical axis.
    normalize : bool
        If True, the confusion matrix will be normalized. Otherwise, the values
        in the given confusion matrix will be plotted as they are.
    cmap : matplotlib.colormap
        Colormap to use when plotting the confusion matrix.
    Returns
    -------
    fig : matplotlib.figure
        Plot figure.
    ax : matplotlib.Axes
        matplotlib.Axes object with horizontal bar chart plotted.
    References
    ----------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    """
    vmin = None
    vmax = None
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        vmin = 0
        vmax = 1

    plt.figure(figsize=(9, 9))
    cax = plt.imshow(
        cm, interpolation='nearest', vmin=vmin, vmax=vmax, cmap=cmap)
    plt.colorbar(cax)

    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)


    plt.yticks(tick_marks,classes)


    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        cell_str = '{:.2f}'.format(cm[i, j]) if normalize else str(cm[i, j])
        plt.text(
            j,
            i,
            cell_str,
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
  
    plt.show()
    
    
def save_models_history(param_list, models_history, file_path):
    
    '''
    saves model history
    
    Parameters
    ----------
    param_list: params - possible parameters combinations for optimizations
    models_history: stores history values over n-fold of 
                    acc, loss, val_acc, val_loss for each params.
    '''

    data = []

    for i in range(len(models_history)):

        tmp_data=[]
        param_id = np.array(len(models_history[i]['val_accuracy'])*['hidden-{}, act-{}, nod-{}, opt-{}'.format(
              param_list[i]['hidden_layer_size'],
              param_list[i]['activation'],
              param_list[i]['node_size'],
              param_list[i]['optimizer']
              )])

        param_id = np.reshape(param_id, (param_id.shape[0], 1))

        for key in models_history[i].keys():
            tmp_data.append(np.reshape(models_history[i][key], (models_history[i][key].shape[0], 1)))

        history_values=np.hstack((param_id, tmp_data[0], tmp_data[1], tmp_data[2], tmp_data[3]))

        data.extend(history_values)

    # generate labels
    labels= list(models_history[i].keys())
    labels.insert(0, 'id')

    dataframe = pd.DataFrame(np.array(data), columns=labels)
    dataframe.to_csv(file_path, index=False, header=True)