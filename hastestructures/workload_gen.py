#!/usr/bin/env python3

import math
import numpy as np
import pandas as pd

from .test_graph import TestGraph

class WorkloadGen:

	def __init__(self):
		self.dags = None
		self.merged = None

		exec_times = pd.read_csv("/Users/Avi/haste_project/azure_data/mod_functions/function_durations_percentiles_anon_d01.csv")
		timings = exec_times[["HashApp", "Average"]]
		mem_alloced = pd.read_csv("/Users/Avi/haste_project/azure_data/mod_functions/app_memory_percentiles_anon_d01.csv")
		mems = mem_alloced[["HashApp","AverageAllocatedMb"]]
		time_mem = (timings.merge(mems, on="HashApp", how="inner"))[["Average", "AverageAllocatedMb"]]
		max_all = max(time_mem["AverageAllocatedMb"])
		tm_int = time_mem.loc[time_mem["Average"] > max_all]
		tm_large = tm_int.loc[tm_int["AverageAllocatedMb"] > 0]
		tm_large.reset_index(drop=True, inplace=True)
		tm_large["UniqueInd"] = tm_large.index
		self.large_values = tm_large.values

	def generate_workload(self, num_dags, percent_duplicate, num_functions_total, num_layers, num_extra_edges, dupl_num_functions, dupl_num_layers, dupl_extra_edges):
		self.dags = []
		for i in range(num_dags):
			temp_graph = TestGraph(num_layers)
			self.dags.append(temp_graph)
		self.merged = TestGraph(num_layers)

		num_functions_per_dag = int(num_functions_total / num_dags)
		num_duplicate = int(num_functions_total * percent_duplicate)
		num_functions = int(num_functions_total - num_duplicate)

		large_range = list(range(len(self.large_values)))
		all_functions_ind = sorted(list(np.random.choice(large_range, num_functions, replace=False)))
		dupl_functions_ind = all_functions_ind[:num_duplicate]
		all_functions = self.large_values[all_functions_ind]
		dupl_functions = self.large_values[dupl_functions_ind]

		max_dupl = num_functions_per_dag - num_layers

		dupls_total = num_duplicate / dupl_num_functions
		dupls_added = 0

		while(dupls_added < dupls_total):
			dupl_picked_graphs = sorted(np.random.choice(len(self.dags), 2, replace=False))
			start_graph = self.dags[dupl_picked_graphs[0]]
			# print(dupl_picked_graphs[0])
			end_graph = self.dags[dupl_picked_graphs[1]]
			# print(dupl_picked_graphs[1])
			if ((start_graph.num_nodes + dupl_num_functions) < max_dupl) and ((end_graph.num_nodes + dupl_num_functions) < max_dupl):
				dupl_start_ind = dupls_added * dupl_num_functions
				dupl_end_ind = (dupls_added + 1) * dupl_num_functions
				ret_dupl = self.gen_partial_dag(dupl_functions[dupl_start_ind:dupl_end_ind], dupl_num_layers, dupl_extra_edges)
				these_nodes = ret_dupl[0]
				# print(these_nodes)
				these_edges = ret_dupl[1]
				# print(these_edges)
				these_ids = ret_dupl[2]
				# print(these_ids)
				for i in range(len(these_nodes)):
					these_layer_nodes = these_nodes[i]
					for j in range(len(these_layer_nodes)):
						start_graph.nodes[i].append(these_layer_nodes[j])
						start_graph.node_map[these_layer_nodes[j][2]] = (i, (len(start_graph.nodes[i]) - 1))
						end_graph.nodes[i].append(these_layer_nodes[j])
						end_graph.node_map[these_layer_nodes[j][2]] = (i, (len(end_graph.nodes[i]) - 1))
						self.merged.nodes[i].append(these_layer_nodes[j])
						self.merged.node_map[these_layer_nodes[j][2]] = (i, (len(self.merged.nodes[i]) - 1))

				start_graph.num_nodes += dupl_num_functions
				end_graph.num_nodes += dupl_num_functions
				self.merged.num_nodes += dupl_num_functions
				start_graph.edges.extend(these_edges)
				end_graph.edges.extend(these_edges)
				self.merged.edges.extend(these_edges)
				start_graph.num_edges += (dupl_num_functions + dupl_extra_edges)
				end_graph.num_edges += (dupl_num_functions + dupl_extra_edges)
				self.merged.num_edges += (dupl_num_functions + dupl_extra_edges)
				TestGraph.replica_nodes.extend(these_ids)

				dupls_added += 1

		single_functions_ind = all_functions_ind[num_duplicate:]
		single_functions = self.large_values[single_functions_ind]

		next_start = 0
		next_end = 0

		for i in range(len(self.dags)):
			next_start = next_end
			next_end += num_functions_per_dag - self.dags[i].num_nodes
			self.complete_dag(single_functions[next_start:next_end], num_layers, num_extra_edges, self.dags[i], self.merged)


		for i in range(len(self.dags)):
				this_dag_nodes = self.dags[i].nodes
				for j in range(len(this_dag_nodes)):
					this_dag_layer_nodes = this_dag_nodes[j]
					for k in range(len(this_dag_layer_nodes)):
						ind_node = this_dag_layer_nodes[k]
						self.dags[i].flat_nodes.append(ind_node)

		for i in range(len(self.merged.nodes)):
			merged_layer_nodes = self.merged.nodes[i]
			for j in range(len(merged_layer_nodes)):
				merge_node = merged_layer_nodes[j]
				self.merged.flat_nodes.append(merge_node)



	def gen_partial_dag(self, this_funcs, gen_num_layers, gen_extra_edges):
		gen_num_functions = len(this_funcs)

		gen_layers = sorted(np.random.choice(gen_num_functions - 1, gen_num_layers - 1, replace=False))
		gen_layers_aug = [layer + 1 for layer in gen_layers]
		gen_layers_aug.append(gen_num_functions)
		gen_layers_aug.insert(0, 0)
		gen_functions = []

		for i in range(len(gen_layers_aug) - 1):

			this_stop = gen_layers_aug[i]
			next_stop = gen_layers_aug[i+1]
			append_list = this_funcs[this_stop:next_stop]
			gen_functions.append(append_list)

		gen_comms = []
		num_edges_done = 0

		for i in range(len(gen_functions) - 1):
			this_stop = len(gen_functions[i])
			next_stop = len(gen_functions[i + 1])
			for j in range(next_stop):
				num_edges_done += 1
				this_ind = np.random.choice(this_stop) + gen_layers_aug[i] # (j % this_stop) + gen_layers_aug[i]
				next_ind = j + gen_layers_aug[i + 1] # (j % next_stop) + gen_layers_aug[i + 1]
				gen_comms.append([this_funcs[this_ind][2], this_funcs[next_ind][2], this_funcs[this_ind][1]])

		num_edges_left = gen_extra_edges + (len(this_funcs) - num_edges_done)

		while(num_edges_left > 0):
			gen_picked_layers = sorted(np.random.choice(len(this_funcs), 2, replace=False))
			first_ind = np.argmax(gen_layers_aug > gen_picked_layers[0])
			second_ind = np.argmax(gen_layers_aug > gen_picked_layers[1])
			if second_ind > first_ind:
				num_edges_left -= 1
				gen_comms.append([this_funcs[gen_picked_layers[0]][2], this_funcs[gen_picked_layers[1]][2], this_funcs[gen_picked_layers[0]][1]])

		dupl_node_list = []
		for i in range(len(this_funcs)):
			dupl_node_list.append(((this_funcs[i]).tolist())[2])

		return (gen_functions, gen_comms, dupl_node_list)


	def complete_dag(self, complete_funcs, complete_layers, complete_extra_edges, partial_graph, total_graph):
		complete_num_functions = len(complete_funcs)

		complete_layers = sorted(np.random.choice(complete_num_functions - 1, len(partial_graph.nodes) - 1, replace=False))
		complete_layers_aug = [layer + 1 for layer in complete_layers]
		complete_layers_aug.append(complete_num_functions)
		complete_layers_aug.insert(0, 0)
		# print("complete Layers")
		# print(complete_layers_aug)

		for i in range(len(complete_layers_aug) - 1):

			complete_stop = complete_layers_aug[i]
			next_stop = complete_layers_aug[i+1]
			append_list = complete_funcs[complete_stop:next_stop]
			partial_graph.nodes[i].extend(append_list)
			total_graph.nodes[i].extend(append_list)

		complete_functions = partial_graph.nodes
		# print(complete_functions)
		# complete_comms = []
		num_edges_done = 0

		# print("complete Functions")
		# print(complete_functions)

		# print("Len Functions")
		# print(len(complete_functions))

		for i in range(len(complete_functions) - 1):
			complete_stop = len(complete_functions[i])
			next_stop = len(complete_functions[i + 1])
			# max_stop = max(complete_stop, next_stop)
			# comm_lengths = np.random.choice(100, next_stop)
			for j in range(next_stop):
				complete_ind = np.random.choice(complete_stop) # np.random.choice(complete_stop) + complete_layers_aug[i] # (j % complete_stop) + complete_layers_aug[i]
				next_ind = j # j + complete_layers_aug[i + 1] # (j % next_stop) + complete_layers_aug[i + 1]
				if(complete_functions[i+1][next_ind][2] not in set(TestGraph.replica_nodes)):
					(partial_graph.edges).append([complete_functions[i][complete_ind][2], complete_functions[i+1][next_ind][2], complete_functions[i][complete_ind][1]])
					(total_graph.edges).append([complete_functions[i][complete_ind][2], complete_functions[i+1][next_ind][2], complete_functions[i][complete_ind][1]])
					num_edges_done += 1

		# print("Num Edges Done")
		# print(num_edges_done)

		num_edges_left = complete_extra_edges + (len(complete_funcs) - num_edges_done)

		while(num_edges_left > 0):
			# print("Select")
			complete_picked_layers = sorted(np.random.choice(len(complete_funcs), 2, replace=False))
			# print(complete_picked_layers)
			# print("First Ind")
			first_ind = np.argmax(complete_layers_aug > complete_picked_layers[0])
			# print(first_ind)
			# print("Second Ind")
			second_ind = np.argmax(complete_layers_aug > complete_picked_layers[1])
			# print(second_ind)
			if (second_ind > first_ind) and complete_funcs[complete_picked_layers[1]][2] not in set(TestGraph.replica_nodes):
				# print("Sucess")
				num_edges_left -= 1
				(partial_graph.edges).append([complete_funcs[complete_picked_layers[0]][2], complete_funcs[complete_picked_layers[1]][2], complete_funcs[complete_picked_layers[0]][1]])
				(total_graph.edges).append([complete_funcs[complete_picked_layers[0]][2], complete_funcs[complete_picked_layers[1]][2], complete_funcs[complete_picked_layers[0]][1]])




