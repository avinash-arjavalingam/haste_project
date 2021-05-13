#!/usr/bin/env python3

from .execution_sequence import ExecutionSequence
from .graph import Graph

class Naive_Sched:

	def __init__(self):
		self.naive_sequence = ExecutionSequence(0)

	def apply_naive(self, input_graph):
		next_time = 0
		start_output = input_graph.get_start()
		ready_nodes = start_output[0]
		not_ready_nodes = start_output[1]

		while(len(ready_nodes) > 0):
			next_node = input_graph.get_node(ready_nodes.pop(0))
			next_time = self.naive_sequence.append_exec_node(next_node, next_time)
			for out_edge_id, out_edge in next_node.outgoing.items():
				out_node = out_edge.head
				out_node.dep_finished -= 1
				if out_node.dep_finished == 0:
					ready_nodes.append(out_node.node_id)
					not_ready_nodes.remove(out_node.node_id)