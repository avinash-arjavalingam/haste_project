#!/usr/bin/env python3

from .node import Node
from .edge import Edge


class Graph:

	def __init__(self):
		self.nodes = {}
		self.edges = {}

	def get_node(self, node_id):
		return self.nodes[node_id]

	def get_edge(self, edge_id):
		return self.edges[edge_id]


	def add_node(self, new_node):
		self.nodes[new_node.node_id] = new_node

	def connect_nodes(self, tail_node_id, head_node_id, edge_comm_size):
		tail_node = self.nodes[tail_node_id]
		head_node = self.nodes[head_node_id]
		this_edge = Edge(tail_node, head_node, edge_comm_size)
		tail_node.outgoing[head_node_id] = this_edge
		head_node.incoming[tail_node_id] = this_edge
		self.edges[this_edge.edge_id] = this_edge
		return this_edge

	def get_start(self):
		start_nodes_list = []
		not_start_nodes_list = []
		for node_id, node in self.nodes.items():
			node.dep_finished = len(node.incoming)
			if node.dep_finished == 0:
				start_nodes_list.append(node_id)

			else:
				not_start_nodes_list.append(node_id)

		return (start_nodes_list, not_start_nodes_list)