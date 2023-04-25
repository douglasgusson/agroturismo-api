from typing import List, Tuple

from ...utils import (
    calculate_distance_matrix,
    calculate_solution_cost,
    generate_random_solution,
)
from .local_search import local_search


def tabu_search(
    coords: List[Tuple[float, float]],
    max_iterations: int,
    max_no_improv: int,
    tabu_tenure: int,
):
    """
    Função que implementa a meta-heurística TS para o problema do caixeiro viajante
    """
    num_points = len(coords)
    dist_matrix = calculate_distance_matrix(coords)
    best_solution = generate_random_solution(num_points)
    best_cost = calculate_solution_cost(best_solution, dist_matrix)
    no_improv = 0
    tabu_list = []

    for i in range(max_iterations):
        candidate_solution = generate_random_solution(num_points)
        candidate_solution, candidate_cost = local_search(
            candidate_solution, dist_matrix
        )

        if candidate_cost < best_cost:
            best_solution = candidate_solution
            best_cost = candidate_cost
            no_improv = 0
        else:
            no_improv += 1

        tabu_list.append((best_solution, best_cost))

        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

        if no_improv >= max_no_improv:
            break

    return best_solution, best_cost
