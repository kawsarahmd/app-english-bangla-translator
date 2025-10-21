/**
 * Type definitions for the translation application
 */

export type LanguageCode = 'en' | 'bn';

export interface TranslationRequest {
  text: string;
  source_lang: LanguageCode;
  target_lang: LanguageCode;
}

export interface TranslationResponse {
  translated_text: string;
  source_lang: LanguageCode;
  target_lang: LanguageCode;
  processing_time: number;
}

export interface HealthResponse {
  status: string;
  vllm_connected: boolean;
  timestamp: string;
}

export interface TranslationHistory {
  id: string;
  sourceText: string;
  translatedText: string;
  sourceLang: LanguageCode;
  targetLang: LanguageCode;
  timestamp: Date;
}

export interface APIError {
  detail: string;
}
