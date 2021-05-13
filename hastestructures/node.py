#!/usr/bin/env python3

class Node:

	def __init__(self, node_id, exec_time, max_alloc):
		self.node_id = node_id
		self.exec_time = exec_time
		self.max_alloc = max_alloc

		self.incoming = {}
		self.outgoing = {}

		self.dep_wait = 0


