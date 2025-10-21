/**
 * Main App component
 */
import { useEffect, useState } from 'react';
import TranslationInterface from './components/TranslationInterface';
import { checkHealth } from './services/api';
import './App.css';

function App() {
  const [healthStatus, setHealthStatus] = useState<{
    isHealthy: boolean;
    vllmConnected: boolean;
  } | null>(null);
  const [showHealthCheck, setShowHealthCheck] = useState(true);

  useEffect(() => {
    // Check health on mount
    const performHealthCheck = async () => {
      try {
        const health = await checkHealth();
        setHealthStatus({
          isHealthy: health.status === 'healthy',
          vllmConnected: health.vllm_connected,
        });
      } catch (error) {
        setHealthStatus({
          isHealthy: false,
          vllmConnected: false,
        });
      }
    };

    performHealthCheck();
  }, []);

  return (
    <div className="app">
      {showHealthCheck && healthStatus && (
        <div className={`health-banner ${healthStatus.isHealthy ? 'healthy' : 'unhealthy'}`}>
          <div className="health-content">
            <span>
              Backend: {healthStatus.isHealthy ? '✓ Connected' : '✗ Disconnected'} |
              vLLM: {healthStatus.vllmConnected ? '✓ Connected' : '✗ Disconnected'}
            </span>
            <button onClick={() => setShowHealthCheck(false)} className="close-banner">
              ×
            </button>
          </div>
        </div>
      )}

      <main className="main-content">
        <TranslationInterface />
      </main>

      <footer className="footer">
        <p>English-Bangla Translator v1.0.0 | Powered by vLLM</p>
      </footer>
    </div>
  );
}

export default App;
