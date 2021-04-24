import numpy as np
import Assembler as assem
import generator.trend_generator as tg
import matplotlib.pyplot as plt
import generator.noise_generator as ng
import generator.season_generator as sg
import matplotlib.pyplot as plt
import time

#====================================================================================
# Group1 
# spike, beat, type1, type2, control noise level.
seas_time_list = []
noise_time_list = []
trend_time_list = []
struc_time_list = []

for cycle_num in [10,20,30,40,50,60,70,80,90,100]:
    season_generator = sg.NormalSeasonGenerator(cycle_num,10,1000,drift_a=0,drift_f=0,forking_depth=0)
    noise_generator = ng.Gaussian()
    trend_generator = tg.TrendGenerator()

    seas_start = time.time()
    season = season_generator.gen_season()
    seas_end = time.time()
    # print(seas_end-seas_start)

    length = len(season[0])

    noise_start = time.time()
    noise = [noise_generator.gen(0,2,length)]
    noise_end = time.time()
    # print(noise_end-noise_start)

    trend_start = time.time()
    trend = trend_generator.gen(0,0,length)
    trend_end = time.time()
    # print(trend_end-trend_start)

    struc_start = time.time()
    assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'noise',10e-7,0.2,a_type='beat')

    assembler.assemble()
    assembler.save(path='output2/spk')
    struc_end = time.time()
    # print(struc_end-struc_start)

    time_seas = seas_end-seas_start
    time_noise = noise_end-noise_start
    time_trend = trend_end-trend_start
    time_struc = struc_end-struc_start
    print(time_seas,time_noise,time_trend,time_struc)
    seas_time_list.append(time_seas)
    noise_time_list.append(time_noise)
    trend_time_list.append(time_trend)
    struc_time_list.append(time_struc)

import matplotlib.pyplot as plt
plt.clf()
plt.plot(seas_time_list,label='seas')
plt.plot(noise_time_list,label='noise')
plt.plot(trend_time_list,label='trend')
plt.plot(struc_time_list,label='ano')
plt.legend()
plt.show()

print(seas_time_list)
print(noise_time_list)
print(trend_time_list)
print(struc_time_list)