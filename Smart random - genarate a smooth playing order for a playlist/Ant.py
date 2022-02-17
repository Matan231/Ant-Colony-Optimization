import numpy as np
import random

class Ant(object):

    def __init__(self, start_node, colony):
        self.start_node = start_node # ant starting node
        self.colony = colony # the ant colony
        self.cur_node = start_node # current node of the ant
        self.graph = colony.graph
        self.path = [start_node]  # the entire path
        self.cost = 0  # total cost of the entire path
        self.q0 = colony.args['q0']  # exploration vs exploitation rate
        self.ev_rate = colony.ro  # evaporation rate
       # self.local = local  # local update

        self.num_nodes = self.graph.num_nodes
        self.unseen_nodes = list(range(self.graph.num_nodes))
        self.unseen_nodes.remove(self.start_node)  # mark the start node as seen

    def search_path(self,): # complete search tour of one ant
        while len(self.unseen_nodes) > 0:
            next_node = self.next(self.cur_node)  # find the next node
            self.local_pheromone_update(self.cur_node, next_node)  # update the pheromone level at the local edge
            self.cost += self.graph.edges_mat[self.cur_node, next_node]  # update the total cost of the path
            self.path.append(next_node)
            self.cur_node = next_node


        self.cost += self.graph.edges_mat[self.path[-1], self.path[0]]  # adding the cost of the last edge the edge from the end to the start

        if self.cost < self.colony.best_global_path_cost:
            self.local_search()


    def next(self, current_node): # ant choosing the next node to go to

        # 1, ant choosing of next node
        next_prob = ((self.colony.pheromone[current_node, self.unseen_nodes] ** self.colony.alpha) * self.colony.heuristic[current_node, self.unseen_nodes] ** self.colony.beta)
        next_node_prob_sum = next_prob.sum()
        if next_node_prob_sum == 0.:
            normed_next_prob = np.ones_like(next_prob) / next_prob.shape[0]
        else:
            normed_next_prob = next_prob / next_node_prob_sum

        # state transition rule

        if random.random() < self.q0: #  exploitaition
            max_value_idx = np.argmax(next_prob)
            next_node = self.unseen_nodes[max_value_idx]
        else:  # exploration
            next_node = random.choices(self.unseen_nodes, weights=normed_next_prob)[0]
        self.unseen_nodes.remove(next_node)  # mark the next node as seen.
        return next_node

    def local_pheromone_update(self, current_node, next_node):  # the local pheromones update an ant is making while touring the edges.
        val = (1 - self.ev_rate) * self.colony.pheromone[current_node, next_node] + self.ev_rate * self.colony.T0
        self.colony.local_update_pheromone(current_node, next_node, val)

    def local_search(self):
        # 2-exchange
        best_path = self.path
        best_cost = self.cost
        for i in range(self.num_nodes - 2):
            for j in range(i + 2, self.num_nodes):
                new_path = self.path[:i + 1] + list(reversed(self.path[i + 1:j + 1])) + self.path[j + 1:]
                new_cost = self.graph.edges_mat[new_path, new_path[1:] + new_path[:1]].sum()
                if new_cost < best_cost:
                    best_path = new_path
                    best_cost = new_cost

        self.path = best_path
        self.cost = best_cost

