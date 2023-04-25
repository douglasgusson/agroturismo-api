import numpy as np


def haversine_distance(coords1, coords2):
    """
    Função que calcula a distância entre duas coordenadas
    """
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    R = 6371  # raio da Terra em km
    dLat = np.radians(lat2 - lat1)
    dLon = np.radians(lon2 - lon1)
    a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(np.radians(lat1)) * np.cos(
        np.radians(lat2)
    ) * np.sin(dLon / 2) * np.sin(dLon / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance
