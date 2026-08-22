"""
Users router — endpoints for user profile management.
"""

from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserResponse
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Returns the profile information of the currently authenticated user.
    Requires a valid JWT token in the Authorization header.
    """
    return current_user
