import math
from os import listdir
import numpy as np
import yaml

from solution.config import Config
from solution.aco import  ACO
from tests.test_config import AntConstants, PheremoneStrategy, ElitenessStrategy, TestCaseConfig

GRAPH_SIZE = 30
NUMBER_OF_ANTS = 100

# HEURISTIC = "basic"
# HEURISTIC = "exploitation"

HEURISTIC = "savings"

EXPLOITATION_CONSTANT = 0.5
HEURISTIC_EXPONENT = 1
PHEROMONE_EXPONENT = 3
PHEROMONE = np.random.rand(GRAPH_SIZE, GRAPH_SIZE)
PHEROMONE = [pheromone*100 for pheromone in PHEROMONE]
EVAPORATE_RATE = 0.1

#PHEROMONE_UPDATE = "basic"
PHEROMONE_UPDATE = "elite"

GLOBAL_UPDATE_STRATEGY = "best_solution"
# GLOBAL_UPDATE_STRATEGY = "all_solutions"

NUMBER_OF_ELITE_ANTS = 10

ANT_CAPACITY = 3



def all_graphs_from_file():
    print("START")
    for file in listdir("../data/Vrp-Set-A/A"):
        print("tests")
        file = open("../data/Vrp-Set-A/A/" + str(file))
        name = str(file.readline())
        optimal_value = str(file.readline())
        idx = optimal_value.find("Optimal value: ")
        optimal_value = int(optimal_value[idx + 15:len(optimal_value)-2])
        capacity = file.readline()
        while capacity.find("CAPACITY") == -1:
            capacity = file.readline()
        capacity_of_ant = int(capacity[11:len(capacity)])
        print(name + " Optimal value: " + str(optimal_value) + "Capacity: " + str(capacity_of_ant))
        file.readline()
        position = file.readline()
        idx = 1
        coordinates = []
        while position.find("DEMAND_SECTION") == -1:
            coordinates.append(list(map(int, position[1:len(position)].split(" ")))[1:3])
            position = file.readline()
            # print(position.find("DEMAND_SECTION"))
        capacity = file.readline()
        capacities = []
        while capacity.find("DEPOT_SECTION") == -1:
            capacities.append(list(map(int, capacity[0:len(capacity)-2].split(" ")))[1:2])
            capacity = file.readline()
        graph = np.zeros((len(coordinates), len(coordinates), 2))
        for idx, first_coordinate in enumerate(coordinates):
            for idx2, second_coordinate in enumerate(coordinates):
                if not idx == idx2:
                    graph[idx][idx2][0] = math.sqrt((first_coordinate[0] - second_coordinate[0])**2 + (first_coordinate[1] - second_coordinate[1])**2)
                    graph[idx][idx2][1] = capacities[idx2][0]
        print("end")

        config_dict = yaml.safe_load(open('../tests/config.yaml'))

        runs = config_dict['runs']

        ant_constants = AntConstants(yaml_dict=config_dict['ant_constants'])

        pheromone_strategy = PheremoneStrategy(yaml_dict=config_dict['pheromone'])

        eliteness_strategy = ElitenessStrategy(yaml_dict=config_dict['eliteness'])

        test_case_config = TestCaseConfig(pheromone_strategy, ant_constants, eliteness_strategy, config_dict['test'])

        # config = Config(1,GRAPH_SIZE,NUMBER_OF_ANTS,PHEROMONE,GLOBAL_UPDATE_STRATEGY,PHEROMONE_UPDATE,HEURISTIC,ANT_CAPACITY,EXPLOITATION_CONSTANT,HEURISTIC_EXPONENT,PHEROMONE_EXPONENT,EVAPORATE_RATE,NUMBER_OF_ELITE_ANTS)

        config = Config.from_test_config(test_case_config, PHEROMONE)
        aco = ACO(config, graph, np.random.rand(len(coordinates), len(coordinates)))
        aco.graph_size = len(coordinates)
        aco.graph = graph
        aco.pheromone = np.random.rand(aco.graph_size, aco.graph_size)
        aco.pheromone_delta = np.zeros((aco.graph_size, aco.graph_size))
        aco.capacity = capacity_of_ant
        aco.config.graph_size = aco.graph_size
        aco.config.pheromone = aco.pheromone
        aco.config.ant_capacity = aco.capacity
        aco.run()


all_graphs_from_file()
