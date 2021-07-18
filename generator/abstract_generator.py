#!python3.6

# Created by Chengyu on 2020/5/13.
# Abstract generators.

import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from shape.RMDF import RMDF

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

# Normal season generator
# template method.
# implement hook to custimize anomaly.
class AbstractSeasonGenerator():
    def __init__(self,cycle_num,amplitude,cycle_len,drift_a=0,drift_f=0,forking_depth=0):
        self.cycle_list = []
        self.label_list = []

        self.cycle_num = int(cycle_num)
        self.amplitude = amplitude
        self.cycle_len = cycle_len
        self.drift_a = drift_a
        self.drift_f = drift_f
        self.forking_depth = forking_depth

        self.drift_a_for_every_cycle = np.random.uniform(1,1+self.drift_a,self.cycle_num)
        self.drift_f_for_every_cycle = np.random.uniform(1,1+self.drift_f,self.cycle_num)

        self.cycle_generator = RMDF(depth=10)
        self.cycle_generator.gen_anchor()

    def _gen(self):
        amplitude = self.amplitude
        for drift_amp, length_d in zip(self.drift_a_for_every_cycle, self.drift_f_for_every_cycle):
            # apply drift
            self.cycle_list.append(amplitude*drift_amp*self.cycle_generator.gen(self.forking_depth, int(length_d*self.cycle_len)))
            self.label_list.append(np.zeros(int(length_d*self.cycle_len),dtype=np.int))

    # hook
    def _inject(self):
        pass

    def gen_season(self):
        self._gen()
        self._inject()
        season = np.concatenate(self.cycle_list)
        label = np.concatenate(self.label_list)
        self.cycle_list = []
        self.label_list = []
        self.cycle_generator.clear_all()
        return (season,label)