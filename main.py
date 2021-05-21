#!/usr/bin/env python3

import math
import numpy as np
import pandas as pd

from hastestructures.edge import Edge
from hastestructures.node import Node
from hastestructures.graph import Graph
from hastestructures.execution_sequence import ExecutionSequence
from hastestructures.naive_sched import  Naive_Sched
from hastestructures.lwb import LWB
from hastestructures.graph_gen import GraphGen
from hastestructures.workload_gen import WorkloadGen
from hastestructures.test_graph import TestGraph

naive_exec_times = []
naive_compute_times = []
lwb_exec_times = []
lwb_compute_times = []
single_compute_times = []

def gen_data(num_functions, num_layers, num_extra_edges):

	data_gen = GraphGen()
	data_gen.generate_graph(num_functions, num_layers, num_extra_edges)

	data_graph = Graph()
	total_mem = 0

	for i in range(len(data_gen.flattened_functions)):
		data_func = data_gen.flattened_functions[i]
		this_func_data = np.random.choice(100) + 1
		total_mem += this_func_data
		data_node = Node(i, data_func, this_func_data)
		data_graph.add_node(data_node)

	# print("Total Mem")
	# print(total_mem)

	for i in range(len(data_gen.comms)):
		data_comm = data_gen.comms[i]
		data_graph.connect_nodes(data_comm[0], data_comm[1], data_comm[2])

	data_naive_sched = Naive_Sched()
	data_naive_sched.apply_naive(data_graph)

	data_lwb = LWB()
	data_lwb.gen_lower_bounds(data_graph)
	data_lwb_execs = data_lwb.gen_sequences(data_graph)
	num_stream = 0
	max_lwb = 0
	max_data = 0
	for data_lwb_exec in data_lwb_execs:
		num_stream += 1
		max_lwb = max(max_lwb, data_lwb_exec.get_last_end())

	counts = [[0,0], [0,0], [0,0], [0,0]]

	# print("Num Streams: ")
	# print(num_stream)

	# print("Ind mem:")

	for data_lwb_exec in data_lwb_execs:
		amount_mem = 10 * data_lwb_exec.get_data_used()
		# print(amount_mem)
		num_proc = min(math.floor(total_mem / amount_mem), 3)
		# print(num_proc)
		counts[num_proc][0] += 1
		counts[num_proc][1] += data_lwb_exec.get_last_end()



	# compute_time_used = (counts[0][1] / (counts[0][0] + 1)) + (counts[1][1] / ((counts[1][0] + 1) * 2)) + (counts[2][1] / ((counts[2][0] + 1) * 3)) + (counts[3][1] / ((counts[3][0] + 1) * 4))
	compute_time_used = counts[0][1] + counts[1][1] / 2 + counts[2][1] / 3 + counts[3][1] / 4
	# print(counts[0][0] +  counts[1][0] + counts[2][0] + counts[3][0])
	# print("Compute Times: ")
	# print(compute_time_used)

	# print("Potential Compute Times: ")
	# print(max_lwb * num_stream)

	 	# print(data_lwb_exec.get_printable())
	# print("Execution Times:")
	# print(max_lwb)
	# print(data_naive_sched.naive_sequence.get_last_end())
	# naive_exec_times.append(data_naive_sched.naive_sequence.get_last_end())
	naive_compute_times.append(max_lwb * num_stream)
	# lwb_exec_times.append(max_lwb)
	lwb_compute_times.append(compute_time_used)
	single_compute_times.append(data_naive_sched.naive_sequence.get_last_end())


test_workload = WorkloadGen()
test_workload.generate_workload(10, 0.1, 1000, 5, 50, 10, 3, 0)

data_graph = Graph()
total_mem = 0

for i in range(len(test_workload.merged.flat_nodes)):
	data_func = test_workload.merged.flat_nodes[i]
	total_mem += data_func[1]
	data_node = Node(data_func[2], data_func[0], data_func[1])
	data_graph.add_node(data_node)


for i in range(len(test_workload.merged.edges)):
	data_comm = test_workload.merged.edges[i]
	data_graph.connect_nodes(data_comm[0], data_comm[1], data_comm[2])


data_naive_sched = Naive_Sched()
data_naive_sched.apply_naive(data_graph)


data_lwb = LWB()
data_lwb.gen_lower_bounds(data_graph)
data_lwb_execs = data_lwb.gen_sequences(data_graph)
num_stream = 0
max_lwb = 0
max_data = 0
for data_lwb_exec in data_lwb_execs:
	num_stream += 1
	max_lwb = max(max_lwb, data_lwb_exec.get_last_end())

print(data_naive_sched.naive_sequence.get_last_end())
print(max_lwb)



# for i in range(100):
# 	gen_data(100, 5, 50)

# # print(naive_exec_times)
# print(naive_compute_times)
# # print(lwb_exec_times)
# print(lwb_compute_times)
# print(single_compute_times)
	








# print((test_graph.get_edge((1, 3))).edge_id)
# print(test_edge_one_three.comm_size)
# print(test_node_one.outgoing[3].edge_id)
# print(test_graph.get_start())
# print(test_naive_sched.naive_sequence.get_printable())
# print(test_lwb.gen_lower_bounds(test_graph))
# test_lwb_execs = test_lwb.gen_sequences(test_graph)
# for test_lwb_exec in test_lwb_execs:
# 	print(test_lwb_exec.get_printable())

# print(test_gen.functions)
# print(test_gen.comms)
# print(test_gen.flattened_functions)

