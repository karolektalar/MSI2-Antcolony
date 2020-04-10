import copy

import numpy as np

HEURISTIC = "basic"
HEURISTIC_EXPONENT = 1
PHEROMONE_EXPONENT = 3
ANT_CAPACITY = 3

class Ant:
    def __init__(self, graph: np.array, pheromone: np.array, capacity: int, current_position: int):
        self.graph = graph #3 dimensional. First two are markers of the road from first idx to second. In third dim are values of weight of this road, and amount of goods in b
        self.pheromone = pheromone
        self.capacity = capacity
        self.current_position = current_position
        self.list_of_moves = []
        self.weight_of_moves = 0


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
    return ant

if __name__ == "__main__":
    graph = np.random.rand(30, 30, 2)
    for idx, element in enumerate(graph):
        for idx2, subelement in enumerate(element):
            if idx == idx2:
                graph[idx][idx2] = np.zeros(2)
    list_of_ants = []
    for i in range(100):
        ant = Ant(copy.deepcopy(graph), np.random.rand(30, 30), ANT_CAPACITY, 0)
        ant = ant_move(ant)
        list_of_ants.append(ant)

    best_weight = list_of_ants[0].weight_of_moves
    worst_weight = list_of_ants[0].weight_of_moves
    best_list_of_moves = list_of_ants[0].list_of_moves
    worst_list_of_moves = list_of_ants[0].list_of_moves
    for idx, a in enumerate(list_of_ants):
        if a.weight_of_moves < best_weight:
            best_weight = a.weight_of_moves
            best_list_of_moves = a.list_of_moves
        if a.weight_of_moves > worst_weight:
            worst_weight = a.weight_of_moves
            worst_list_of_moves = a.list_of_moves
    print("WORST WEIGHT: " + str(worst_weight))
    print("WORST MOVES: " + str(worst_list_of_moves))
    print("BEST WEIGHT: " + str(best_weight))
    print("BEST MOVES: " + str(best_list_of_moves))
