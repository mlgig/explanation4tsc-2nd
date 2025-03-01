import numpy as np
import random
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn import preprocessing
from scipy.interpolate import interp1d


def get_random_color(n):
    ans = []
    random.seed(1)
    for j in range(n):
        rand_color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        ans.append(rand_color)
    return ans


def visualize_class_ts(X,y):
    X = np.squeeze(X)
    class_name = list(np.unique(y))
    num_class = len(class_name)
    color_list = get_random_color(num_class)
    index_dict = defaultdict(list)
    for i,y0 in enumerate(y):
        index_dict[y0].append(i)
    
    
    for class_,color in zip(class_name,color_list):
        for j in range(X.shape[0]):
            if j in index_dict[class_]:
                plt.plot(X[j,:],color=color)
                plt.title("Class %d sample" %(class_))
        plt.show()    
    

def visualize_explanation(idx, X_series, explanation,ds, savefig=False):
    """Visualize one time series with explanation by a heatmap
    Args:
        idx: Index of the example to produce heatmap (0-indexed)
        X_series: the X_series that needs to visualize (2d array)
        explanation: coressponding explanation weights for the X_series
        ds: the name of the dataset to explain (for annotation purpose only)

    Return: a plot of heatmap explanation for an example index in a given dataset
    """
    def transform(X):
        ma,mi = np.max(X), np.min(X)
        X = (X - mi)/(ma-mi)
        return X*100
    weight = abs(explanation[idx])
    weight = transform(weight)
    ts = np.squeeze(X_series[idx])
        
    max_length1, max_length2 = len(ts),10000 #
    x1 = np.linspace(0,max_length1,num = max_length1)
    x2 = np.linspace(0,max_length1,num = max_length2)
    y1 = ts
    
    f = interp1d(x1, y1) # interpolate time series
    fcas = interp1d(x1, weight) # interpolate weight color
    weight = fcas(x2) # convert vector of original weight vector to new weight vector

    plt.scatter(x2,f(x2), c = weight, cmap = 'jet', marker='.', s= 1,vmin=0,vmax = 100)
    # plt.xlabel('Explanation for index %d, dataset %s' %(idx, ds))
    cbar = plt.colorbar(orientation = 'vertical')
    
    if savefig:
        plt.savefig('temp.pdf',format='pdf',dpi=300)
    else: plt.show()


def visualize_single_explanation(x, w, savefig=False):
    """Visualize one time series with explanation by a heatmap
    Args:
        idx: Index of the example to produce heatmap (0-indexed)
        X_series: the X_series that needs to visualize (2d array)
        explanation: coressponding explanation weights for the X_series
        ds: the name of the dataset to explain (for annotation purpose only)

    Return: a plot of heatmap explanation for an example index in a given dataset
    """
    def transform(X):
        ma,mi = np.max(X), np.min(X)
        X = (X - mi)/(ma-mi)
        return X*100
    weight = abs(w)
    weight = transform(weight)
    # z = np.histogram(weight)
    plt.hist(weight, bins = [0,20,40,60,80,100]) 
    plt.title("histogram") 
    plt.show()
    ts = np.squeeze(x)
        
    max_length1, max_length2 = len(ts),10000 #
    x1 = np.linspace(0,max_length1,num = max_length1)
    x2 = np.linspace(0,max_length1,num = max_length2)
    y1 = ts
    
    f = interp1d(x1, y1) # interpolate time series
    fcas = interp1d(x1, weight) # interpolate weight color
    weight = fcas(x2) # convert vector of original weight vector to new weight vector

    plt.scatter(x2,f(x2), c = weight, cmap = 'jet', marker='.', s= 1,vmin=0,vmax = 100)
    # plt.xlabel('Explanation for index %d, dataset %s' %(idx, ds))
    cbar = plt.colorbar(orientation = 'vertical')
    
    if savefig:
        plt.savefig('temp.pdf',format='pdf',dpi=300)
    else: plt.show()


def visualize_experiment_result(df, fsize=15, padsize=15, legendsize=8,savefig=False,savepath='./plot/temp'):
    referees = list(set(df['Referee']))
    xais = list(set(df['XAI_method']))
    datasets = list(set(df['dataset']))
    color = get_random_color(len(xais))
    marker = ['v', 'o', 'd','v','o','d']
    nr,nc = len(datasets),len(referees)
    x = np.arange(0,101,10)

    if nr==1 and nc==1: # one XAI, one dataset --> single figure
        fig = plt.figure(figsize=(6,4))
        ref= referees[0]
        dataset=datasets[0]
        print(ref)
        for xai,c,m in zip(xais,color,marker):
            y = df[(df['Referee'] == ref) & 
                                  (df['XAI_method'] == xai) & 
                                  (df['dataset'] == dataset)]['metrics: acc']
            plt.plot(x,y, color=c, marker=m)
            plt.title('Referee: %s' %ref.upper(), fontsize=fsize)
            plt.xlabel('Noise Level in Percentage')
            plt.ylabel('Dataset: %s' %dataset, fontsize=fsize, labelpad=padsize)
            plt.legend(xais, loc='upper right', fontsize=legendsize)
        plt.show()
    
    else:
        fig, axes = plt.subplots(nrows=nr, ncols=nc, sharex=True, sharey=True, figsize=(4*nc,4*nr))
        for i, dataset in enumerate(datasets):
            for j, ref in enumerate(referees):
                for xai,c,m in zip(xais,color,marker):
                    y = df[(df['Referee'] == ref) & 
                                      (df['XAI_method'] == xai) & 
                                      (df['dataset'] == dataset)]['metrics: acc']
                    if   nr==1: # ONE dataset only --> one row of XAIs
                        axes[j].plot(x,y, color=c, marker = m)
                        axes[j].set_title('Referee: %s' %ref.upper(), fontsize=fsize, pad=padsize)
                        axes[j].set_xlabel('Noise Level in Percentage')
                        if j==0: 
                            axes[j].set_ylabel('Dataset: %s' %dataset, fontsize=fsize, labelpad=padsize)
                            axes[j].legend(xais, loc='upper right', fontsize=legendsize)

                    elif nc==1: # ONE referee only --> one column of datasets
                        axes[i].plot(x,y, color=c, marker = m)
                        axes[i].set_ylabel('Dataset: %s' %dataset, fontsize=fsize, labelpad=padsize)
                        if i==0: 
                            axes[i].set_title('Referee: %s' %ref.upper(), fontsize=fsize, pad=padsize)
                            axes[i].legend(xais, loc='upper right', fontsize=legendsize)
                        if i == len(datasets)-1:
                            axes[i].set_xlabel('Noise Level in Percentage')

                    else:
                        axes[i,j].plot(x,y, color=c, marker = m)
                        if i==0: axes[i,j].set_title('Referee: %s' %ref.upper(), fontsize=fsize, pad=padsize) 
                        if j==0: 
                            axes[i,j].set_ylabel('Dataset: %s' %dataset, fontsize=fsize, labelpad=padsize)
                            axes[i,j].legend(xais, loc='upper right', fontsize=legendsize)
                        if i == len(datasets)-1:
                            axes[i,j].set_xlabel('Noise Level in Percentage')
    
        plt.tight_layout()
  
        if savefig:
            plt.savefig(savepath+'.png',bbox_inches='tight', pad_inches=0)
