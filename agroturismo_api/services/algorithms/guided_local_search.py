import random
from typing import List, Tuple

import numpy as np

from ...utils import (
    calculate_distance_matrix,
    calculate_solution_cost,
    generate_random_solution,
)
from .local_search import local_search


def construct_initial_solution(dist_matrix, alpha):
    """
    Função que constrói a solução inicial, levando em consideração o alpha dado
    """
    num_points = dist_matrix.shape[0]
    candidate_list = list(range(num_points))
    solution = []
    current_point = random.choice(candidate_list)
    candidate_list.remove(current_point)
    solution.append(current_point)
    while candidate_list:
        distances = dist_matrix[current_point][candidate_list]
        max_distance = np.max(distances)
        min_distance = np.min(distances)
        threshold = min_distance + alpha * (max_distance - min_distance)
        eligible_indices = np.where(distances <= threshold)[0]
        if eligible_indices.shape[0] == 0:
            eligible_indices = [np.argmin(distances)]
        index = random.choice(eligible_indices)
        current_point = candidate_list[index]
        candidate_list.remove(current_point)
        solution.append(current_point)
    return solution


def guided_local_search(
    coords: List[Tuple[float, float]],
    max_iterations: int,
    max_no_improv: int,
    alpha: float,
    beta: float,
):
    """
    Função que implementa a meta-heurística GLS para o problema do caixeiro viajante
    """
    num_points = len(coords)
    dist_matrix = calculate_distance_matrix(coords)
    best_solution = generate_random_solution(num_points)
    best_cost = calculate_solution_cost(best_solution, dist_matrix)
    no_improv = 0

    for i in range(max_iterations):
        candidate_solution = construct_initial_solution(dist_matrix, alpha)
        candidate_solution, candidate_cost = local_search(
            candidate_solution, dist_matrix
        )
        candidate_solution, candidate_cost = local_search(
            candidate_solution, dist_matrix
        )

        if candidate_cost < best_cost:
            best_solution = candidate_solution
            best_cost = candidate_cost
            no_improv = 0
        else:
            no_improv += 1
        alpha *= beta
        if no_improv >= max_no_improv:
            break

    return best_solution, best_cost
