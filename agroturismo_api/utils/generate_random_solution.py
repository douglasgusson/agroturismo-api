import random


def generate_random_solution(num_points):
    """
    Função que gera uma solução inicial aleatória
    """
    solution = list(range(num_points))
    random.shuffle(solution)
    return solution
