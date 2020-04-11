import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
np.random.seed = 1

GRAPH_SIZE = 30
NUMBER_OF_ANTS = 100
# HEURISTIC = "basic"
HEURISTIC = "savings"
# HEURISTIC = "exploitation"
EXPLOITATION_CONSTANT = 0.5
HEURISTIC_EXPONENT = 1
PHEROMONE_EXPONENT = 3
PHEROMONE = np.random.rand(GRAPH_SIZE, GRAPH_SIZE)
EVAPORATE_RATE = 0.6
# PHEROMONE_UPDATE = "basic"
PHEROMONE_UPDATE = "elite"
PHEROMONE_UPDATE_LOCAL = False
NUMBER_OF_ELITE_ANTS = 10
PHEROMONE_EXPONENT = 3

ANT_CAPACITY = 3


class Ant:
    def __init__(self, graph: np.array, pheromone: np.array, pheromone_delta: np.array , capacity: int, current_position: int):
        self.graph = graph #3 wymiarowa tablica, gdzie pierwsze dwa wymiary to współrzedne grafu, a w trzecim trzymana jest odległość i pojemność dobra w docelowym wierzchołku
        self.pheromone = pheromone
        self.capacity = capacity
        self.current_position = current_position
        self.list_of_moves = []
        self.pheromone_delta = pheromone_delta
        self.weight_of_moves = 0

    def update_pheromone_local(self, new_position: int):
        if PHEROMONE_UPDATE_LOCAL:
            delta = abs(self.pheromone[self.current_position, new_position] - (EVAPORATE_RATE * self.pheromone[self.current_position, new_position] + (1-EVAPORATE_RATE)* 1/self.graph[self.current_position, new_position,0]))
            PHEROMONE[self.current_position, new_position] += delta

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
    elif HEURISTIC == "savings":
        sum = 0
        for move in possible_moves:
            probability_for_move = ((graph[ant.current_position][0][0] + graph[0][move][0] -
                                     2 * graph[ant.current_position][move][0] +
                                     2 * abs(graph[ant.current_position][0][0] - graph[0][move][0])) ** HEURISTIC_EXPONENT) * \
                                   (pheromone[ant.current_position][move] ** PHEROMONE_EXPONENT)
            probabilities.append(probability_for_move)
            sum += probability_for_move
        return [probability / sum for probability in probabilities]
    elif HEURISTIC == "exploitation":
        probabilities = []
        if np.random.rand() > EXPLOITATION_CONSTANT:
            best_move = -1
            best_move_idx = 0
            for idx, move in enumerate(possible_moves):
                probabilities.append(0)
                if graph[ant.current_position][move][0] < best_move or best_move == -1:
                    best_move = move
                    best_move_idx = idx
            probabilities[best_move_idx] = 1
            return probabilities
        else:
            sum = 0
            for move in possible_moves:
                probability_for_move = ((graph[ant.current_position][0][0] + graph[0][move][0] -
                                         2 * graph[ant.current_position][move][0] +
                                         2 * abs(
                            graph[ant.current_position][0][0] - graph[0][move][0])) ** HEURISTIC_EXPONENT) * \
                                       (pheromone[ant.current_position][move] ** PHEROMONE_EXPONENT)
                probabilities.append(probability_for_move)
                sum += probability_for_move
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


def update_pheromone_after_epoch(ants: list, pheromone_delta: np.array, pheromone: np.array):
    size = ants[0].pheromone.shape[0]
    if PHEROMONE_UPDATE == "basic":
        for ant in ants:
            previous = ant.list_of_moves[0]
            for move in ant.list_of_moves:
                if not move == previous:
                    pheromone_delta[previous][move] += 1 / ant.weight_of_moves

    if PHEROMONE_UPDATE == "elite":
        best_ant = ants[0]
        for ant in ants:
            if ant.weight_of_moves < best_ant.weight_of_moves:
                best_ant = ant
            previous = ant.list_of_moves[0]
            for move in ant.list_of_moves:
                if not move == previous:
                    pheromone_delta[previous][move] += 1 / ant.weight_of_moves
        for i in range(NUMBER_OF_ELITE_ANTS):
            previous = best_ant.list_of_moves[0]
            for move in best_ant.list_of_moves:
                if not move == previous:
                    pheromone_delta[previous][move] += 1 / best_ant.weight_of_moves

    for i in range(0, size):
        for j in range(0, size):
            pheromone[i, j] = EVAPORATE_RATE * pheromone[i, j] + pheromone_delta[i, j]

    return pheromone


if __name__ == "__main__":
    graph = np.random.rand(GRAPH_SIZE, GRAPH_SIZE, 2)
    pheromone_delta = np.zeros((GRAPH_SIZE,GRAPH_SIZE))
    for idx, element in enumerate(graph):
        for idx2, subelement in enumerate(element):
            if idx == idx2:
                graph[idx][idx2] = np.zeros(2)
    list_of_ants = []
    for i in range(NUMBER_OF_ANTS):
        ant = Ant(copy.deepcopy(graph), PHEROMONE, pheromone_delta, ANT_CAPACITY, 0)
        list_of_ants.append(ant)

    current_best_weight = 10000

    for i in range(50):
        for idx, ant in enumerate(list_of_ants):
            list_of_ants[idx] = ant_move(ant)

        best_weight = list_of_ants[0].weight_of_moves
        worst_weight = list_of_ants[0].weight_of_moves
        best_list_of_moves = list_of_ants[0].list_of_moves
        worst_list_of_moves = list_of_ants[0].list_of_moves

        for idx, ant in enumerate(list_of_ants):
            if ant.weight_of_moves < best_weight:
                best_weight = ant.weight_of_moves
                best_list_of_moves = ant.list_of_moves
                best_ant = ant
            if ant.weight_of_moves > worst_weight:
                worst_weight = ant.weight_of_moves
                worst_list_of_moves = ant.list_of_moves

        print(f"WORST WEIGHT at epoch {i}/50 : {str(worst_weight)}")
        #print("WORST MOVES: " + str(worst_list_of_moves))
        print(f"BEST WEIGHT at epoch {i}/50 : {str(best_weight)} loss = {current_best_weight - best_weight})")
        #print("BEST MOVES: " + str(best_list_of_moves))

        if current_best_weight > best_weight:
            current_best_weight = best_weight
            current_best_list_of_moves = best_list_of_moves

        PHEROMONE = update_pheromone_after_epoch(list_of_ants, pheromone_delta, PHEROMONE)
        print("************-------------**************")
        pheromone_delta = np.zeros((GRAPH_SIZE, GRAPH_SIZE))
        list_of_ants = []
        for tmp in range(NUMBER_OF_ANTS):
            ant = Ant(copy.deepcopy(graph), PHEROMONE, pheromone_delta, ANT_CAPACITY, 0)
            list_of_ants.append(ant)

    print("BEST MOVES: " + str(current_best_weight))
    print("BEST MOVES: " + str(current_best_weight))

