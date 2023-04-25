from typing import List, Tuple

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session

from ..core.db import ActiveSession
from ..models.local import Local, LocalBase
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
