from fastapi import APIRouter

from .algorithm import router as algorithm_router
from .category import router as category_router
from .local import router as local_router
from .tag import router as tag_router
from .tourist import router as tourist_router

main_router = APIRouter()

main_router.include_router(local_router, prefix="/locals", tags=["Locals"])
main_router.include_router(category_router, prefix="/categories", tags=["Categories"])
main_router.include_router(tourist_router, prefix="/tourists", tags=["Tourists"])
main_router.include_router(tag_router, prefix="/tags", tags=["Tags"])
main_router.include_router(algorithm_router, prefix="/algorithm", tags=["Algorithm"])
