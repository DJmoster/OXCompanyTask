from fastapi import APIRouter

from .auth.router import router as auth_router
from .employees.router import router as employee_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(employee_router)
