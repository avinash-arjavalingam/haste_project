#!/usr/bin/env python3

from .execution_sequence import ExecutionSequence
from .graph import Graph


class LWB:

	def __init__(self):
		self.sequence_list = []
		self.lower_map = {}

	def get_max_pred(self, this_node, input_graph, seen_set):
		max_id = None
		max_value = 0
		for in_edge_id, in_edge in this_node.incoming.items():
			in_node = in_edge.tail
			if in_node.node_id not in seen_set:
				comp_value = in_node.bound + in_node.exec_time + in_edge.comm_size
				# print(str(this_node.node_id) + ": " + str(in_node.node_id) + " and " + str(comp_value))
				if (comp_value > max_value):
					max_value = comp_value
					max_id = in_node.node_id

		return (max_id, max_value)


	def gen_lower_bounds(self, input_graph):
		lower_bound_map = {}
		start_output = input_graph.get_start()
		ready_nodes = start_output[0]
		not_ready_nodes = start_output[1]

		while(len(ready_nodes) > 0):
			next_node = input_graph.get_node(ready_nodes.pop(0))
			highest_set = {}
			max_ret = self.get_max_pred(next_node, input_graph, highest_set)
			next_bound = 0

			if max_ret[0] is not  None:
				max_node = input_graph.get_node(max_ret[0])
				max_no_comm = max_node.bound + max_node.exec_time
				highest_set[max_ret[0]] = max_ret[1]
				second_ret = self.get_max_pred(next_node, input_graph, highest_set)
				tru_max = max(max_no_comm, second_ret[1])
				next_bound = tru_max
			
			next_node.bound = next_bound
			lower_bound_map[next_node.node_id] = next_node.bound

			for out_edge_id, out_edge in next_node.outgoing.items():
				out_node = out_edge.head
				out_node.dep_finished -= 1
				if out_node.dep_finished == 0:
					ready_nodes.append(out_node.node_id)
					not_ready_nodes.remove(out_node.node_id)

		self.lower_map = lower_bound_map
		return lower_bound_map

	def gen_sequences(self, input_graph):
		lower_list = []
		for lower_node_id, lower_bound in self.lower_map.items():
			lower_list.append([lower_node_id, lower_bound])

		sort_lower_list = sorted(lower_list, key=lambda node_tuple: -1 * node_tuple[1])
		sort_lower_index = [lower_item[0] for lower_item in sort_lower_list]

		all_paths = []


		while(len(sort_lower_index) > 0):
			highest_node = input_graph.get_node(sort_lower_index.pop(0))

			crit_path = [highest_node.node_id]
			back_node = highest_node
			go_back = True
			while(go_back):
				go_back = False
				for in_edge_id, in_edge in back_node.incoming.items():
					in_node = in_edge.tail
					if (in_node.bound + in_node.exec_time + in_edge.comm_size > back_node.bound):
						go_back = True
						crit_path.insert(0, in_node.node_id)
						back_node = in_node
						if in_node.node_id in sort_lower_index:
							sort_lower_index.remove(in_node.node_id)
						break

			all_paths.append(crit_path)

		all_execs = []
		exec_id_iter = 0

		for single_path in all_paths:
			single_exec = ExecutionSequence(exec_id_iter)
			exec_id_iter += 1
			for single_ind in single_path:
				single_exec.append_exec_node(input_graph.get_node(single_ind), self.lower_map[single_ind])

			all_execs.append(single_exec)

		return all_execs
				