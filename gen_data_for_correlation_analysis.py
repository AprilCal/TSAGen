#!python3.6

# Created by Chengyu on 2021/3/8.
# Generating data for correlation analysis.

import numpy as np
import Assembler as assem
import generator.trend_generator as tg
import matplotlib.pyplot as plt
import generator.noise_generator as ng
import generator.season_generator as sg
import matplotlib.pyplot as plt

# season_generator = sg.SeasonGeneratorWithShapeDeformation(10,10,200,drift_a=0,drift_f=0,forking_depth=7)
season_generator = sg.NormalSeasonGenerator(10,10,200,drift_a=0,drift_f=0,forking_depth=7)
noise_generator = ng.Gaussian()
# noise_generator = ng.GaussianWithChangePoints()
trend_generator = tg.TrendGenerator()

season = [season_generator.gen_season() for x in range(1)]
length = len(season[0][0])
noise = noise_generator.gen(0,0.5,length)
trend = trend_generator.gen(15,0,length)

# assembler = assem.AbstractAssembler(season,noise,trend,'season')
# assembler = assem.AbstractAssembler(season,noise,trend,'season')
assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'season', q=10e-7,a_type='type2')
assembler.assemble()
assembler.save(path='output/TSACorr')