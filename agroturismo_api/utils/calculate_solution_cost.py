def calculate_solution_cost(solution, dist_matrix):
    """
    Função que calcula o custo de uma solução
    """
    cost = 0
    for i in range(len(solution) - 1):
        cost += dist_matrix[solution[i]][solution[i + 1]]
    cost += dist_matrix[solution[-1]][solution[0]]
    return cost
