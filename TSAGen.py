'''
Created by Chengyu on 2021/7/18.
'''

import argparse
from numpy.core.fromnumeric import size
from numpy.lib.function_base import iterable
import yaml
import os
import numpy as np
import generator.trend_generator as tg
import generator.noise_generator as ng
import generator.season_generator as sg

def r(zeta):
    pos = np.random.choice([1,2,3,4],1,p=[1/4,1/4,1/4,1/4])
    if pos == 1:
        return np.random.uniform(zeta[0],zeta[1])
    elif pos == 2:
        return np.random.uniform(zeta[1],zeta[2])
    elif pos == 3:
        return np.random.uniform(zeta[2],zeta[3])
    else:
        return np.random.uniform(zeta[3],zeta[4])

def gen_theta(theta,size):
    theta_list = [r(theta) for x in range(0,size)]
    return theta_list

def pre_process_config(config):
    # Deal with season features.
    for feature in config:
        # print(config['SEASON'][feature])
        if not isinstance(config[feature], list):
            # padding
            config[feature]=[config[feature] for x in range(0,5)]
    return config

def gen_m(config):
    num = config['TOTAL_NUM']
    features = pre_process_config(config['FEATURES'])
    # print(features)
    theta1_list = gen_theta(features['theta1'],num)
    theta2_list = gen_theta(features['theta2'],num)
    theta3_list = gen_theta(features['theta3'],num)
    theta4_list = gen_theta(features['theta4'],num)
    theta5_list = gen_theta(features['theta5'],num)
    theta6_list = gen_theta(features['theta6'],num)
    theta7_list = gen_theta(features['theta7'],num)
    theta8_list = gen_theta(features['theta8'],num)
    theta9_list = gen_theta(features['theta9'],num)
    k1_list = gen_theta(features['k1'],num)
    k2_list = gen_theta(features['k2'],num)
    for i in range(0,num):
        noise_generator = ng.NoiseGeneratorFactory().get_generator(None)
        trend_generator = tg.TrendGenerator()
        sg.SeasonGeneratorFactory(theta5_list[i],10,200,drift_a=0,drift_f=0,forking_depth=7).get_generator('vanish')

        noise = noise_generator.gen(theta6_list[i],theta7_list[i],theta8_list[i],theta9_list[i],num)
        trend = trend_generator.gen(theta1_list[i],theta2_list[i],num)

def gen_v(config):
    config
    # season_generator = sg.SeasonGeneratorFactory(10,10,200,drift_a=0,drift_f=0,forking_depth=7,'vanish')
    noise_generator = ng.Gaussian()
    trend_generator = tg.TrendGenerator()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TSAGen help document.')
    parser.add_argument('--mode', type=str, choices=['m', 'v'], help='generation mode. m: meta manner; v: variable-control manner.')
    parser.add_argument('--meta', type=str, help='meta features path')

    args = parser.parse_args()

    meta_path = args.meta
    
    with open(meta_path) as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
        # print(config)
        out_path = config['OUT_PATH']
        if not os.path.exists(out_path):
            os.mkdir(out_path)

        if args.mode=='m':
            gen_m(config)
        else:
            gen_v(config)