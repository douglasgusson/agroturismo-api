from fastapi import APIRouter

from .category import router as category_router
from .tag import router as tag_router

main_router = APIRouter()

main_router.include_router(tag_router, prefix="/tags", tags=["tags"])
main_router.include_router(category_router, prefix="/categories", tags=["categories"])
