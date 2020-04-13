import numpy as np
from solution.ant import Ant
from solution.config import Config


def update_pheromone_after_epoch(ants: list, pheromone_delta: np.array, pheromone: np.array, config: Config):
    size = len(ants[0].pheromone)
    if config.local_update_strategy == 'basic':
        for ant in ants:
            ant.update_pheromone_on_path(delta= pheromone_delta)

    if config.local_update_strategy == "elite":
        best_ant = ants[0]

        for ant in ants:
            if ant.weight_of_moves < best_ant.weight_of_moves:
                best_ant = ant
            ant.update_pheromone_on_path(delta = pheromone_delta)

        for i in range(config.number_of_elite_ants):
            best_ant.update_pheromone_on_path(delta= pheromone_delta)

    for i in range(0, size):
        for j in range(0, size):
            pheromone[i][j] = config.evaporate_rate * pheromone[i][j] + pheromone_delta[i][j]

    return pheromone


def update_pheromone_from_the_best_solution(ant: Ant, pheromone_delta: np.array, pheromone: np.array, config: Config):
    size = ant.pheromone.shape[0]

    ant.update_pheromone_on_path(delta= pheromone_delta)

    for i in range(size):
        for j in range(size):
            pheromone[i][j] = config.evaporate_rate * pheromone[i][j] + pheromone_delta[i][j]

    return pheromone
