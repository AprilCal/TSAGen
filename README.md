# TSAGen
Repository for paper ''TSAGen: Synthetic Time Series Generation for KPI Anomaly Detection''

This repository will be maintained for a long time.
Fell free to submit a issue or contact us if you encounter any issue when using TSAGen.

# Installation
```bash
git clone https://AprilCal/TSAGen.git
cd ./TSAGen
pip install requirements.txt
python setup.py install
```

# Usage
## API usage
You can directly use the API provided by TSAGen. The source file ''gen.py'' contains many examples for the API usage.
For example:
```python
# Choose the generator for season, noise, and trend component, respectively.
season_generator = sg.NormalSeasonGenerator(10,10,200,drift_a=0,drift_f=0,forking_depth=7)
noise_generator = ng.Gaussian()
trend_generator = tg.TrendGenerator()

# Control the noise component as a variable.
season = season_generator.gen_season()
length = len(season[0])
noise = [noise_generator.gen(0,sigma,length) for sigma in np.linspace(0.5,2,100)]
trend = trend_generator.gen(0,0,length)

# Assemble components.
assembler = assem.AssemblerWithAdditiveAnomalyInjector_v1(season,noise,trend,'noise',10e-7,0.2,a_type='beat')
assembler.assemble()
```
## Other usage
Coming soon...

# Notes
Note that, to enable the pearson distribution, the installation of MATLAB and other configurations are required.

