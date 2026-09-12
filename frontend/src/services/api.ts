import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export const analyzeDisease = async (crop: string, image: File) => {
	const formData = new FormData();
	formData.append("image", image);

	const response = await axios.post(`${API_URL}/disease/analyze`, formData, {
		params: { crop },
		headers: { "Content-Type": "multipart/form-data" },
	});
	return response.data;
};

export const adviseSoil = async (data: any) => {
	const response = await axios.post(`${API_URL}/soil/advise`, data);
	return response.data;
};

export const generateAdvisory = async (type: string, id: number) => {
	const response = await axios.post(`${API_URL}/advisory/generate`, {
		source_reading_type: type,
		source_reading_id: id,
	});
	return response.data;
};
