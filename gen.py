#!python3.6

# Created by Chengyu on 2021/1/2.
# examples.

import numpy as np
import Assembler as assem
import generator.trend_generator as tg
import generator.noise_generator as ng
import generator.season_generator as sg
import matplotlib.pyplot as plt

#====================================================================================
# Group1 
# spike, beat, type1, type2, control noise level.
season_generator = sg.NormalSeasonGenerator(10,10,200,drift_a=0,drift_f=0,forking_depth=7)
noise_generator = ng.Gaussian()
trend_generator = tg.TrendGenerator()

season = season_generator.gen_season()
length = len(season[0])
noise = [noise_generator.gen(0,sigma,length) for sigma in np.linspace(0.5,2,100)]
trend = trend_generator.gen(0,0,length)

# assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'noise',10e-7,0.2,a_type='spike')
assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'noise',10e-7,0.2,a_type='beat')
# assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'noise',10e-7,0.2,a_type='type1')
# assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'noise',10e-7,0.2,a_type='type2')
assembler.assemble()

# assembler.save(path='output/TSABen/group_2/spike')
# assembler.save(path='output/TSABen/group_1/beat_noise')
# assembler.save(path='output/TSABen/group_1/type1_noise')
# assembler.save(path='output/TSABen/group_1/type2_noise')

#====================================================================================
# Group2
# spike, beat, type1, type2
# season_generator = sg.NormalSeasonGenerator(10,10,200,drift_a=0,drift_f=0,forking_depth=7)
# noise_generator = ng.Gaussian()
# trend_generator = tg.TrendGenerator()

# season = [season_generator.gen_season() for x in range(100)]
# length = len(season[0][0])
# noise = noise_generator.gen(0,0.5,length)
# trend = trend_generator.gen(0,0,length)

# # assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'season',10e-7,0.2,a_type='spike')
# # assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'season',10e-7,0.2,a_type='beat')
# assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'season',10e-7,0.2,a_type='type1')
# # assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'season',10e-7,0.2,a_type='type2')
# assembler.assemble()

# # assembler.save(path='output/TSABen/group_2/spike')
# # assembler.save(path='output/TSABen/group_2/beat')
# assembler.save(path='output/TSABen/group_2/type1')
# # assembler.save(path='output/TSABen/group_2/type2')

#====================================================================================
# Group2
# cycle deformation.
# season_generator = sg.SeasonGeneratorWithShapeDeformation(10,10,200,drift_a=0,drift_f=0,forking_depth=7)
# noise_generator = ng.Gaussian()
# trend_generator = tg.TrendGenerator()

# season = [season_generator.gen_season() for x in range(100)]
# length = len(season[0][0])
# noise = noise_generator.gen(0,0.5,length)
# trend = trend_generator.gen(15,0,length)

# assembler = assem.AbstractAssembler(season,noise,trend,'season')
# assembler.assemble()
# # assembler.save(path='output/TSABen/group_2/cycle_deformation')

# cycle vanish.
# season_generator = sg.SeasonGeneratorWithCycleVanish(10,10,200,drift_a=0,drift_f=0,forking_depth=7)
# noise_generator = ng.Gaussian()
# trend_generator = tg.TrendGenerator()

# season = [season_generator.gen_season() for x in range(100)]
# length = len(season[0][0])
# noise = noise_generator.gen(0,0.5,length)
# trend = trend_generator.gen(15,0,length)

# assembler = assem.AbstractAssembler(season,noise,trend,'season')
# assembler.assemble()
# assembler.save(path='output/TSABen/group_2/cycle_vanish')

# change point
# season_generator = sg.NormalSeasonGenerator(10,10,200,drift_a=0,drift_f=0,forking_depth=7)
# noise_generator = ng.GaussianWithChangePoints()
# trend_generator = tg.TrendGenerator()

# season = [season_generator.gen_season() for x in range(100)]
# length = len(season[0][0])
# noise = noise_generator.gen(0,1,length)
# trend = trend_generator.gen(15,0,length)

# assembler = assem.AbstractAssembler(season,noise,trend,'season')
# assembler.assemble()
# assembler.save(path='output/TSABen/group_2/change_point')