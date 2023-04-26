import copy

from ...utils import calculate_solution_cost


def local_search(solution, dist_matrix):
    """
    Função que realiza a busca local para uma solução dada
    """
    best_cost = calculate_solution_cost(solution, dist_matrix)
    improved = True
    while improved:
        improved = False
        for i in range(len(solution) - 1):
            for j in range(i + 1, len(solution)):
                new_solution = copy.deepcopy(solution)
                new_solution[i], new_solution[j] = (
                    new_solution[j],
                    new_solution[i],
                )
                new_cost = calculate_solution_cost(new_solution, dist_matrix)
                if new_cost < best_cost:
                    solution = new_solution
                    best_cost = new_cost
                    improved = True
                    break
            if improved:
                break
    return solution, best_cost
