#!python3.6

# Created by Chengyu on 2020/5/14。
# Noise Generator.

import numpy as np

class Gaussian():
    def __init__(self):
        self.noise = []
        self.label = []
        self.sigma = 0
        pass
    
    def _inject(self):
        pass

    def gen(self, mu, sigma, size):
        self.noise = np.random.normal(mu, sigma, size)
        self.label = np.zeros(size, dtype=np.int)
        self.mu = mu
        self.sigma = sigma
        self._inject()
        return (self.noise, self.label)

class Pearson():
    def __init__(self):
        pass

    def _inject(self):
        pass
    def gen(self, mu, sigma, skew, kurt, size):
        pass

class GaussianWithChangePoints(Gaussian):
    def _inject(self):
        pos_list = [0.5,0.8]
        a_len = 20
        for pos in pos_list:
            position = int(pos*len(self.noise))
            a_segment = np.random.normal(self.mu, self.sigma*10, a_len)
            self.noise[position:position+a_len] = a_segment
            self.label[position:position+a_len] = np.ones(len(a_segment),dtype=np.int)
            