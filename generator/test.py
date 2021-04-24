#!python3.6

# Created by Chengyu on 2020/5/13.
# season generator.

import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import mean_squared_error

def sine_p(size):
    # print(np.pi/np.arange(len))
    # print(np.linspace(10,100,91))
    return np.sin(np.linspace(0,np.pi,size))

def sine(size):
    return np.sin(np.linspace(0,2*np.pi,size))

# std_size is the standard size of a cycle.
# cycle_num is the number of cycles.
# The overall length of returned seasonal component is
# std_size * cycle_number, in the absense of drift.
# drift_a, drift_f are drift factors of amplitude and
# frequency, respectively.
def sine_p_season(std_size, cycle_num, drift_a, drift_f):
    sines = [sine_p(std_size) for x in range(cycle_num)]
    return np.concatenate(sines)

def sine_season(std_size, cycle_num, drift_a, drift_f):
    sines = sine(std_size)
    sines = [sine(std_size)[1:] for x in range(cycle_num)]
    return np.concatenate(sines)

# length of line (p1,p2)
# p = [x,y]
def length(p1,p2):
    # 2-norm
    return np.linalg.norm(p1-p2)

# mid of line(p1,p2)
def mid(p1,p2):
    x = (p2[0]+p1[0])/2
    y = (p2[1]+p1[1])/2
    return np.array([x,y])

def std():
    point_list = list(map(lambda x:x[2],expression))
    # print(point_list)
    y_value_list = list(map(lambda x:x[1], point_list))
    max_y = np.max(y_value_list)
    min_y = np.min(y_value_list)
    height = max_y-min_y
    for i in range(len(expression)):
        expression[i][2][1]=expression[i][2][1]/height

def std10():
    point_list = list(map(lambda x:x[2],expression_[10]))
    # print(point_list)
    y_value_list = list(map(lambda x:x[1], point_list))
    max_y = np.max(y_value_list)
    min_y = np.min(y_value_list)
    height = max_y-min_y
    for i in range(len(expression_[10])):
        expression_[10][i][2][1]=expression_[10][i][2][1]/height

# plot curve of depth d
# d start from 0
def func_of_d(x,depth):
    expression = expression_[depth]
    for e in expression:
        if x>=e[0][0] and x<=e[0][1]:
            p1 = e[1]
            p2 = e[2]
            k = (p2[1]-p1[1])/(p2[0]-p1[0])
            b = p1[1]-k*p1[0]
            return k*x+b

expression_ = [[],[],[],[],[],[],[],[],[],[],[]]

# RMDF loop version.
def RMDF_loop(H,sigma,max_depth):
    start = np.array([0,0])
    end = np.array([1,0])
    expression_[0].append([[start[0],end[0]],start,end])
    for d in range(max_depth):
        for e in expression_[d]:
            start = e[1]
            end = e[2]
            l = length(start,end)
            pmid = mid(start,end)
            h = np.random.normal(0,l/8)

            zeta = math.atan(h/(l/2))
            l2 = math.sqrt(h*h+(l/2)*(l/2))
            T = np.matrix([[math.cos(zeta),-math.sin(zeta)],[math.sin(zeta),math.cos(zeta)]])
            a = np.matrix([[pmid[0]-start[0]],[pmid[1]-start[1]]])
            b = np.matmul(T,a)*(l2/l*2)
            p = np.array([start[0]+b[0,0],start[1]+b[1,0]])

            expression_[d+1].append([[start[0],p[0]],start,p])
            expression_[d+1].append([[p[0],end[0]],p,end])

# RMDF_loop(0.3,0.2,10)

# RMDF recursive version.
def RMDF(start,end,depth,H,sigma,max_depth):
    if depth >= max_depth:
        expression_[depth].append([[start[0],end[0]],start,end])
        return
    else:
        expression_[depth].append([[start[0],end[0]],start,end])

    l = length(start,end)
    pmid = mid(start,end)
    h = np.random.normal(0,l/8)

    zeta = math.atan(h/(l/2))
    l2 = math.sqrt(h*h+(l/2)*(l/2))
    T = np.matrix([[math.cos(zeta),-math.sin(zeta)],[math.sin(zeta),math.cos(zeta)]])
    a = np.matrix([[pmid[0]-start[0]],[pmid[1]-start[1]]])
    b = np.matmul(T,a)*(l2/l*2)
    p = np.array([start[0]+b[0,0],start[1]+b[1,0]])
    RMDF(start,p,depth+1,H,sigma,max_depth)
    RMDF(p,end,depth+1,H,sigma,max_depth)

