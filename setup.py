#!python3.6

# Created by Chengyu on 2020/5/14。
# Usage: python setup.py install

from distutils.core import setup
setup(name="shape", version="1.0", description="RMDF", author="Chengyu", py_modules=['shape.RMDF'])
setup(name="generator", version="1.0", description="some generators", author="Chengyu", py_modules=['generator.additive_anomaly_generator','generator.pattern','generator.abstract_generator','generator.noise_generator','generator.trend_generator','generator.season_generator','generator.anomaly_generator'])
setup(name="EVT", version="1.0", description="Extreme Value Theory", author="Chengyu", py_modules=['EVT.spot'])
setup(name="visual", version="1.0", description="visualization tools", author="Chengyu", py_modules=['tsagen_visual.visual'])