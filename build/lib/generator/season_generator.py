from generator.abstract_generator import AbstractSeasonGenerator
import matplotlib.pyplot as plt
import numpy as np

class NormalSeasonGenerator(AbstractSeasonGenerator):
    def _inject(self):
        # do nothing
        pass

class SeasonGeneratorWithShapeDeformation(AbstractSeasonGenerator):
    def _inject(self):
        pos_list = [5]
        forking_depth = 9
        for pos in pos_list:
            amplitude = self.amplitude
            drift_a = self.drift_a_for_every_cycle[pos]
            length_d = self.drift_f_for_every_cycle[pos]
            anomaly_cycle = drift_a*amplitude*self.cycle_generator.gen(forking_depth, int(length_d*self.cycle_len))
            self.cycle_list[pos] = anomaly_cycle
            self.label_list[pos] = np.ones(len(anomaly_cycle),dtype=np.int)

class SeasonGeneratorWithCycleVanish(AbstractSeasonGenerator):
    def _inject(self):
        pos_list = [5]
        forking_depth = 9
        for pos in pos_list:
            amplitude = self.drift_a_for_every_cycle[pos]
            length_d = self.drift_f_for_every_cycle[pos]
            # anomaly_cycle = amplitude*self.cycle_generator.gen(forking_depth, int(length_d*self.cycle_len))
            anomaly_cycle = np.zeros(int(length_d*self.cycle_len))
            self.cycle_list[pos] = anomaly_cycle
            self.label_list[pos] = np.ones(len(anomaly_cycle),dtype=np.int)
            
class example_season_generator(AbstractSeasonGenerator):
    def _inject(self):
        pos_list = [5,6]
        forking_depth = 10
        for pos in pos_list:
            amplitude = self.drift_a_for_every_cycle[pos]
            length_d = self.drift_f_for_every_cycle[pos]
            anomaly_cycle = amplitude*self.cycle_generator.gen(forking_depth, int(length_d*self.cycle_len))
            self.cycle_list[pos] = anomaly_cycle
            self.label_list[pos] = np.ones(len(anomaly_cycle),dtype=np.int)