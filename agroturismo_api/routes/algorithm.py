from typing import List, Tuple

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, case

import numpy as np

from python_tsp.distances import osrm_distance_matrix
from python_tsp.heuristics import solve_tsp_local_search

from ..core.db import ActiveSession
from ..models.local import Local, LocalRead
from ..services.algorithms import guided_local_search, tabu_search

router = APIRouter()


def get_coords(ids: List[int], session: Session) -> List[Tuple[float, float]]:
    """
    Função que obtém as coordenadas de uma lista de IDs de locais
    """
    coords = []
    for id in ids:
        local = session.get(Local, id)
        if not local:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Local não encontrado",
            )
        coords.append((local.latitude, local.longitude))
    return coords


@router.get("/guided-local-search", response_model=List[LocalRead])
async def calculate_best_route_guided_local_search(
    *, ids: List[int] = Query(None), session: Session = ActiveSession
):
    """
    Função que calcula o TSP para uma lista de IDs de locais
    """
    if ids is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IDs não informados",
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


@router.get("/tabu-search", response_model=List[LocalRead])
async def calculate_best_route_tabu_search(
    *, ids: List[int] = Query(None), session: Session = ActiveSession
):
    """
    Função que calcula o TSP para uma lista de IDs de locais
    """
    if ids is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IDs não informados",
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


@router.get("/tsp", response_model=List[LocalRead])
async def calculate_tsp_route(
    *,
    current_latitude: float,
    current_longitude: float,
    ids: List[int] = Query(None),
    session: Session = ActiveSession
):
    """
    Função que calcula o TSP para uma lista de IDs de locais
    """
    if ids is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Locais não informados",
        )

    start_point = (current_latitude, current_longitude)

    # Obtém as coordenadas dos locais
    coords = get_coords(ids, session)

    # Adiciona a coordenada atual no início da lista
    coords.insert(0, start_point)
    sources = np.array(coords)

    distance_matrix = osrm_distance_matrix(
        sources, osrm_server_address="https://router.project-osrm.org"
    )

    permutation, distance = solve_tsp_local_search(distance_matrix)

    permutation = list(map(lambda i: (i - 1), permutation[1:]))
    locals_ids = [ids[i] for i in permutation]

    id_ordering = case(
        {_id: index for index, _id in enumerate(locals_ids)},
        value=Local.id,
    )

    # seleciona os locais
    locals = (
        session.query(Local)
        .filter(Local.id.in_(locals_ids))
        .order_by(id_ordering)
        .all()
    )

    # Retorna a lista de locais ordenados
    return locals
