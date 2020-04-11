from solution.config import HEURISTIC_EXPONENT, PHEROMONE_EXPONENT, EXPLOITATION_CONSTANT
from solution.ant import Ant
import numpy as np


def calculate_probability_basic_heuristic(ant: Ant, possible_moves: [], graph: np.array, pheromone: np.array):
    probabilities = []

    sum = 0
    for move in possible_moves:
        probabilities.append((graph[ant.current_position][move][0] ** HEURISTIC_EXPONENT) *
                             (pheromone[ant.current_position][move] ** PHEROMONE_EXPONENT))
        sum += ((graph[ant.current_position][move][0] ** HEURISTIC_EXPONENT) *
                (pheromone[ant.current_position][move] ** PHEROMONE_EXPONENT))
    return [probability / sum for probability in probabilities]


def calculate_probability_savings_heuristic(ant: Ant, possible_moves: [], graph: np.array, pheromone: np.array):
    probabilities = []
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


def calculate_probability_exploitatioin_heuristic(ant: Ant, possible_moves: [], graph: np.array, pheromone: np.array):
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


def calculate_probability(ant: Ant, possible_moves: []):
    if ant.heuristic == "basic":
        return calculate_probability_basic_heuristic(ant, possible_moves, ant.graph, ant.pheromone)
    elif ant.heuristic == "savings":
        return calculate_probability_savings_heuristic(ant, possible_moves, ant.graph, ant.pheromone)
    elif ant.heuristic == "exploitation":
        return calculate_probability_exploitatioin_heuristic(ant, possible_moves, ant.graph, ant.pheromone)
