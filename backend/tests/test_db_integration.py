import pytest
from sqlmodel import Session, create_engine, select

from app.models import (
    AdvisoryRecord,
    ClimateSnapshot,
    DiseaseAnalysis,
    Farm,
    FarmLocation,
    SoilReading,
    WeatherSnapshot,
)


@pytest.fixture
def db_engine():
    # In-memory SQLite engine simulating full relational model and indexes
    engine = create_engine("sqlite:///:memory:", echo=False)
    Farm.metadata.create_all(engine)
    return engine


def test_postgresql_sqlmodel_schema_and_crud(db_engine):
    with Session(db_engine) as session:
        # 1. Create Farm
        farm = Farm(
            name="Telangana Maize Plot",
            location_query="Warangal, Telangana",
            latitude=17.9784,
            longitude=79.5941,
            elevation_m=270.0,
            primary_crop="Maize",
        )
        session.add(farm)
        session.commit()
        session.refresh(farm)

        assert farm.id is not None
        assert farm.name == "Telangana Maize Plot"

        # 2. Persist Location and Snapshots with Foreign Keys
        loc = FarmLocation(
            farm_id=farm.id,
            display_name="Warangal Rural District, Telangana",
            latitude=farm.latitude,
            longitude=farm.longitude,
            elevation_m=farm.elevation_m,
        )
        weather_snap = WeatherSnapshot(
            farm_id=farm.id,
            temperature_c=31.2,
            humidity_pct=68.0,
            rainfall_mm=0.0,
            provider="open_meteo",
            freshness="fresh",
        )
        climate_snap = ClimateSnapshot(
            farm_id=farm.id,
            period_label="Last 30 Days Agroclimate",
            total_precip_mm=45.0,
            dry_spell_days=4,
            provider="nasa_power",
            freshness="fresh",
        )
        session.add(loc)
        session.add(weather_snap)
        session.add(climate_snap)
        session.commit()

        # 3. Query snapshots by farm_id
        w_res = session.exec(
            select(WeatherSnapshot).where(WeatherSnapshot.farm_id == farm.id)
        ).all()
        assert len(w_res) == 1
        assert w_res[0].temperature_c == 31.2

        c_res = session.exec(
            select(ClimateSnapshot).where(ClimateSnapshot.farm_id == farm.id)
        ).all()
        assert len(c_res) == 1
        assert c_res[0].total_precip_mm == 45.0

        # 4. Save Disease Analysis and Soil Reading
        disease = DiseaseAnalysis(
            farm_id=farm.id,
            crop="Maize",
            image_path="uploads/leaf_01.jpg",
            predicted_class="Leaf Blight",
            confidence=None,  # Demo model
            model_version="demo-mobilenet-v1",
            is_demo=True,
        )
        soil = SoilReading(
            farm_id=farm.id,
            nitrogen=50.0,
            phosphorus=25.0,
            potassium=30.0,
            ph=6.8,
            moisture=22.0,
            crop="Maize",
            predicted_category="Optimal",
            confidence=0.92,
            model_version="xgboost-synthetic-v1",
            is_synthetic=True,
        )
        session.add(disease)
        session.add(soil)
        session.commit()

        # 5. Save Advisory Record
        adv = AdvisoryRecord(
            farm_id=farm.id,
            source_type="disease",
            source_id=disease.id,
            recommendation="Apply balanced copper fungicide.",
            provider="local-demo",
            citations_json="[]",
            limitations="Demo recommendation",
        )
        session.add(adv)
        session.commit()
        session.refresh(adv)

        assert adv.id is not None
        assert adv.farm_id == farm.id
