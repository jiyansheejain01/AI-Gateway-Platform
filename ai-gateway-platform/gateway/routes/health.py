"""
Health check endpoints.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    tags=["Health"],
)
def health_check():
    return {
        "status": "AI Gateway Running"
    }