# experiment code
# RMDF(np.array([0,0]),np.array([1,0]),0,0.3,0.2,5)

def draww():
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    air_force_blue = '#5D8AA8'
    sub1 = plt.subplot(151)
    sub2 = plt.subplot(152)
    sub3 = plt.subplot(153)
    plt.subplots_adjust(wspace =0, hspace =0)
    x = np.arange(0,1,1/1000)

    # std()3
    y = [func_of_d(x,3) for x in np.arange(0,1,1/1000)]
    sub1.plot(x,y,linewidth=2,color='#5D8AA8')
    y = [func_of_d(x,4) for x in np.arange(0,1,1/1000)]
    sub2.plot(x,y,linewidth=2,color='#5D8AA8')
    y = [func_of_d(x,10) for x in np.arange(0,1,1/1000)]
    sub3.plot(x,y,linewidth=2,color='#5D8AA8')

    sub1.set_title("d = 3", y=-0.3,fontsize=25)
    sub1.set_yticks([])
    sub2.set_title("d = 4", y=-0.3,fontsize=25)
    sub2.set_yticks([])
    sub3.set_title("d = 6", y=-0.3,fontsize=25)
    sub3.set_yticks([])
    plt.show()

# draww()

# RMDF loop version.
def RMDF_shared(shared_depth):
    start = np.array([0,0])
    end = np.array([1,0])
    expression_[0].append([[start[0],end[0]],start,end])
    for d in range(shared_depth):
        for e in expression_[d]:
            start = e[1]
            end = e[2]
            l = length(start,end)
            pmid = mid(start,end)
            h = np.random.normal(0,l/8)

            zeta = math.atan(h/(l/2))
            l2 = math.sqrt(h*h+(l/2)*(l/2))
            T = np.matrix([[math.cos(zeta),-math.sin(zeta)],[math.sin(zeta),math.cos(zeta)]])
            a = np.matrix([[pmid[0]-start[0]],[pmid[1]-start[1]]])
            b = np.matmul(T,a)*(l2/l*2)
            p = np.array([start[0]+b[0,0],start[1]+b[1,0]])

            expression_[d+1].append([[start[0],p[0]],start,p])
            expression_[d+1].append([[p[0],end[0]],p,end])

def clear(shared_depth,max_depth):
    for i in range(shared_depth,max_depth):
        expression_[i+1]=[]

def RMDF_diverge(shared_depth,max_depth):
    for d in range(shared_depth,max_depth):
        for e in expression_[d]:
            start = e[1]
            end = e[2]
            l = length(start,end)
            pmid = mid(start,end)
            h = np.random.normal(0,l/8)

            zeta = math.atan(h/(l/2))
            l2 = math.sqrt(h*h+(l/2)*(l/2))
            T = np.matrix([[math.cos(zeta),-math.sin(zeta)],[math.sin(zeta),math.cos(zeta)]])
            a = np.matrix([[pmid[0]-start[0]],[pmid[1]-start[1]]])
            b = np.matmul(T,a)*(l2/l*2)
            p = np.array([start[0]+b[0,0],start[1]+b[1,0]])

            expression_[d+1].append([[start[0],p[0]],start,p])
            expression_[d+1].append([[p[0],end[0]],p,end])

RMDF_shared(10)


