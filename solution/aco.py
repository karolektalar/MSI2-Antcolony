import copy
import numpy as np

from solution.ant import Ant
from solution.move import ant_move
from solution.pheromone import update_pheromone_after_epoch, update_pheromone_from_the_best_solution
from solution.config import  GRAPH_SIZE, PHEROMONE, ANT_CAPACITY, HEURISTIC, NUMBER_OF_ANTS, GLOBAL_UPDATE_STRATEGY

if __name__ == "__main__":
    graph = np.random.rand(GRAPH_SIZE, GRAPH_SIZE, 2)
    pheromone_delta = np.zeros((GRAPH_SIZE,GRAPH_SIZE))
    for idx, element in enumerate(graph):
        for idx2, subelement in enumerate(element):
            if idx == idx2:
                graph[idx][idx2] = np.zeros(2)
    list_of_ants = []
    for i in range(NUMBER_OF_ANTS):
        ant = Ant(graph= copy.deepcopy(graph), pheromone=PHEROMONE, capacity=ANT_CAPACITY, current_position=0, heuristic=HEURISTIC)
        list_of_ants.append(ant)

    current_best_weight = 10000

    for i in range(50):
        for idx, ant in enumerate(list_of_ants):
            list_of_ants[idx] = ant_move(ant)

        best_weight = list_of_ants[0].weight_of_moves
        worst_weight = list_of_ants[0].weight_of_moves
        best_list_of_moves = list_of_ants[0].list_of_moves
        worst_list_of_moves = list_of_ants[0].list_of_moves
        best_ant = list_of_ants[0]

        for idx, ant in enumerate(list_of_ants):
            if ant.weight_of_moves < best_weight:
                best_weight = ant.weight_of_moves
                best_list_of_moves = ant.list_of_moves
                best_ant = ant
            if ant.weight_of_moves > worst_weight:
                worst_weight = ant.weight_of_moves
                worst_list_of_moves = ant.list_of_moves

        loss = current_best_weight - best_weight

        if loss > 0:
            print(f"WORST WEIGHT at epoch {i}/50 : {str(worst_weight)}")
            # print("WORST MOVES: " + str(worst_list_of_moves))
            print(f"BEST WEIGHT at epoch {i}/50 : {str(best_weight)} loss = {loss})")
            # print("BEST MOVES: " + str(best_list_of_moves))
            print("************-------------**************")

        if current_best_weight > best_weight:
            current_best_weight = best_weight
            current_best_list_of_moves = best_list_of_moves

        if GLOBAL_UPDATE_STRATEGY == 'best_solution':
            PHEROMONE = update_pheromone_from_the_best_solution(ant=best_ant, pheromone=PHEROMONE,
                                                                pheromone_delta=pheromone_delta)
        elif GLOBAL_UPDATE_STRATEGY == 'all_solutions':
            PHEROMONE = update_pheromone_after_epoch(list_of_ants, pheromone_delta, PHEROMONE)

        pheromone_delta = np.zeros((GRAPH_SIZE, GRAPH_SIZE))
        list_of_ants = []

        for tmp in range(NUMBER_OF_ANTS):
            ant = Ant(graph = copy.deepcopy(graph), pheromone= PHEROMONE, capacity= ANT_CAPACITY, current_position=0, heuristic=HEURISTIC)
            list_of_ants.append(ant)

    print("BEST MOVES: " + str(current_best_weight))
    print("BEST MOVES: " + str(current_best_weight))

