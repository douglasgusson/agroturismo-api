from fastapi import APIRouter

from .admin_user import router as admin_user_router
from .algorithm import router as algorithm_router
from .category import router as category_router
from .image import router as image_router
from .itinerary import router as itinerary_router
from .local import router as local_router
from .opening_hours import router as opening_hours_router
from .review import router as review_router
from .security import router as security_router
from .special_opening_hours import router as special_opening_hours_router
from .tag import router as tag_router
from .tourist import router as tourist_router

main_router = APIRouter()

main_router.include_router(local_router, prefix="/locals", tags=["Locals"])
main_router.include_router(category_router, prefix="/categories", tags=["Categories"])
main_router.include_router(image_router, prefix="/images", tags=["Images"])
main_router.include_router(tourist_router, prefix="/tourists", tags=["Tourists"])
main_router.include_router(
    itinerary_router, prefix="/itineraries", tags=["Itineraries"]
)
main_router.include_router(review_router, prefix="/reviews", tags=["Reviews"])
main_router.include_router(
    opening_hours_router, prefix="/opening-hours", tags=["OpeningHours"]
)
main_router.include_router(
    special_opening_hours_router,
    prefix="/special-opening-hours",
    tags=["SpecialOpeningHours"],
)
main_router.include_router(tag_router, prefix="/tags", tags=["Tags"])
main_router.include_router(algorithm_router, prefix="/algorithms", tags=["Algorithms"])
main_router.include_router(admin_user_router, prefix="/admins", tags=["Admins"])
main_router.include_router(security_router, tags=["Auth"])
