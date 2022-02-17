import numpy as np
import networkx

class Graph(object):

    def __init__(self, matrix):
        self.num_nodes = matrix.shape[0]
        self.edges_mat = matrix

