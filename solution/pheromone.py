from solution.config import PHEROMONE_UPDATE, NUMBER_OF_ELITE_ANTS, EVAPORATE_RATE
import numpy as np
from solution.ant import Ant


def update_pheromone_after_epoch(ants: list, pheromone_delta: np.array, pheromone: np.array):
    size = ants[0].pheromone.shape[0]

    if PHEROMONE_UPDATE == 'basic':
        for ant in ants:
            ant.update_pheromone_on_path(delta= pheromone_delta)

    if PHEROMONE_UPDATE == "elite":
        best_ant = ants[0]

        for ant in ants:
            if ant.weight_of_moves < best_ant.weight_of_moves:
                best_ant = ant
            ant.update_pheromone_on_path(delta= pheromone_delta)

        for i in range(NUMBER_OF_ELITE_ANTS):
            best_ant.update_pheromone_on_path(delta= pheromone_delta)

    for i in range(0, size):
        for j in range(0, size):
            pheromone[i, j] = EVAPORATE_RATE * pheromone[i, j] + pheromone_delta[i, j]

    return pheromone


def update_pheromone_from_the_best_solution(ant: Ant, pheromone_delta: np.array, pheromone: np.array):
    size = ant.pheromone.shape[0]

    ant.update_pheromone_on_path(delta= pheromone_delta)

    for i in range(size):
        for j in range(size):
            pheromone[i, j] = EVAPORATE_RATE * pheromone[i, j] + pheromone_delta[i, j]

    return pheromone
