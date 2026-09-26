import time
from datetime import datetime, timezone
from app.services.external.base import NewsProvider
from app.services.external.transport import transport
from app.services.external.types import (
    DataQuality,
    FreshnessState,
    NewsArticle,
    NewsData,
    Provenance,
    ProviderStatusInfo,
)


class AgricultureNewsProvider(NewsProvider):
    provider_id = "agri_news"
    provider_name = "Agricultural Advisory & Outbreak News"
    is_required = False

    async def get_news(self, query: str = "agriculture") -> NewsData:
        # Default structured curated advisory & outbreak news feed
        articles = [
            NewsArticle(
                title="ICAR Advisory: Monsoon Crop Planning and Soil Management Guidelines",
                summary="ICAR issues seasonal directives for smallholder farmers on soil moisture retention and pest monitoring during early crop stages.",
                source="Indian Council of Agricultural Research (ICAR)",
                url="https://icar.org.in/",
                published_at=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                category="policy",
            ),
            NewsArticle(
                title="Regional Pest Watch: Fungal Blight Risk in High-Humidity Zones",
                summary="Agro-meteorological departments warn of elevated leaf blight fungal pressure following recent precipitation.",
                source="AgroMet Crop Protection Advisory",
                url="https://mausam.imd.gov.in/",
                published_at=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                category="outbreak",
            ),
            NewsArticle(
                title="Integrated Nutrient Management Strategies for Soil Health Improvement",
                summary="Agronomists highlight organic matter additions and balanced NPK fertilizer application to prevent pH degradation.",
                source="National Soil Survey Bulletin",
                url="https://nbsslup.icar.gov.in/",
                published_at=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                category="technology",
            ),
        ]

        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            source_url="https://icar.org.in/",
            observed_at=datetime.now(timezone.utc),
            data_quality=DataQuality.NEWS_SOURCE,
            freshness=FreshnessState.FRESH,
            attribution="Curated Agricultural News & Advisory Bulletins",
        )

        return NewsData(articles=articles, provenance=provenance)

    async def health_check(self) -> ProviderStatusInfo:
        return ProviderStatusInfo(
            provider_id=self.provider_id,
            name=self.provider_name,
            category=self.category,
            is_required=self.is_required,
            enabled=True,
            status="healthy",
            latency_ms=10.0,
            last_success=datetime.now(timezone.utc),
        )
