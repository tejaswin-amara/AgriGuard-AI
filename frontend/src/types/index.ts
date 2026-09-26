export type DataQuality =
  | "LAB_MEASUREMENT"
  | "SENSOR_MEASUREMENT"
  | "OFFICIAL_OBSERVATION"
  | "REMOTE_SENSING"
  | "WEATHER_MODEL"
  | "HISTORICAL_CLIMATE"
  | "ML_PREDICTION"
  | "LLM_OUTPUT"
  | "NEWS_SOURCE"
  | "HEURISTIC";

export type FreshnessState = "fresh" | "cached" | "stale" | "unavailable";

export interface Provenance {
  provider: string;
  provider_name: string;
  capability: string;
  source_url?: string;
  observed_at?: string;
  retrieved_at: string;
  data_quality: DataQuality;
  freshness: FreshnessState;
  attribution?: string;
  notes?: string;
}

export interface GeocodedLocation {
  name: string;
  display_name: string;
  latitude: number;
  longitude: number;
  elevation_m?: number;
  country?: string;
  state?: string;
  district?: string;
  city?: string;
  village?: string;
  provenance: Provenance;
}

export interface ForecastDay {
  date: string;
  min_temp_c?: number;
  max_temp_c?: number;
  precipitation_mm?: number;
  et0_mm?: number;
}

export interface WeatherData {
  temperature_c?: number;
  humidity_pct?: number;
  rainfall_mm?: number;
  wind_speed_kmh?: number;
  solar_radiation_mj?: number;
  et0_mm?: number;
  vpd_kpa?: number;
  soil_temperature_c?: number;
  soil_moisture_m3m3?: number;
  gdd?: number;
  forecast: ForecastDay[];
  provenance: Provenance;
}

export interface ClimateData {
  period_label: string;
  mean_temp_c?: number;
  min_temp_c?: number;
  max_temp_c?: number;
  total_precipitation_mm?: number;
  rainfall_7d_mm?: number;
  rainfall_14d_mm?: number;
  rainfall_30d_mm?: number;
  dry_spell_days?: number;
  gdd_cumulative?: number;
  et0_cumulative?: number;
  anomalies: Record<string, number>;
  provenance: Provenance;
}

export interface AirQualityData {
  pm25?: number;
  pm10?: number;
  no2?: number;
  o3?: number;
  aqi_estimate?: number;
  provenance: Provenance;
}

export interface ElevationData {
  elevation_m: number;
  provenance: Provenance;
}

export interface BiodiversityObservation {
  species_name: string;
  common_name?: string;
  category: string;
  observation_count: number;
  last_observed_at?: string;
  dataset?: string;
}

export interface BiodiversityData {
  total_observations: number;
  observations: BiodiversityObservation[];
  provenance: Provenance;
}

export interface NewsArticle {
  title: string;
  summary?: string;
  source: string;
  url: string;
  published_at?: string;
  category: string;
}

export interface NewsData {
  articles: NewsArticle[];
  provenance: Provenance;
}

export interface RiskSignal {
  name: string;
  level: "low" | "moderate" | "elevated" | "severe" | "none" | "mild" | "high";
  score: number;
  explanation: string;
}

export interface RiskContext {
  fungal_pressure: string;
  water_stress: string;
  heat_stress: string;
  overall_level: string;
  signals: RiskSignal[];
  explanations: string[];
}

export interface ProviderStatusInfo {
  provider_id: string;
  name: string;
  category: string;
  is_required: boolean;
  enabled: boolean;
  status: "healthy" | "degraded" | "unavailable";
  latency_ms?: number;
  last_success?: string;
  last_failure?: string;
  error_message?: string;
}

export interface Citation {
  title: string;
  organization: string;
  content: string;
  document_id: string;
  url?: string;
  provider?: string;
  source_type?: string;
  data_quality?: string;
}

export interface ModelProvenance {
  model_name: string;
  model_version: string;
  inference_mode: string;
  training_data: string;
  field_validated: boolean;
  limitation: string;
}

export interface Farm {
  id: number;
  name: string;
  location_query: string;
  latitude: number;
  longitude: number;
  elevation_m?: number;
  timezone: string;
  primary_crop: string;
  plot_identifier?: string;
  created_at: string;
  updated_at: string;
}

export interface FarmCreateInput {
  name: string;
  location_query: string;
  primary_crop: string;
  plot_identifier?: string;
}

export interface FarmContextResponse {
  farm: Farm;
  location: GeocodedLocation;
  weather: WeatherData;
  climate: ClimateData;
  air_quality?: AirQualityData;
  elevation?: ElevationData;
  biodiversity?: BiodiversityData;
  news?: NewsData;
  risk_context: RiskContext;
  provider_status: ProviderStatusInfo[];
  freshness: Record<string, string>;
}

export interface DiseaseAnalyzeResponse {
  id: number;
  crop: string;
  predicted_class: string;
  confidence: number;
  model_version: string;
  is_demo: boolean;
  limitation: string;
  farm_id?: number;
  risk_context?: RiskContext;
  weather_summary?: string;
  citations: Citation[];
  model_provenance: ModelProvenance;
}

export interface SoilAdviseRequest {
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  ph: number;
  moisture: number;
  crop?: string;
  farm_id?: number;
}

export interface SoilAdviseResponse {
  id: number;
  predicted_category: string;
  confidence?: number;
  model_version: string;
  is_synthetic: boolean;
  limitation: string;
  farm_id?: number;
  risk_context?: RiskContext;
  weather_summary?: string;
  citations: Citation[];
  model_provenance: ModelProvenance;
}

export interface AdvisoryGenerateRequest {
  source_reading_type: "disease" | "soil" | "general";
  source_reading_id?: number;
  farm_id?: number;
  custom_query?: string;
}

export interface AdvisoryGenerateResponse {
  id: number;
  recommendation: string;
  provider: string;
  citations: Citation[];
  limitation: string;
  risk_signals?: RiskContext;
  created_at: string;
}

export interface AdvisoryDetailResponse {
  id: number;
  farm_id?: number;
  source_type: string;
  source_id?: number;
  recommendation: string;
  provider: string;
  model_version: string;
  citations: Citation[];
  risk_signals?: RiskContext;
  limitations: string;
  created_at: string;
}
