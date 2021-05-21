#!/usr/bin/env python3

import math
import numpy as np
import pandas as pd

class TestGraph:
    
    replica_nodes = []
    
    def __init__(self, test_layers):
        self.node_map = {}
        self.num_nodes = 0
        self.nodes = []
        self.num_edges = 0
        self.edges = []
        self.flat_nodes = []
        
        for i in range(test_layers):
            self.nodes.append([])