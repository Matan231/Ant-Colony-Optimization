
import math
import Ant
import colony
import graph
import numpy as np
import pandas as pd
import operator
import matplotlib.pyplot as plt
num_of_iter = 400
num_of_ants = 20
file_name = './data/berlin52.txt'

def main():
    # the results are highly dependant on the parameters of the algorithm!

    cost_matrix, points = city_file_parser_to_cost_matrix(file_name)
    args = {}
    args['alpha'] = 1.  # the pheromones importance wight
    args['beta'] = 2.   # the heuristic ( 1/distance of local edge) importance wight
    args['ro'] = 0.1    # the evaporation rate
    args['q0'] = 0.9    # the exploitation vs exploration parameter

    G = graph.Graph(cost_matrix)
    ant_colony = colony.Colony(num_of_ants, args, G, num_of_iter)
    ant_colony.start_search()
    print(f"the best path found: {ant_colony.best_global_path}")
    print(f"the best path Total distance: {ant_colony.best_global_path_cost}")
    plot(points, ant_colony.best_global_path, ant_colony.iter_costs)

def city_distance(city1, city2):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def city_file_parser_to_cost_matrix(file_name): # parsing the point coordinates from the files to a distances matrix
    cities = []
    points = []
    with open(file_name) as f:
        for line in f.readlines():
            city = line.split(' ')
            cities.append(dict(index=float(city[0]), x=float(city[1]), y=float(city[2])))
            points.append((float(city[1]), float(city[2])))
    cost_matrix = []
    rank = len(cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(city_distance(cities[i], cities[j]))
        cost_matrix.append(row)

    cost_matrix = np.array(cost_matrix)
    return cost_matrix, points

def plot(points, path, cost_list):  # plotting the points and the best tour of the algorithm between all of them and back and the distance as a function of the number of iterations
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])

    plt.plot(x, y, 'co')

    for _ in range(0, len(path)):
        i = path[_ - 1]
        j = path[_]

        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)

    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.title(f"My Total Distance: {cost_list[-1]}")
    plt.show()
    plt.plot( [i+1 for i in range(len(cost_list))],cost_list)
    plt.show()
if __name__ == '__main__':
    main()

