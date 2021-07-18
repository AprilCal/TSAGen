#!python3.6

# Created by Chengyu on 2020/6/6.
# Additive anomaly generator.

import numpy as np
import generator.pattern as pt
import random

def partition(length, seg_num):
    if seg_num >= length:
        print("error:segment num > length.")
    sublen = int(length/seg_num)
    pos = 0
    pt = []
    for i in range(0,seg_num-1):
        pt.append([pos,pos+sublen])
        pos += sublen
    pt.append([pos,length])
    return pt

# insert spike anomaly
def insert_spike_anomaly(kpi,label,upt,dwt,pos_list):
    kpi = kpi.copy()
    length = len(kpi)
    for pos in pos_list:
        position = int(pos*length)
        degree = [upt[position]-kpi[position]]
        a = degree
        for i in np.arange(len(a)):
            kpi[position+i] = a[i]+kpi[position+i]
            label[position+i] = 1
    return (kpi, label)

def insert_beat_anomaly(kpi,label,upt,dwt,pos_list):
    kpi = kpi.copy()
    length = len(kpi)
    for pos in pos_list:
        position = int(pos*length)
        direction = 1 #np.random.choice([-1,1],1,p=[0.5,0.5])
        degree1 = upt[position]-kpi[position]
        degree2 = kpi[position+1]-upt[position+1]
        a = [degree1,degree2]
        for i in np.arange(len(a)):
            kpi[position+i] = a[i]+kpi[position+i]
            label[position+i] = 1
    return (kpi,label)

def insert_type1_anomaly(kpi, label, upt, dwt, pos_list):
    kpi = kpi.copy()
    length = len(kpi)
    for pos in pos_list:
        position = int(pos*length)
        # direction = 1 #np.random.choice([-1,1],1,p=[0.5,0.5])
        degree = upt[position]-kpi[position]
        a = pt.typeI(10,20,degree)
        for i in np.arange(len(a)):
            kpi[position+i] = a[i]+kpi[position+i]
            label[position+i] = 1
    return (kpi, label)

def insert_type2_anomaly(kpi, label, upt, dwt, pos_list):
    kpi = kpi.copy()
    length = len(kpi)
    for pos in pos_list:
        position = int(pos*length)
        direction = 1 #np.random.choice([-1,1],1,p=[0.5,0.5])
        a_l = 20
        degree1 = upt[position]-kpi[position]
        degree2 = upt[position]-kpi[position+a_l]
        a = pt.typeII(20,degree1,degree2)
        for i in np.arange(len(a)):
            kpi[position+i] = a[i]+kpi[position+i]
            label[position+i] = 1
    return (kpi, label)

# def insert_fluctuate_anomaly(noise,label,degree,num,moms):
#     noise = noise.copy()
#     mu = moms[0]
#     sigma = moms[1]
#     skew = -10*moms[2]
#     kurt = moms[3]

#     pt = partition(len(noise),num)
#     for k in pt:
#         a_length = int(random.uniform(50,150))
#         pos = int(random.uniform(k[0],k[1]-a_length))

#         noiseGenerator = ng.NoiseGenerator()
#         a_noise = noiseGenerator.genNoise(moms[0],moms[1],moms[2],moms[3],150)
#         print('a_noise',a_noise)
#         for i in range(0,a_length):
#             noise[pos+i] = a_noise[i]
#             label[pos+i] = 1
#     return noise,label

# # insert null point.
# def insert_null_anomaly(kpi,label,num):
#     kpi = kpi.copy()
#     pt = partition(len(kpi),num)
#     for k in pt:
#         pos = int(random.uniform(k[0],k[1]-1))
#         kpi[pos]=0
#         label[pos-1]=1
#         label[pos]=1
#         label[pos+1]=1
#     return kpi,label

# # insert dip anomaly
# def insert_dip_anomaly(kpi,label,num, upt, dwt):
#     kpi = kpi.copy()
#     pt = partition(len(kpi),num)
#     for k in pt:
#         pos = int(random.uniform(k[0],k[1]-1))
#         label[pos-1]=1
#         label[pos]=1
#         label[pos+1]=1
#         degree = kpi[pos]-dwt[pos]
#         kpi[pos]+=degree
#     return kpi,label

# this type is defined in the paper of Microsoft.
def insert_point_anomaly(kpi,label,num):
    pt = partition(len(kpi),num)
    for k in pt:
        pos = int(random.uniform(k[0],k[1]-1))

        local_mean = np.mean(kpi[:pos])
        mean = np.mean(kpi[pos-50:pos+50])
        var = np.var(kpi[pos-50:pos+50])
        r = np.random.normal(0,1,1)
        print(local_mean,mean,var,r)
        x = (local_mean+mean)*(1+var)*r+kpi[pos]

        kpi[pos] = x
        label[pos-1]=1
        label[pos]=1
        label[pos+1]=1
    return kpi,label