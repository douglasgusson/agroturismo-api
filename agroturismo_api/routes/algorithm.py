import copy
import random
from typing import List, Tuple, Union

import numpy as np
from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, select

from ..core.db import ActiveSession
from ..models.local import Local, LocalBase, LocalRead

router = APIRouter()


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


def generate_random_solution(num_points):
    """
    Função que gera uma solução inicial aleatória
    """
    solution = list(range(num_points))
    random.shuffle(solution)
    return solution


def calculate_solution_cost(solution, dist_matrix):
    """
    Função que calcula o custo de uma solução
    """
    cost = 0
    for i in range(len(solution) - 1):
        cost += dist_matrix[solution[i]][solution[i + 1]]
    cost += dist_matrix[solution[-1]][solution[0]]
    return cost


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
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                new_cost = calculate_solution_cost(new_solution, dist_matrix)
                if new_cost < best_cost:
                    solution = new_solution
                    best_cost = new_cost
                    improved = True
                    break
            if improved:
                break
    return solution, best_cost


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


def get_coords(ids: List[int], session: Session) -> List[Tuple[float, float]]:
    """
    Função que obtém as coordenadas de uma lista de IDs de locais
    """
    coords = []
    for id in ids:
        local = session.get(Local, id)
        if not local:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Local não encontrado"
            )
        coords.append((local.latitude, local.longitude))
    return coords


@router.get("/guided-local-search", response_model=List[LocalBase])
async def calculate_best_route_guided_local_search(
    *, ids: List[int] = Query(None), session: Session = ActiveSession
):
    """
    Função que calcula o TSP para uma lista de IDs de locais
    """
    if ids is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="IDs não informados"
        )

    # Obtém as coordenadas dos locais
    coords = get_coords(ids, session)

    # Definindo os parâmetros da meta-heurística
    max_iterations = 100
    max_no_improv = 50
    alpha = 0.3
    beta = 0.99

    # Resolvendo o problema do caixeiro viajante com a meta-heurística GLS
    best_solution, best_cost = guided_local_search(
        coords, max_iterations, max_no_improv, alpha, beta
    )

    print("### Guided Local Search", best_cost, best_solution)

    locals_ids = [ids[i] for i in best_solution]

    # seleciona os locais ordenados
    locals = session.query(Local).filter(Local.id.in_(locals_ids)).all()

    # Retorna a lista de locais ordenados
    return locals


@router.get("/tabu-search", response_model=List[LocalBase])
async def calculate_best_route_tabu_search(
    *, ids: List[int] = Query(None), session: Session = ActiveSession
):
    """
    Função que calcula o TSP para uma lista de IDs de locais
    """
    if ids is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="IDs não informados"
        )

    # Obtém as coordenadas dos locais
    coords = get_coords(ids, session)

    # Definindo os parâmetros da meta-heurística
    max_iterations = 100
    max_no_improv = 50
    tabu_tenure = 10

    # Resolvendo o problema do caixeiro viajante com a meta-heurística TS
    best_solution, best_cost = tabu_search(
        coords, max_iterations, max_no_improv, tabu_tenure
    )

    print("### Tabu Search", best_cost, best_solution)

    locals_ids = [ids[i] for i in best_solution]

    # seleciona os locais ordenados
    locals = session.query(Local).filter(Local.id.in_(locals_ids)).all()

    # Retorna a lista de locais ordenados
    return locals
