from EVT.spot import bidSPOT
import numpy as np
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

def insert_point_anomaly(kpi,label,num):
    pt = partition(len(kpi),num)
    for k in pt:
        pos = int(random.uniform(k[0],k[1]-1))

        local_mean = np.mean(kpi[:pos])
        mean = np.mean(kpi[pos-50:pos+50])
        var = np.var(kpi[pos-50:pos+50])
        r = np.random.normal(0,1,1)
        # print(local_mean,mean,var,r)
        x = (local_mean+mean)*(1+var)*r+kpi[pos]

        kpi[pos] = x
        label[pos-1]=1
        label[pos]=1
        label[pos+1]=1
    return kpi,label