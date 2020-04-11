from solution.ant import Ant
import numpy as np

from solution.config import ANT_CAPACITY

from solution.move_probability import calculate_probability


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


def calculate_move(ant: Ant):
    possible_moves = []
    for idx, move in enumerate(ant.graph[ant.current_position]):
        if idx == 0:
            continue
        if (not move[0] == 0) and move[1] <= ant.capacity and idx != ant.current_position:
            possible_moves.append(idx)
    if len(possible_moves) == 0:
        return 0
    heuristic_probability = calculate_probability(ant = ant, possible_moves= possible_moves)
    random_number = np.random.rand()
    for idx, probability in enumerate(heuristic_probability):
        if random_number - probability < 0:
            return possible_moves[idx]
        else:
            random_number -= probability
