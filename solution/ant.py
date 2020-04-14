import numpy as np


class Ant:
    def __init__(self, graph: np.array, pheromone: np.array , capacity: int, current_position: int, heuristic: str):
        self.graph = graph #3 wymiarowa tablica, gdzie pierwsze dwa wymiary to współrzedne grafu, a w trzecim trzymana jest odległość i pojemność dobra w docelowym wierzchołku
        self.pheromone = pheromone
        self.capacity = capacity
        self.current_position = current_position
        self.list_of_moves = []
        self.weight_of_moves = 0
        self.heuristic = heuristic

    def update_pheromone_on_path(self, delta: np.array):
        amount_of_moves = len(self.list_of_moves)
        for i in range(0,amount_of_moves-1):
            delta[self.list_of_moves[i]][self.list_of_moves[i+1]] += 1 / self.weight_of_moves

    def reset(self, graph: np.array):
        self.graph = graph
        self.list_of_moves = []
        self.weight_of_moves = 0
        return self
