import numpy as np
from tests.test_config import TestCaseConfig

class Config:
    def __init__(self, seed: np.random.seed, graph_size: int, number_of_ants:int, pheromone : np.random.rand, global_updates_strategy: str, local_update_strategy: str, heuristic: str,capacity: int, exploit_const, heuristic_exp: float, pheromone_exp: float, evap_rate: float, number_of_elite_ants: int):
        self.seed = seed
        self.graph_size = graph_size
        self.number_of_ants = number_of_ants
        self.heuristic = heuristic
        self.exploiot_const = exploit_const
        self.heuristic_exp = heuristic_exp
        self.pheromone_exp = pheromone_exp
        self.pheromone = pheromone
        self.evaporate_rate = evap_rate
        self.global_update_strat = global_updates_strategy
        self.number_of_elite_ants = number_of_elite_ants
        self.ant_capacity = capacity
        self.local_update_strategy = local_update_strategy

    @classmethod
    def from_test_config(cls, config: TestCaseConfig, pheromone: np.array):
        return cls(config.seed, config.graph_size, config.ant_constants.number_of_ants, pheromone, config.pheromone_strategy.global_strategy, config.pheromone_strategy.local_strategy, config.heuristic, config.ant_constants.ant_capacity, config.exploitation, config.hueristic_exp, config.pheromone_exp, config.vaporizataion, config.eliteness_strategy.number_of_elite_ants)
