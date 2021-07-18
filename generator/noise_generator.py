#!python3.6

# Created by Chengyu on 2020/5/14。
# Noise Generator.

import numpy as np
import matlab
import matlab.engine

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

class GaussianWithChangePoints(Gaussian):
    def _inject(self):
        pos_list = [0.5,0.8]
        a_len = 20
        for pos in pos_list:
            position = int(pos*len(self.noise))
            a_segment = np.random.normal(self.mu, self.sigma*10, a_len)
            self.noise[position:position+a_len] = a_segment
            self.label[position:position+a_len] = np.ones(len(a_segment),dtype=np.int)

print("starting matlab.")
engine = matlab.engine.start_matlab()

class Pearson:
    def __init__(self):
        # print("starting matlab.")
        self.engine = engine # Start MATLAB process
        # engine = matlab.engine.start_matlab("-desktop") # Start MATLAB process with graphic UI

        self.noise = []
        self.label = []

    def gen(self,mu,sigma,skew,kurt,size):
        
        self.mu = mu
        self.sigma = sigma
        self.skew = skew
        self.kurt = kurt

        self.noise = self.engine.pearsrnd(matlab.double([mu]),
                                    matlab.double([sigma]),
                                    matlab.double([skew]),
                                    matlab.double([kurt]),
                                    matlab.double([1]),
                                    matlab.double([size]))[0]
        self.label = np.zeros(size, dtype=np.int)
        self._inject()
        return (np.array(self.noise), np.array(self.label))
    
    def _inject(self):
        pass

class PearsonWithChangePoints(Pearson):
    def _inject(self):
        pos_list = [0.5,0.8]
        a_len = 20
        for pos in pos_list:
            position = int(pos*len(self.noise))
            a_segment = np.random.normal(self.mu, self.sigma*10, a_len)
            self.noise[position:position+a_len] = a_segment
            self.label[position:position+a_len] = np.ones(len(a_segment),dtype=np.int)