/**
 * Main translation interface component
 */
import { useState } from 'react';
import { translateText } from '../services/api';
import type { LanguageCode, TranslationHistory } from '../types';

export default function TranslationInterface() {
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLang, setSourceLang] = useState<LanguageCode>('en');
  const [targetLang, setTargetLang] = useState<LanguageCode>('bn');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [processingTime, setProcessingTime] = useState<number | null>(null);
  const [history, setHistory] = useState<TranslationHistory[]>([]);
  const [copySuccess, setCopySuccess] = useState<string | null>(null);

  const handleTranslate = async () => {
    if (!sourceText.trim()) {
      setError('Please enter text to translate');
      return;
    }

    setIsLoading(true);
    setError(null);
    setProcessingTime(null);

    try {
      const response = await translateText(sourceText, sourceLang, targetLang);
      setTranslatedText(response.translated_text);
      setProcessingTime(response.processing_time);

      // Add to history
      const newHistory: TranslationHistory = {
        id: Date.now().toString(),
        sourceText,
        translatedText: response.translated_text,
        sourceLang,
        targetLang,
        timestamp: new Date(),
      };
      setHistory(prev => [newHistory, ...prev].slice(0, 10));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Translation failed');
      setTranslatedText('');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSwapLanguages = () => {
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
    setSourceText(translatedText);
    setTranslatedText(sourceText);
  };

  const handleClear = () => {
    setSourceText('');
    setTranslatedText('');
    setError(null);
    setProcessingTime(null);
  };

  const handleCopyToClipboard = async (text: string, label: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopySuccess(label);
      setTimeout(() => setCopySuccess(null), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  const handleHistoryClick = (item: TranslationHistory) => {
    setSourceText(item.sourceText);
    setTranslatedText(item.translatedText);
    setSourceLang(item.sourceLang);
    setTargetLang(item.targetLang);
  };

  const getLanguageName = (code: LanguageCode): string => {
    return code === 'en' ? 'English' : 'বাংলা (Bangla)';
  };

  return (
    <div className="translation-container">
      <header className="header">
        <h1>English-Bangla Translator</h1>
        <p className="subtitle">Bidirectional translation powered by vLLM</p>
      </header>

      <div className="language-selector">
        <select
          value={sourceLang}
          onChange={(e) => setSourceLang(e.target.value as LanguageCode)}
          className="language-select"
        >
          <option value="en">English</option>
          <option value="bn">বাংলা (Bangla)</option>
        </select>

        <button onClick={handleSwapLanguages} className="swap-button" title="Swap languages">
          ⇄
        </button>

        <select
          value={targetLang}
          onChange={(e) => setTargetLang(e.target.value as LanguageCode)}
          className="language-select"
        >
          <option value="en">English</option>
          <option value="bn">বাংলা (Bangla)</option>
        </select>
      </div>

      <div className="translation-panels">
        <div className="panel">
          <div className="panel-header">
            <h3>{getLanguageName(sourceLang)}</h3>
            <div className="panel-actions">
              <span className="char-count">{sourceText.length} / 5000</span>
              {sourceText && (
                <button
                  onClick={() => handleCopyToClipboard(sourceText, 'source')}
                  className="copy-button"
                  title="Copy source text"
                >
                  {copySuccess === 'source' ? '✓ Copied' : '📋 Copy'}
                </button>
              )}
            </div>
          </div>
          <textarea
            value={sourceText}
            onChange={(e) => setSourceText(e.target.value.slice(0, 5000))}
            placeholder="Enter text to translate..."
            className="text-area"
            disabled={isLoading}
          />
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3>{getLanguageName(targetLang)}</h3>
            {translatedText && (
              <button
                onClick={() => handleCopyToClipboard(translatedText, 'translated')}
                className="copy-button"
                title="Copy translated text"
              >
                {copySuccess === 'translated' ? '✓ Copied' : '📋 Copy'}
              </button>
            )}
          </div>
          <textarea
            value={translatedText}
            readOnly
            placeholder="Translation will appear here..."
            className="text-area readonly"
          />
        </div>
      </div>

      <div className="controls">
        <button
          onClick={handleTranslate}
          disabled={isLoading || !sourceText.trim()}
          className="translate-button"
        >
          {isLoading ? 'Translating...' : 'Translate'}
        </button>
        <button onClick={handleClear} disabled={isLoading} className="clear-button">
          Clear
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {processingTime && (
        <div className="info-message">
          Translation completed in {processingTime.toFixed(0)}ms
        </div>
      )}

      {history.length > 0 && (
        <div className="history-section">
          <h3>Recent Translations</h3>
          <div className="history-list">
            {history.map((item) => (
              <button
                key={item.id}
                onClick={() => handleHistoryClick(item)}
                className="history-item"
              >
                <div className="history-text">
                  <strong>{item.sourceLang.toUpperCase()} → {item.targetLang.toUpperCase()}</strong>
                  <span>{item.sourceText.slice(0, 50)}{item.sourceText.length > 50 ? '...' : ''}</span>
                </div>
                <div className="history-time">
                  {item.timestamp.toLocaleTimeString()}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
