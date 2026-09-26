from fastapi import APIRouter, Query

from app.services.external.providers.news import AgricultureNewsProvider
from app.services.external.types import NewsData

router = APIRouter(prefix="/news", tags=["News"])
news_provider = AgricultureNewsProvider()


@router.get(
    "", response_model=NewsData, summary="Get Agricultural Outbreak & Advisory News"
)
async def get_agricultural_news(query: str = Query("agriculture", max_length=100)):
    return await news_provider.get_news(query)
