#!python3.6

# Created by Chengyu on 2020/6/26
# visualization tools.

import matplotlib.pyplot as plt
import numpy as np

air_force_blue = '#5D8AA8'

def show(values,labels,title='default',a_color='red',dilated=True, figure_size=(8,6)):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    # check length
    if len(values)!=len(labels):
        print('length of values must equal length of labels')
    i = 0
    length = len(values)
    # adjecent label of value 1 will be grouped into the same group
    groups = []
    while i < length:
        if labels[i] == 0:
            i += 1
            continue
        else:
            start = i
            while i<length and labels[i]==1:
                i += 1
            end = i-1
            groups.append([start,end])
    sub1, ax = plt.subplots(figsize=figure_size)
    ax.plot(np.arange(length),values,color=air_force_blue)
    for p in groups:
        ax.plot(np.arange(p[0],p[1]+1),values[p[0]:p[1]+1],color=a_color)
        ax.plot(np.arange(p[0]-1,p[1]+2),values[p[0]-1:p[1]+2],color=a_color)
    ax.set_xlabel('TIME',size='20')
    ax.set_ylabel('KPI VALUE',size='20')
    plt.title(title)
    return sub1