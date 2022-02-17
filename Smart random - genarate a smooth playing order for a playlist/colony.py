import random
import numpy as np
import Ant


class Colony(object):

    def __init__(self, num_of_ants, args, graph, num_of_iter):
        self.graph = graph
        self.T0 = 1 / (self.graph.num_nodes*self.L_nn())  # pheromone init value
        self.num_of_ants = num_of_ants
        self.args = args
        self.best_global_path = None
        self.best_global_path_cost = np.inf
        self.alpha = args['alpha']
        self.beta = args['beta']
        self.ant = None
        self.ro = args['ro']
        self.pheromone = np.empty(self.graph.edges_mat.shape)
        self.pheromone.fill(self.T0)
        self.num_of_iter = num_of_iter
        self.heuristic = np.zeros_like(self.graph.edges_mat)
        self.heuristic = np.divide(1., self.graph.edges_mat, where=self.graph.edges_mat != 0)
        self.iter_costs = []

    def start_search(self): # start the search for the best path
        for i in range(self.num_of_iter):
            sol_path, sol_path_cost = self.constuct_ants_one_solution()
            self.offline_pheromone_update(sol_path,sol_path_cost)
            self.iter_costs.append(sol_path_cost)

    def offline_pheromone_update(self,sol_path,sol_path_cost): # the main pheromones update of only the best path until now

        if sol_path_cost <= self.best_global_path_cost:
            self.best_global_path_cost = sol_path_cost
            self.best_global_path = sol_path
        self.pheromone = (1-self.ro)*self.pheromone
        self.pheromone[self.best_global_path, self.best_global_path[1:] + self.best_global_path[:1]] += self.ro / self.best_global_path_cost

    def constuct_ants_one_solution(self):
        best_path_cost = np.inf
        best_path = None
        for i in range(self.num_of_ants): # bach of ants search
            start_node = random.randint(0, self.graph.num_nodes - 1)
            self.ant = Ant.Ant(start_node, self)
            self.ant.search_path()  # one ant search
            if self.ant.cost < best_path_cost:
                best_path = self.ant.path  # best ant solution
                best_path_cost = self.ant.cost

        return best_path , best_path_cost
    def local_update_pheromone(self,current_node, next_node, val):
        self.pheromone[current_node, next_node] = val

    def L_nn(self): #calculate the distance with a greeday algorithem
        min_cost = np.inf
        min_path = None
        for start in range(self.graph.num_nodes):
            unseen = list(range(self.graph.num_nodes))
            del unseen[start]
            cur = start
            cur_path = [start]
            cost = 0
            for _ in range(self.graph.num_nodes - 1):
                min_cost_idx = int(np.argmin(self.graph.edges_mat[cur, unseen]))
                next_node = unseen[min_cost_idx]
                del unseen[min_cost_idx]
                cur_path.append(next_node)
                cost += self.graph.edges_mat[cur, next_node]
                cur = next_node
            cost += self.graph.edges_mat[cur_path[-1], cur_path[0]]
            if cost < min_cost:
                min_cost = cost
                min_path = cur_path
        print(f"Greedy algorithm cost: {min_cost}")
        return  min_cost
