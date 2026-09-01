from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def health_check():
    """
    Check if the application is running.
    """
    return {"status": "ok"}
