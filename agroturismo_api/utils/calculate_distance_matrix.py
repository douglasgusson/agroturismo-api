from typing import List, Tuple

import numpy as np

from .haversine_distance import haversine_distance


def calculate_distance_matrix(coords: List[Tuple[float, float]]):
    """
    Função que calcula a matriz de distâncias a partir de um conjunto de coordenadas
    """
    num_points = len(coords)
    dist_matrix = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(i + 1, num_points):
            dist = haversine_distance(coords[i], coords[j])
            dist_matrix[i][j] = dist
            dist_matrix[j][i] = dist
    return dist_matrix
