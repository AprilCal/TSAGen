#!python3.6

# Created by Chengyu on 2020/12/9.
# Assembler.

import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import generator.pattern as pattern
import generator.additive_anomaly_generator as ag
from tqdm import tqdm
from tsagen_visual.visual import show
from EVT.spot import bidSPOT

# This is an abstract calss.
# method assemble() is template method.
# inject() should be rewritten according to your need.
class AbstractAssembler():
    def __init__(self, season, noise, trend, control=None):
        self.season = season
        self.trend = trend
        self.noise = noise
        self.label = 0
        self.additive = 0
        self.results = []
        self.control = control
    
    # template method.
    def assemble(self):
        # invoke hook
        self._inject()
        # print(self.control)
        if self.control == 'season':
            for s,l in self.season:
                label = np.bitwise_or(l,self.noise[1])
                label = np.bitwise_or(label,self.trend[1])
                self.results.append((s+self.noise[0]+self.trend[0],label))
        elif self.control == 'noise':
            for n,l in self.noise:
                label = np.bitwise_or(l,self.season[1])
                label = np.bitwise_or(label,self.trend[1])
                self.results.append((n+self.season[0]+self.trend[0],label))
        elif self.control == 'trend':
            for t,l in self.season:
                label = np.bitwise_or(l,self.noise[1])
                label = np.bitwise_or(label,self.season[1])
                self.results.append((t+self.noise[0]+self.season[0],label))
        elif self.control == 'drift_f':
            pass
        else:
            label = np.bitwise_or(self.noise[1],self.season[1])
            label = np.bitwise_or(label,self.trend[1])
            self.results.append((self.noise[0]+self.season[0]+self.trend[0],label))
        self._post_inject()

    # hook.
    def _inject(self):
        pass

    # post hook.
    def _post_inject(self):
        pass

    def save(self,path='output',preifix='synthetic',plot=True,fig_size=(16,4)):
        idx = 0
        for r, l in tqdm(self.results):
            df = pd.DataFrame()
            df['timestamp']=np.arange(len(r))
            df['value']=r
            df['label']=l

            if not os.path.exists(path+'/data'):
                os.makedirs(path+'/data')
            if not os.path.exists(path+'/fig'):
                os.makedirs(path+'/fig')
            filename = path+'/data/'+preifix+'_'+str(idx)
            figname = path+'/fig/'+preifix + '_' + str(idx)
            df.to_csv(filename + '.csv',index=None)
            if plot:
                sub = show(df['value'],df['label'],title=filename,figure_size=fig_size)
                sub.savefig(figname + '.jpg')
                # plt.show()
                plt.close()
            idx += 1

# Assmebler with additive anomaly injector.
class AssemblerWithAdditiveAnomalyInjector(AbstractAssembler):
    def __init__(self, season, noise, trend, control=None, q=10e-5, init_portion=0.2):
        AbstractAssembler.__init__(self, season, noise, trend, control)
        self.q = q
        self.init_portion = init_portion

    def _post_inject(self):
        # establish low probablity boundary.
        q = self.q
        d = 10
        init_portion = self.init_portion
        idx = 0
        for result, label in self.results:
            length = len(result)
            init_data = result[:int(length*init_portion)]
            s = bidSPOT(q,d)
            s.fit(init_data, result)
            s.initialize()
            r = s.run()
            s.plot(r)
            # plt.show()
            upper_thresholds = r['upper_thresholds']
            lower_thresholds = r['lower_thresholds']

            # r,l = insert_type2_anomaly(result,label,upper_thresholds,lower_thresholds,[0.3,0.4,0.5,0.6,0.7])
            r,l = ag.insert_spike_anomaly(result,label,upper_thresholds,lower_thresholds,[0.3,0.4,0.5,0.6,0.7]) #insert_type2_anomaly(result,label,upper_thresholds,lower_thresholds,[0.3,0.4,0.5,0.6,0.7])
            self.results[idx]=(r,l)

# Assmebler with additive anomaly injector.
# control noise level.
class AssemblerWithAdditiveAnomalyInjector_v1(AbstractAssembler):
    def __init__(self, season, noise, trend, control=None, q=10e-7, init_portion=0.2, a_type='spike'):
        AbstractAssembler.__init__(self, season, noise, trend, control)
        self.q = q
        self.a_type = a_type
        self.init_portion = init_portion

    def _post_inject(self):
        # establish low probablity boundary.
        q = self.q
        d = 10
        init_portion = self.init_portion
        idx = 0
        for result, label in self.results:
            length = len(result)
            init_data = result[:int(length*init_portion)]
            s = bidSPOT(q,d)
            s.fit(init_data, result)
            s.initialize()
            r = s.run()
            s.plot(r)
            # plt.show()
            upper_thresholds = r['upper_thresholds']
            lower_thresholds = r['lower_thresholds']
            if self.a_type == 'spike':
                r,l = ag.insert_spike_anomaly(result,label,upper_thresholds,lower_thresholds,[0.3,0.4,0.5,0.6,0.7])
            elif self.a_type == 'beat':
                r,l = ag.insert_beat_anomaly(result,label,upper_thresholds,lower_thresholds,[0.3,0.4,0.5,0.6,0.7])
            elif self.a_type == 'type1':
                r,l = ag.insert_type1_anomaly(result,label,upper_thresholds,lower_thresholds,[0.3,0.4,0.5,0.6,0.7])
            elif self.a_type == 'type2':
                r,l = ag.insert_type2_anomaly(result,label,upper_thresholds,lower_thresholds,[0.6,0.9])
            else:
                print('a_type does not exist.')
            self.results[idx]=(r,l)
            idx += 1
