import copy

from solution.config import Config
from solution.ant import Ant
import numpy as np


def calculate_probability_basic_heuristic(ant: Ant, possible_moves: [], graph: np.array, pheromone: np.array, config: Config):
    probabilities = []

    sum = 0
    for move in possible_moves:
        probabilities.append(((1/(graph[ant.current_position][move][0])) ** config.heuristic_exp) *
                             (pheromone[ant.current_position][move] ** config.pheromone_exp))
        sum += (((1/(graph[ant.current_position][move][0])) ** config.heuristic_exp) *
                             (pheromone[ant.current_position][move] ** config.pheromone_exp))

    if sum == 0:
        return [1/len(possible_moves) for probability in probabilities]
    return [probability / sum for probability in probabilities]


def calculate_probability_savings_heuristic(ant: Ant, possible_moves: [], graph: np.array, pheromone: np.array, config: Config):
    probabilities = []
    sum = 0
    for move in possible_moves:
        probability_for_move = ((1/(graph[ant.current_position][0][0] + graph[0][move][0] -
                                 2 * graph[ant.current_position][move][0] +
                                 2 * abs(
                    graph[ant.current_position][0][0] - graph[0][move][0])) ** config.heuristic_exp)) * \
                               (pheromone[ant.current_position][move] ** config.pheromone_exp)
        probabilities.append(probability_for_move)
        sum += probability_for_move
    if sum == 0:
        return [1/len(possible_moves) for probability in probabilities]
    return [probability / sum for probability in probabilities]


def calculate_probability_exploitation_heuristic(ant: Ant, possible_moves: [], graph: np.array, pheromone: np.array, config: Config):
    probabilities = []
    if np.random.rand() > config.exploiot_const:
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
                        graph[ant.current_position][0][0] - graph[0][move][0])) ** config.heuristic_exp) * \
                                   (pheromone[ant.current_position][move] ** config.pheromone_exp)
            probabilities.append(probability_for_move)
            sum += probability_for_move
        return [probability / sum for probability in probabilities]


def calculate_probability(ant: Ant, possible_moves: [], config: Config):
    if ant.heuristic == "basic":
        return calculate_probability_basic_heuristic(ant, possible_moves, ant.graph, ant.pheromone, config)
    elif ant.heuristic == "savings":
        return calculate_probability_savings_heuristic(ant, possible_moves, ant.graph, ant.pheromone, config)
    elif ant.heuristic == "exploitation":
        return calculate_probability_exploitation_heuristic(ant, possible_moves, ant.graph, ant.pheromone, config)
