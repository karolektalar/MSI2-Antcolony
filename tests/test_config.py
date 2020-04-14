import numpy as np


class AntConstants:
    def __init__(self, yaml_dict: {}):
        self.number_of_ants = yaml_dict['number_of_ants']


class PheremoneStrategy:
    def __init__(self, yaml_dict: {}):
        self.local_strategy = yaml_dict['local_update_strategy']
        self.global_strategy = yaml_dict['global_update_strategy']


class ElitenessStrategy:
    def __init__(self, yaml_dict: {}):
        self.number_of_elite_ants = yaml_dict['number_of_elite_ants']


class TestGraph:
    def __init__(self, graph_size: int, graph: np.array, capacity: int):
        self.graph_size = graph_size
        self.graph = graph
        self.pheromone = np.random.rand(self.graph_size, self.graph_size)
        self.pheromone_detla = np.zeros((self.graph_size, self.graph_size))
        self.capacity = capacity


class TestCaseConfig:
    def __init__(self, pheromone_strategy: PheremoneStrategy, ant_constants: AntConstants, eliteness_strategy: ElitenessStrategy, yaml_dict: {}, number_of_runs: int):
        self.pheromone_strategy = pheromone_strategy
        self.ant_constants = ant_constants
        self.eliteness_strategy = eliteness_strategy
        self.heuristic = yaml_dict['heuristic']
        self.seed = yaml_dict['seed']
        self.vaporizataion = yaml_dict['vaporization']
        self.exploitation = yaml_dict['exploitation_constant']
        self.heuristic_exp = yaml_dict['heuristic_exponent']
        self.pheromone_exp = yaml_dict['pheromone_exponent']
        self.iterations = number_of_runs
