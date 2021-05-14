#!/usr/bin/env python3

from hastestructures.edge import Edge
from hastestructures.node import Node
from hastestructures.graph import Graph
from hastestructures.execution_sequence import ExecutionSequence
from hastestructures.naive_sched import  Naive_Sched
from hastestructures.lwb import LWB

test_graph = Graph()

test_node_one = Node(1, 4, 0)
test_node_two = Node(2, 3, 0)
test_node_three = Node(3, 2, 0)
test_node_four = Node(4, 2, 0)
test_node_five = Node(5, 2, 0)
test_node_six = Node(6, 3, 0)
test_node_seven = Node(7, 3, 0)
test_node_eight = Node(8, 3, 0)
test_node_nine = Node(9, 1, 0)

test_graph.add_node(test_node_one)
test_graph.add_node(test_node_two)
test_graph.add_node(test_node_three)
test_graph.add_node(test_node_four)
test_graph.add_node(test_node_five)
test_graph.add_node(test_node_six)
test_graph.add_node(test_node_seven)
test_graph.add_node(test_node_eight)
test_graph.add_node(test_node_nine)

test_edge_one_three = test_graph.connect_nodes(1, 3, 3)
test_edge_one_four = test_graph.connect_nodes(1, 4, 2)
test_edge_two_four = test_graph.connect_nodes(2, 4, 1)
test_edge_two_five = test_graph.connect_nodes(2, 5, 1)
test_edge_three_six =  test_graph.connect_nodes(3, 6, 1)
test_edge_three_seven = test_graph.connect_nodes(3, 7, 1)
test_edge_four_six = test_graph.connect_nodes(4, 6, 1)
test_edge_four_eight = test_graph.connect_nodes(4, 8, 1)
test_edge_five_seven = test_graph.connect_nodes(5, 7, 1)
test_edge_five_eight = test_graph.connect_nodes(5, 8, 1)
test_edge_six_nine = test_graph.connect_nodes(6, 9, 2)
test_edge_seven_nine = test_graph.connect_nodes(7, 9, 2)
test_edge_eight_nine = test_graph.connect_nodes(8, 9, 2)

test_naive_sched = Naive_Sched()
test_naive_sched.apply_naive(test_graph)

test_lwb = LWB()

# print((test_graph.get_edge((1, 3))).edge_id)
# print(test_edge_one_three.comm_size)
# print(test_node_one.outgoing[3].edge_id)
print(test_graph.get_start())
print(test_naive_sched.naive_sequence.get_printable())
print(test_lwb.gen_lower_bounds(test_graph))
test_lwb_execs = test_lwb.gen_sequences(test_graph)
for test_lwb_exec in test_lwb_execs:
	print(test_lwb_exec.get_printable())

