import math
from os import listdir
import numpy as np
import yaml
from solution.config import Config
from solution.aco import ACO
from tests.test_config import AntConstants, PheremoneStrategy, ElitenessStrategy, TestCaseConfig, TestGraph


def parse_graph(filename: str):
    print(f"Parsing {filename}")
    file = open("../data/Vrp-Set-A/A/" + str(filename))
    name = str(file.readline())
    optimal_value = str(file.readline())
    idx = optimal_value.find("Optimal value: ")
    optimal_value = int(optimal_value[idx + 15:len(optimal_value) - 2])
    capacity = file.readline()
    while capacity.find("CAPACITY") == -1:
        capacity = file.readline()
    capacity_of_ant = int(capacity[11:len(capacity)])
    print(name + " Optimal value: " + str(optimal_value) + "Capacity: " + str(capacity_of_ant))
    file.readline()
    position = file.readline()
    coordinates = []
    while position.find("DEMAND_SECTION") == -1:
        coordinates.append(list(map(int, position[1:len(position)].split(" ")))[1:3])
        position = file.readline()
    capacity = file.readline()
    capacities = []
    while capacity.find("DEPOT_SECTION") == -1:
        capacities.append(list(map(int, capacity[0:len(capacity) - 2].split(" ")))[1:2])
        capacity = file.readline()
    graph = np.zeros((len(coordinates), len(coordinates), 2))
    for idx, first_coordinate in enumerate(coordinates):
        for idx2, second_coordinate in enumerate(coordinates):
            if not idx == idx2:
                graph[idx][idx2][0] = math.sqrt((first_coordinate[0] - second_coordinate[0]) ** 2 + (
                            first_coordinate[1] - second_coordinate[1]) ** 2)
                graph[idx][idx2][1] = capacities[idx2][0]

    return [TestGraph(len(coordinates), graph, capacity_of_ant), optimal_value]


def prepare_test_case_config(path_to_config):
    config_dict = yaml.safe_load(open(path_to_config))
    runs = config_dict['runs']
    ant_constants = AntConstants(yaml_dict=config_dict['ant_constants'])
    pheromone_strategy = PheremoneStrategy(yaml_dict=config_dict['pheromone'])
    eliteness_strategy = ElitenessStrategy(yaml_dict=config_dict['eliteness'])

    return TestCaseConfig(pheromone_strategy, ant_constants, eliteness_strategy, config_dict['test'], runs)


def prepare_test_case(graph: TestGraph, test_case_config: TestCaseConfig):
    return Config.from_graph_and_config(test_case_config, graph)


results = []
f = open("results.txt", "w+")
for i in range(10):
    for file in listdir("../data/Vrp-Set-A/A"):
        graph, optimal_result = parse_graph(file)

        yaml_config = prepare_test_case_config('./config.yaml')
        test_case_config = prepare_test_case(graph, yaml_config)


# FIXME iteration over files needed to be implemented


        aco = ACO(test_case_config)
        solution = aco.run()
        result = solution[0]/optimal_result
        print(result)
        f.write(str(result) + "\n")
    f.write("---------\n")
