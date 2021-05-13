#!/usr/bin/env python3

from .node import Node

class ExecutionNode:

		def __init__(self, this_node, start_time):
			self.this_node = this_node
			self.start_time = start_time

			self.end_time = self.start_time + this_node.exec_time
			self.this_node_id = this_node.node_id
			self.send_exec_ids = []