def dtw_distance(ts_a, ts_b, d=lambda x,y: abs(x-y), mww=10000):
    """Computes dtw distance between two time series
    
    Args:
        ts_a: time series a
        ts_b: time series b
        d: distance function
        mww: max warping window, int, optional (default = infinity)
        
    Returns:
        dtw distance
    """
    
    # Create cost matrix via broadcasting with large int
    ts_a, ts_b = np.array(ts_a), np.array(ts_b)
    M, N = len(ts_a), len(ts_b)
    cost = np.ones((M, N))

    # Initialize the first row and column
    cost[0, 0] = d(ts_a[0], ts_b[0])
    for i in range(1, M):
        cost[i, 0] = cost[i-1, 0] + d(ts_a[i], ts_b[0])

    for j in range(1, N):
        cost[0, j] = cost[0, j-1] + d(ts_a[0], ts_b[j])

    # Populate rest of cost matrix within window
    for i in range(1, M):
        for j in range(max(1, i - mww), min(N, i + mww)):
            choices = cost[i-1, j-1], cost[i, j-1], cost[i-1, j]
            cost[i, j] = min(choices) + d(ts_a[i], ts_b[j])

    # Return DTW distance given window 
    return cost[-1, -1]


y = []
def gen_1000curves_and_save():
    x_ = np.arange(0,1,1/1000)
    for i in tqdm(range(100)):
        clear(0,10)
        RMDF_shared(10)
        std10()
        y1 = [func_of_d(x,10) for x in x_]
        clear(9,10)
        RMDF_diverge(9,10)
        std10()
        y2 = [func_of_d(x,10) for x in x_]
        clear(8,10)
        RMDF_diverge(8,10)
        std10()
        y3 = [func_of_d(x,10) for x in x_]
        clear(7,10)
        RMDF_diverge(7,10)
        std10()
        y4 = [func_of_d(x,10) for x in x_]
        clear(6,10)
        RMDF_diverge(6,10)
        std10()
        y5 = [func_of_d(x,10) for x in x_]
        clear(5,10)
        RMDF_diverge(5,10)
        std10()
        y6 = [func_of_d(x,10) for x in x_]
        clear(4,10)
        RMDF_diverge(4,10)
        std10()
        y7 = [func_of_d(x,10) for x in x_]
        clear(3,10)
        RMDF_diverge(3,10)
        std10()
        y8 = [func_of_d(x,10) for x in x_]
        clear(2,10)
        RMDF_diverge(2,10)
        std10()
        y9 = [func_of_d(x,10) for x in x_]
        clear(1,10)
        RMDF_diverge(1,10)
        std10()
        y10 = [func_of_d(x,10) for x in x_]
        y.append((y1,y2,y3,y4,y5,y6,y7,y8,y9,y10))
    # save list
    a = np.array(y)
    np.save('exp_data_in_paper/curves.npy',a)

distance_list = [[],[],[],[],[],[],[],[],[]]
mse_list = [[],[],[],[],[],[],[],[],[]]
rmse_list = [[],[],[],[],[],[],[],[],[]]

def calculate_mse_and_save():
    curves=np.load('exp_data_in_paper/curves.npy')
    curves=curves.tolist()
    for curve in tqdm(curves):
        anchor = curve[0]
        for sample,idx in zip(curve[1:],range(9)):
            mse = mean_squared_error(anchor,sample)
            mse_list[idx].append(mse)
    mse = np.array(mse_list)
    np.save('exp_data_in_paper/mse.npy',mse)

def calculate_rmse_and_save():
    curves=np.load('exp_data_in_paper/curves.npy')
    curves=curves.tolist()
    for curve in tqdm(curves):
        anchor = curve[0]
        for sample,idx in zip(curve[1:],range(9)):
            rmse = np.sqrt(mean_squared_error(anchor,sample))
            rmse_list[idx].append(rmse)
    rmse = np.array(rmse_list)
    np.save('exp_data_in_paper/rmse.npy',rmse)

def calculate_DTW_and_save():
    curves=np.load('exp_data_in_paper/curves.npy')
    curves=curves.tolist()
    for curve in tqdm(curves):
        anchor = curve[0]
        for sample,idx in zip(curve[1:],range(9)):
            distance = dtw_distance(anchor,sample,mww=100)
            distance_list[idx].append(distance)
    dtw = np.array(distance_list)
    np.save('exp_data_in_paper/dtw.npy',dtw)

