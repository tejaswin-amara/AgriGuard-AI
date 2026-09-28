import axios from "axios";
import type {
  AdvisoryDetailResponse,
  AdvisoryGenerateRequest,
  AdvisoryGenerateResponse,
  AirQualityData,
  BiodiversityData,
  ClimateData,
  DiseaseAnalyzeResponse,
  ElevationData,
  Farm,
  FarmContextResponse,
  FarmCreateInput,
  GeocodedLocation,
  NewsData,
  ProviderStatusInfo,
  SoilAdviseRequest,
  SoilAdviseResponse,
  WeatherData,
} from "../types";

export const apiClient = axios.create({
  baseURL: "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

export const farmService = {
  async createFarm(input: FarmCreateInput): Promise<Farm> {
    const res = await apiClient.post<Farm>("/farms", input);
    return res.data;
  },

  async listFarms(): Promise<Farm[]> {
    const res = await apiClient.get<Farm[]>("/farms");
    return res.data;
  },

  async getFarm(farmId: number): Promise<Farm> {
    const res = await apiClient.get<Farm>(`/farms/${farmId}`);
    return res.data;
  },

  async getFarmContext(farmId: number): Promise<FarmContextResponse> {
    const res = await apiClient.get<FarmContextResponse>(
      `/farms/${farmId}/context`,
    );
    return res.data;
  },
};

export const locationService = {
  async geocode(query: string): Promise<GeocodedLocation> {
    const res = await apiClient.post<GeocodedLocation>("/location/geocode", {
      query,
    });
    return res.data;
  },

  async reverseGeocode(lat: number, lon: number): Promise<GeocodedLocation> {
    const res = await apiClient.get<GeocodedLocation>("/location/reverse", {
      params: { lat, lon },
    });
    return res.data;
  },
};

export const weatherService = {
  async getWeather(lat: number, lon: number): Promise<WeatherData> {
    const res = await apiClient.get<WeatherData>("/weather", {
      params: { lat, lon },
    });
    return res.data;
  },

  async getClimate(lat: number, lon: number): Promise<ClimateData> {
    const res = await apiClient.get<ClimateData>("/climate", {
      params: { lat, lon },
    });
    return res.data;
  },
};

export const environmentService = {
  async getAirQuality(lat: number, lon: number): Promise<AirQualityData> {
    const res = await apiClient.get<AirQualityData>(
      "/environment/air-quality",
      { params: { lat, lon } },
    );
    return res.data;
  },

  async getElevation(lat: number, lon: number): Promise<ElevationData> {
    const res = await apiClient.get<ElevationData>("/environment/elevation", {
      params: { lat, lon },
    });
    return res.data;
  },
};

export const providerService = {
  async getProvidersHealth(): Promise<ProviderStatusInfo[]> {
    const res = await apiClient.get<ProviderStatusInfo[]>("/providers/health");
    return res.data;
  },
};

export const newsService = {
  async getAgriculturalNews(query = "agriculture"): Promise<NewsData> {
    const res = await apiClient.get<NewsData>("/news", { params: { query } });
    return res.data;
  },
};

export const biodiversityService = {
  async getBiodiversity(lat: number, lon: number): Promise<BiodiversityData> {
    const res = await apiClient.get<BiodiversityData>("/biodiversity", {
      params: { lat, lon },
    });
    return res.data;
  },
};

export const diseaseService = {
  async analyzeDisease(
    file: File,
    crop: string,
    farmId?: number,
  ): Promise<DiseaseAnalyzeResponse> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("crop", crop);
    if (farmId) {
      formData.append("farm_id", farmId.toString());
    }

    const res = await apiClient.post<DiseaseAnalyzeResponse>(
      "/disease/analyze",
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      },
    );
    return res.data;
  },
};

export const soilService = {
  async adviseSoil(req: SoilAdviseRequest): Promise<SoilAdviseResponse> {
    const res = await apiClient.post<SoilAdviseResponse>("/soil/advise", req);
    return res.data;
  },
};

export const advisoryService = {
  async generateAdvisory(
    req: AdvisoryGenerateRequest,
  ): Promise<AdvisoryGenerateResponse> {
    const res = await apiClient.post<AdvisoryGenerateResponse>(
      "/advisory/generate",
      req,
    );
    return res.data;
  },

  async listAdvisories(farmId?: number): Promise<AdvisoryDetailResponse[]> {
    const res = await apiClient.get<AdvisoryDetailResponse[]>("/advisories", {
      params: { farm_id: farmId },
    });
    return res.data;
  },

  async getAdvisory(id: number): Promise<AdvisoryDetailResponse> {
    const res = await apiClient.get<AdvisoryDetailResponse>(
      `/advisories/${id}`,
    );
    return res.data;
  },
};
