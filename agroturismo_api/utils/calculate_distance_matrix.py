from typing import List, Tuple

import httpx
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


def get_distance_matrix_osrm(points: List[Tuple[float, float]]):
    """
    Função que obtém a matriz de distâncias a partir de um conjunto de coordenadas
    """
    url = f"https://router.project-osrm.org/table/v1/driving/"
    params = {
        "sources": ";".join([f"{i}" for i in range(len(points))]),
        "destinations": ";".join([f"{i}" for i in range(len(points))]),
        "annotations": "distance"
    }

    url_with_points = url + ";".join([f"{p[1]},{p[0]}" for p in points])

    response = httpx.get(url_with_points, params=params)

    distances = response.json()["distances"]
    matrix = np.zeros((len(points), len(points)))

    for i, row in enumerate(distances):
        for j, element in enumerate(row):
            matrix[i][j] = element / 1000  # Dividir por 1000 para obter responsedistâncias em km

    request_url = response.request.url

    print("\n\n", request_url, matrix, sep="\n", end="\n\n")

    return matrix
