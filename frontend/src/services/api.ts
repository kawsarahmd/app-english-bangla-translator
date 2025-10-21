/**
 * API service for communicating with the backend
 */
import axios, { AxiosError } from 'axios';
import type { TranslationRequest, TranslationResponse, HealthResponse, APIError } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Translate text from source to target language
 */
export async function translateText(
  text: string,
  sourceLang: string,
  targetLang: string
): Promise<TranslationResponse> {
  try {
    const request: TranslationRequest = {
      text,
      source_lang: sourceLang as 'en' | 'bn',
      target_lang: targetLang as 'en' | 'bn',
    };

    const response = await api.post<TranslationResponse>('/translate', request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<APIError>;
      const message = axiosError.response?.data?.detail || axiosError.message;
      throw new Error(message);
    }
    throw error;
  }
}

/**
 * Check backend and vLLM health status
 */
export async function checkHealth(): Promise<HealthResponse> {
  try {
    const response = await api.get<HealthResponse>('/health');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error('Unable to connect to translation service');
    }
    throw error;
  }
}

export default api;
