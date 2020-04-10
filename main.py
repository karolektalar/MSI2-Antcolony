import copy

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

HEURISTIC = "basic"
HEURISTIC_EXPONENT = 1
PHEROMONE_EXPONENT = 3
EVAPORATE_RATE = 0.6
ANT_CAPACITY = 3


class Ant:
    def __init__(self, graph: np.array, pheromone: np.array, pheromone_delta: np.array , capacity: int, current_position: int):
        self.graph = graph #3 dimensional. First two are markers of the road from first idx to second. In third dim are values of weight of this road, and amount of goods in b
        self.pheromone = pheromone
        self.capacity = capacity
        self.current_position = current_position
        self.list_of_moves = []
        self.pheromone_delta = pheromone_delta
        self.weight_of_moves = 0

    def update_pheromone_local(self, new_position: int):
        delta = abs(self.pheromone[self.current_position, new_position] - (EVAPORATE_RATE * self.pheromone[self.current_position, new_position] + (1-EVAPORATE_RATE)* 1/self.graph[self.current_position, new_position,0]))
        self.pheromone[self.current_position, new_position] += delta
        self.pheromone_delta[self.current_position, new_position] += delta

    def reset(self, graph: np.array):
        self.graph = graph
        self.list_of_moves = []
        self.weight_of_moves = 0
        return self


def calculate_probability(possible_moves: [], graph: np.array, pheromone: np.array):
    probabilities = []
    if HEURISTIC == "basic":
        sum = 0
        for move in possible_moves:
            probabilities.append((graph[ant.current_position][move][0]**HEURISTIC_EXPONENT) *
                                         (pheromone[ant.current_position][move]**PHEROMONE_EXPONENT))
            sum += ((graph[ant.current_position][move][0]**HEURISTIC_EXPONENT) *
                    (pheromone[ant.current_position][move]**PHEROMONE_EXPONENT))
        return [probability / sum for probability in probabilities]


def calculate_move(ant: Ant):
    possible_moves = []
    for idx, move in enumerate(ant.graph[ant.current_position]):
        if idx == 0:
            continue
        if (not move[0] == 0) and move[1] <= ant.capacity and idx != ant.current_position:
            possible_moves.append(idx)
    if len(possible_moves) == 0:
        return 0
    heuristic_probability = calculate_probability(possible_moves, ant.graph, ant.pheromone)
    random_number = np.random.rand()
    for idx, probability in enumerate(heuristic_probability):
        if random_number - probability < 0:
            return possible_moves[idx]
        else:
            random_number -= probability


def ant_move(ant: Ant):
    while np.any(ant.graph):
        move = calculate_move(ant)
        ant.capacity -= ant.graph[ant.current_position][move][1]
        if move == 0:
            ant.list_of_moves.append(0)
            ant.weight_of_moves += ant.graph[ant.current_position][0][0]
            if ant.current_position != 0:
                ant.graph[ant.current_position] = np.zeros((len(ant.graph[0]), 2))
                for element in ant.graph:
                    element[ant.current_position] = np.zeros((2))
                ant.current_position = move
            ant.current_position = 0
            ant.capacity = ANT_CAPACITY
        else:
            ant.list_of_moves.append(move)
            ant.weight_of_moves += ant.graph[ant.current_position][move][0]
            if ant.current_position != 0:
                ant.graph[ant.current_position] = np.zeros((len(ant.graph[0]), 2))
                for element in ant.graph:
                    element[ant.current_position] = np.zeros((2))
            ant.current_position = move
        ant.update_pheromone_local(move)
    return ant


def update_pheromone_after_epoch(ants: list, pheromone_delta: np.array):
    size = ants[0].pheromone.shape[0]

    for ant in ants:
        for i in range(0,size):
            for j in range(0,size):
                ant.pheromone[i,j] = EVAPORATE_RATE * ant.pheromone[i,j] + pheromone_delta[i,j]


if __name__ == "__main__":
    graph = np.random.rand(30, 30, 2)
    pheromone_delta = np.zeros((30,30))
    for idx, element in enumerate(graph):
        for idx2, subelement in enumerate(element):
            if idx == idx2:
                graph[idx][idx2] = np.zeros(2)
    list_of_ants = []
    for i in range(100):
        ant = Ant(copy.deepcopy(graph), np.random.rand(30, 30), pheromone_delta,ANT_CAPACITY, 0)
        list_of_ants.append(ant)

    for i in range(0,51):

        for idx, ant in enumerate(list_of_ants):
            list_of_ants[idx] = ant_move(ant)

        best_weight = list_of_ants[0].weight_of_moves
        worst_weight = list_of_ants[0].weight_of_moves
        best_list_of_moves = list_of_ants[0].list_of_moves
        worst_list_of_moves = list_of_ants[0].list_of_moves
        best_ant = list_of_ants[0]
        for idx, ant in enumerate(list_of_ants):
            if ant.weight_of_moves < best_weight:
                best_weight = ant.weight_of_moves
                best_list_of_moves = ant.list_of_moves
                best_ant = ant
            if ant.weight_of_moves > worst_weight:
                worst_weight = ant.weight_of_moves
                worst_list_of_moves = ant.list_of_moves
            list_of_ants[idx] = ant.reset(copy.deepcopy(graph))

        print(f"WORST WEIGHT at epoch {i}/50 : {str(worst_weight)}")
        #print("WORST MOVES: " + str(worst_list_of_moves))
        print(f"BEST WEIGHT at epoch {i}/50 : {str(best_weight)}")
        #print("BEST MOVES: " + str(best_list_of_moves))
        update_pheromone_after_epoch(list_of_ants, pheromone_delta)
        print("************-------------**************")
        pheromone_delta = np.zeros((30, 30))
