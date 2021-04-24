#!python3.6

# Created by Chengyu on 2020/5/14.
# Trend generator.

import numpy as np
import math

class TrendGenerator():
    def __init__(self):
        pass

    def _expression(self,zeta,ba,x):
        k = math.tan(zeta)
        b = ba
        return k*x+b

    def _inject(self):
        pass

    def gen(self,ba,zeta,size):
        x = np.arange(size)
        trend = []
        for i in x:
            trend.append(self._expression(zeta,ba,i))
        label = np.zeros(size,dtype=np.int)
        return (np.array(trend),label)
