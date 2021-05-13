#!/usr/bin/env python3

from .node import Node
from .execution_node import ExecutionNode

class ExecutionSequence:

	def __init__(self, exec_id):
		self.exec_id = exec_id
		self.nodelist = []


	def append_exec_node(self, this_node, start_time):
		new_exec_node = ExecutionNode(this_node, start_time)
		self.nodelist.append(new_exec_node)
		return self.nodelist[-1].end_time

	def get_printable(self):
		printable_list = []
		for exec_node in self.nodelist:
			printable_list.append("Node ID: " + str(exec_node.this_node_id) + ", Start Time: " + str(exec_node.start_time) + ", End Time: " + str(exec_node.end_time))
		return printable_list