def draw_boxplot_of_DTW():
    distance_list=np.load('exp_data_in_paper/dtw.npy')
    distance_list=distance_list.tolist()
    # remove outlier
    new_distance_list = []
    for dist in distance_list:
        new_distance_list.append(np.sort(dist)[:-10])
    f = plt.figure(figsize=(16, 6))
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.boxplot(new_distance_list,labels=['1','2','3','4','5','6','7','8','9'],whis=1.5,sym = '.',showmeans=True)
    plt.xlabel('forking depth',size='20')
    plt.ylabel('DTW cost',size='20')
    plt.show()

def draw_boxplot_of_MSE():
    distance_list=np.load('exp_data_in_paper/mse.npy')
    distance_list=distance_list.tolist()
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.boxplot(distance_list,labels=['1','2','3','4','5','6','7','8','9'],whis=1.5,sym = '.',showmeans=True)
    plt.xlabel('forking depth',size='20')
    plt.ylabel('MSE',size='20')
    plt.show()

def draw_boxplot_of_RMSE():
    distance_list=np.load('exp_data_in_paper/rmse.npy')
    distance_list=distance_list.tolist()
    # remove outlier
    new_distance_list = []
    for dist in distance_list:
        new_distance_list.append(np.sort(dist)[:-10])
    f = plt.figure(figsize=(16, 6))
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.boxplot(new_distance_list,labels=['1','2','3','4','5','6','7','8','9'],whis=1.5,sym = '*',showmeans=True)
    plt.xlabel('forking depth',size='20')
    plt.ylabel('RMSE',size='20')
    plt.show()

# # gen
# gen_1000curves_and_save()

# # calculate distance
# calculate_DTW_and_save()
# calculate_mse_and_save()
# calculate_rmse_and_save()

# # draw
# draw_boxplot_of_MSE()
# draw_boxplot_of_RMSE()
# draw_boxplot_of_DTW()






# # DO NOT TOUCH THIS!!!
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
air_force_blue = '#5D8AA8'
sub1 = plt.subplot(151)
sub2 = plt.subplot(152)
sub3 = plt.subplot(153)
sub4 = plt.subplot(154)
sub5 = plt.subplot(155)

plt.subplots_adjust(wspace =0, hspace =0)
x = np.arange(0,1,1/1000)

std10()
y1 = [func_of_d(x,10) for x in np.arange(0,1,1/1000)]

clear(6,10)
RMDF_diverge(6,10)
std10()
y2 = [func_of_d(x,10) for x in np.arange(0,1,1/1000)]

clear(3,10)
RMDF_diverge(3,10)
std10()
y3 = [func_of_d(x,10) for x in np.arange(0,1,1/1000)]

clear(2,10)
RMDF_diverge(2,10)
std10()
y4 = [func_of_d(x,10) for x in np.arange(0,1,1/1000)]

clear(1,10)
RMDF_diverge(1,10)
std10()
y5 = [func_of_d(x,10) for x in np.arange(0,1,1/1000)]

sub1.plot(x,y1,linewidth=2,color='#5D8AA8')
sub2.plot(x,y2,linewidth=2,color='#5D8AA8')
sub3.plot(x,y3,linewidth=2,color='#5D8AA8')
sub4.plot(x,y4,linewidth=2,color='#5D8AA8')
sub5.plot(x,y5,linewidth=2,color='#5D8AA8')

sub1.set_title("contrast", y=-0.3,fontsize=25)
sub2.set_title(r'$\hat{d} = 2$', y=-0.3,fontsize=25)
sub3.set_title(r'$\hat{d} = 6$', y=-0.3,fontsize=25)
sub4.set_title(r'$\hat{d} = 8$', y=-0.3,fontsize=25)
sub5.set_title(r'$\hat{d} = 9$', y=-0.3,fontsize=25)

sub1.set_yticks([])
sub2.set_yticks([])
sub3.set_yticks([])
sub4.set_yticks([])
sub5.set_yticks([])
sub1.set_xticks([])
sub2.set_xticks([])
sub3.set_xticks([])
sub4.set_xticks([])
sub5.set_xticks([])

plt.show()