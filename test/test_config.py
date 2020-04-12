
class AntConstants:
    def __init__(self, yaml_dict: {}):
        self.ant_capacity = yaml_dict['ant_capacity']
        self.number_of_ants = yaml_dict['number_of_ants']


class PheremoneStrategy:
    def __init__(self, yaml_dict: {}):
        self.local_strategy = yaml_dict['local_update_strategy']
        self.global_strategy = yaml_dict['global_update_strategy']


class ElitenessStrategy:
    def __init__(self, yaml_dict: {}):
        self.number_of_elite_ants = yaml_dict['number_of_elite_ants']


class TestCaseConfig:
    def __init__(self, pheromone_strategy: PheremoneStrategy, ant_constants: AntConstants, eliteness_strategy: ElitenessStrategy,yaml_dict: {}):
        self.pheromone_strategy = pheromone_strategy
        self.ant_constants = ant_constants
        self.eliteness_strategy = eliteness_strategy
        self.heuristic = yaml_dict['heuristic']
        self.graph_size = yaml_dict['graph_size']
        self.seed = yaml_dict['seed']
        self.vaporizataion = yaml_dict['vaporization']
        self.exploitation = yaml_dict['exploitation_constant']
        self.hueristic_exp = yaml_dict['heuristic_exponent']
        self.pheromone_exp = yaml_dict['pheromone_exponent']
