import copy

from solution.ant import Ant
from solution.move import ant_move
from solution.pheromone import update_pheromone_after_epoch, update_pheromone_from_the_best_solution
from solution.config import Config
import numpy as np


NUMBER_OF_EPOCHS = 300


class ACO:
    def __init__(self, config: Config):
        self.config = config
        self.graph_size = config.graph_size
        self.global_update_strategy = config.global_update_strat
        self.graph = config.graph
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
        for i in range(NUMBER_OF_EPOCHS):
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
                # print(f"WORST WEIGHT at epoch {i+1}/"+str(NUMBER_OF_EPOCHS)+f" : {str(worst_weight)}")
                # print("WORST MOVES: " + str(worst_list_of_moves))
                print(f"BEST WEIGHT at epoch {i+1}/"+str(NUMBER_OF_EPOCHS)+f" : {str(best_weight)} loss = {loss})")
                # print("BEST MOVES: " + str(best_list_of_moves))
                print("************-------------**************")
            if i % 100 == 0:
                print(f"Epoch {i}/"+str(NUMBER_OF_EPOCHS))
            if self.current_best_weight > best_weight:
                self.current_best_weight = best_weight
                current_best_list_of_moves = best_list_of_moves

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

        return self.current_best_weight, current_best_list_of_moves

