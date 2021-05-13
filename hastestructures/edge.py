#!/usr/bin/env python3

from .node import Node

class Edge:

	def __init__(self, tail, head, comm_size):
		self.tail = tail
		self.head = head
		self.comm_size = comm_size

		self.edge_id = (tail.node_id, head.node_id)