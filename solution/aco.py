import copy

import yaml
from test.test_config import AntConstants, PheremoneStrategy, ElitenessStrategy, TestCaseConfig

from solution.ant import Ant
from solution.move import ant_move
from solution.pheromone import update_pheromone_after_epoch, update_pheromone_from_the_best_solution
from solution.config import Config
import numpy as np

GRAPH_SIZE = 30
NUMBER_OF_ANTS = 100

# HEURISTIC = "basic"
# HEURISTIC = "exploitation"

HEURISTIC = "savings"

EXPLOITATION_CONSTANT = 0.5
HEURISTIC_EXPONENT = 1
PHEROMONE_EXPONENT = 3
PHEROMONE = np.random.rand(GRAPH_SIZE, GRAPH_SIZE)
EVAPORATE_RATE = 0.6

#PHEROMONE_UPDATE = "basic"
PHEROMONE_UPDATE = "elite"

GLOBAL_UPDATE_STRATEGY = "best_solution"
# GLOBAL_UPDATE_STRATEGY = "all_solutions"

NUMBER_OF_ELITE_ANTS = 10

ANT_CAPACITY = 3


class ACO:
    def __init__(self, config: Config):
        self.config = config
        self.graph_size = config.graph_size
        self.global_update_strategy = config.global_update_strat
        self.graph = np.random.rand(self.graph_size, self.graph_size, 2)
        self.pheromone_delta = np.zeros((self.graph_size, self.graph_size))
        self.capacity = config.ant_capacity
        self.heuristic = config.heuristic
        self.number_of_ants = config.number_of_ants
        self.pheromone = config.pheromone
        self.current_best_weight = 10000

        for idx, element in enumerate(self.graph):
            for idx2, subelement in enumerate(element):
                if idx == idx2:
                    self.graph[idx][idx2] = np.zeros(2)
        self.list_of_ants = []
        for i in range(self.number_of_ants):
            ant = Ant(graph=copy.deepcopy(self.graph), pheromone=self.pheromone, capacity=self.capacity, current_position=0,
                      heuristic=self.heuristic)
            self.list_of_ants.append(ant)

    def run(self):
        for i in range(50):
            for idx, ant in enumerate(self.list_of_ants):
                self.list_of_ants[idx] = ant_move(ant,self.config)

            best_weight = self.list_of_ants[0].weight_of_moves
            worst_weight = self.list_of_ants[0].weight_of_moves
            best_list_of_moves = self.list_of_ants[0].list_of_moves
            worst_list_of_moves = self.list_of_ants[0].list_of_moves
            best_ant = self.list_of_ants[0]

            for idx, ant in enumerate(self.list_of_ants):
                if ant.weight_of_moves < best_weight:
                    best_weight = ant.weight_of_moves
                    best_list_of_moves = ant.list_of_moves
                    best_ant = ant
                if ant.weight_of_moves > worst_weight:
                    worst_weight = ant.weight_of_moves
                    worst_list_of_moves = ant.list_of_moves

            loss = self.current_best_weight - best_weight

            if loss > 0:
                print(f"WORST WEIGHT at epoch {i}/50 : {str(worst_weight)}")
                # print("WORST MOVES: " + str(worst_list_of_moves))
                print(f"BEST WEIGHT at epoch {i}/50 : {str(best_weight)} loss = {loss})")
                # print("BEST MOVES: " + str(best_list_of_moves))
                print("************-------------**************")

            if self.current_best_weight > best_weight:
                self.current_best_weight = best_weight
                self.current_best_list_of_moves = best_list_of_moves

            if self.global_update_strategy == 'best_solution':
                self.pheromone = update_pheromone_from_the_best_solution(best_ant, self.pheromone, self.pheromone_delta, self.config)
            elif self.global_update_strategy == 'all_solutions':
                self.pheromone = update_pheromone_after_epoch(self.list_of_ants, self.pheromone_delta, self.pheromone, self.config)

            self.pheromone_delta = np.zeros((self.graph_size, self.graph_size))
            self.list_of_ants = []

            for tmp in range(self.number_of_ants):
                ant = Ant(graph = copy.deepcopy(self.graph), pheromone= self.pheromone, capacity= self.capacity, current_position=0, heuristic=self.heuristic)
                self.list_of_ants.append(ant)

        print("BEST MOVES: " + str(self.current_best_weight))

        return self.current_best_weight, self.current_best_list_of_moves


config_dict = yaml.safe_load(open('test/config.yaml'))

runs = config_dict['runs']

ant_constants = AntConstants(yaml_dict=config_dict['ant_constants'])

pheromone_strategy = PheremoneStrategy(yaml_dict=config_dict['pheromone'])

eliteness_strategy = ElitenessStrategy(yaml_dict=config_dict['eliteness'])

test_case_config = TestCaseConfig(pheromone_strategy,ant_constants, eliteness_strategy, config_dict['test'])


# config = Config(1,GRAPH_SIZE,NUMBER_OF_ANTS,PHEROMONE,GLOBAL_UPDATE_STRATEGY,PHEROMONE_UPDATE,HEURISTIC,ANT_CAPACITY,EXPLOITATION_CONSTANT,HEURISTIC_EXPONENT,PHEROMONE_EXPONENT,EVAPORATE_RATE,NUMBER_OF_ELITE_ANTS)

config = Config.from_test_config(test_case_config, PHEROMONE)
aco = ACO(config)
aco.run()
