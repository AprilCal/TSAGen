#!python3.6

# Created by Chengyu on 2020/6/6.
# Additive anomaly patterns.

import numpy as np

def typeI(w1,w2,h):
    return list(map(lambda x: exprForTypeII(w1,w2,h,x), np.arange(w1+w2+1)))

def typeII(w,h1,h2):
    k = (h2-h1)/(w-1)
    return list(map(lambda x: linear(k,h1,x), np.arange(w+1)))

def a(w1,h,x):
    return h*(np.e**((-np.log(1/1000)/w1)*(x-w1)))

def b(w1,w2,h,x):
    return h*(np.e**((np.log(1/1000)/w2)*(x-w1)))

# function expressions.
def linear(k,b,x):
    return k*x+b

def exprForTypeII(w1,w2,h,x):
    if(x<=w1):
        return a(w1,h,x)
    else:
        return b(w1,w2,h,x)