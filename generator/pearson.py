#!python3.6

# Created by Chengyu on 2020/5/15.
# Pearson Distribution System.

# Usage:
# p = Pearson()
# p.pearsrnd(nu,sigma,skew,kurt,size)
# pearsrnd returns a np.array

import matlab
import matlab.engine
import numpy as np

engine = matlab.engine.start_matlab()

class Pearson:
    def __init__(self):
        self.engine = engine # Start MATLAB process
        # engine = matlab.engine.start_matlab("-desktop") # Start MATLAB process with graphic UI
    def pearsrnd(self,mu,sigma,skew,kurt,size):
        result = self.engine.pearsrnd(matlab.double([mu]),
                                    matlab.double([sigma]),
                                    matlab.double([skew]),
                                    matlab.double([kurt]),
                                    matlab.double([1]),
                                    matlab.double([size]))[0]
        return np.array(result)