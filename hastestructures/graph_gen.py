#!/usr/bin/env python3

import math
import numpy as np
import pandas as pd


class GraphGen:

	def __init__(self):
		self.functions = []
		self.comms = []
		self.flattened_functions = []


	def generate_graph(self, num_functions, num_layers, num_extra_edges):
		exec_times = pd.read_csv("/Users/Avi/haste_project/azure_data/mod_functions/function_durations_percentiles_anon_d01.csv")
		timings = exec_times["Average"].to_frame()
		timings_clean = timings[(timings["Average"] != 0)]
		timings_clean["Average"] += 100
		timings_list = timings_clean["Average"].tolist()
		layers = sorted(np.random.choice(num_functions - 1, num_layers - 1, replace=False))
		layers_aug = [layer + 1 for layer in layers]
		layers_aug.append(num_functions)
		layers_aug.insert(0, 0)

		for ind in range(len(layers_aug) - 1):
			this_stop = layers_aug[ind]
			next_stop = layers_aug[ind+1]
			diff = next_stop - this_stop
			append_list = []
			for j in range(diff):
				append_list = (np.random.choice(timings_list, diff)).tolist()
			self.functions.append(append_list)


		comms = []
		comms_extra = []

		for i in range(len(self.functions) - 1):
			this_stop = len(self.functions[i])
			next_stop = len(self.functions[i + 1])
			max_stop = max(this_stop, next_stop)
			comm_lengths = np.random.choice(100, max_stop)
			for j in range(max_stop):
				this_ind = (j % this_stop) + layers_aug[i]
				next_ind = (j % next_stop) + layers_aug[i + 1]
				comms.append([this_ind, next_ind, comm_lengths[j]])
        
		while(len(comms_extra) < num_extra_edges):
			picked_layers = sorted(np.random.choice(num_functions, 2))
			first_ind = np.argmax(layers_aug > picked_layers[0])
			second_ind = np.argmax(layers_aug > picked_layers[1])
			if second_ind > first_ind:
				comms_extra.append([picked_layers[0], picked_layers[1], np.random.choice(100)])

		self.comms = comms + comms_extra

		self.flattened_functions = list(np.concatenate(self.functions).flat)

