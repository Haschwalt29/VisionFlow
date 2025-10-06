import React, { useState, useEffect } from 'react';
import axios from 'axios';
import InputBox from './components/InputBox';
import DataTable from './components/DataTable';
import './index.css';

// Configure axios base URL
const API_BASE_URL = (() => {
  // For production builds, use environment variable (set via Netlify)
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // For development, default to localhost
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:5000';
  }
  
  // Default fallback for production
  return 'https://visionflow-backend.onrender.com';
})();
axios.defaults.baseURL = API_BASE_URL;
// Set a sane default timeout so the UI doesn't hang forever on network issues
axios.defaults.timeout = 30000; // 30 seconds to tolerate cold starts

function App() {
  const [extractions, setExtractions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingData, setIsLoadingData] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // Fetch data on component mount
  useEffect(() => {
    // Initial load with retries to tolerate backend cold starts
    const fetchWithRetry = async () => {
      const maxAttempts = 3;
      let attempt = 0;
      let lastError = null;
      while (attempt < maxAttempts) {
        try {
          await fetchData(true);
          lastError = null;
          break;
        } catch (err) {
          lastError = err;
          const backoffMs = 1000 * Math.pow(2, attempt); // 1s, 2s, 4s
          await new Promise(r => setTimeout(r, backoffMs));
        }
        attempt += 1;
      }
      if (lastError) {
        // Ensure loading stops if all retries failed
        setIsLoadingData(false);
      }
    };
    fetchWithRetry();
    
    // Set up polling for real-time updates (silent updates)
    const interval = setInterval(() => fetchData(false), 8000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async (showLoading = false) => {
    try {
      if (showLoading) {
        setIsLoadingData(true);
      }
      const response = await axios.get('/data');
      if (response.data.success) {
        setExtractions(response.data.data);
        // Clear any previous error if data loads successfully
        setError(null);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      // Surface the error to the user and stop the loading spinner
      const message =
        error.code === 'ECONNABORTED'
          ? 'Request timed out while loading data. Please check the backend.'
          : (error.response?.data?.error || error.message || 'Failed to load data');
      setError(message);
      // Re-throw so caller (retry wrapper) can handle it
      throw error;
    } finally {
      if (showLoading) {
        setIsLoadingData(false);
      }
    }
  };

  const handleExtract = async (url) => {
    setIsLoading(true);
    setError(null);
    setSuccessMessage(null);
    
    try {
      const response = await axios.post('/extract', { url });
      
      if (response.data.success) {
        setSuccessMessage(`Successfully extracted data from ${new URL(url).hostname}`);
        // Refresh data after successful extraction (silent)
        await fetchData(false);
      } else {
        setError(response.data.error || 'Extraction failed');
      }
    } catch (error) {
      console.error('Extraction error:', error);
      setError(
        error.response?.data?.error || 
        error.message || 
        'Failed to connect to the extraction service'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const clearMessages = () => {
    setError(null);
    setSuccessMessage(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      {/* Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1.5s' }}></div>
      </div>
      
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center space-x-3 bg-gray-800/50 rounded-full px-6 py-3 mb-6">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span className="text-gray-300 font-medium">VisionFlow Demo</span>
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-xs text-gray-400">Live</span>
            </div>
          </div>
          
          <h1 className="text-5xl font-bold text-white mb-4 animate-fade-in">
            AI Workflow Automation
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto animate-fade-in" style={{ animationDelay: '0.1s' }}>
            Extract structured data from any webpage using advanced AI. 
            Perfect for competitive analysis, market research, and automation workflows.
          </p>
        </div>

        {/* Status Messages */}
        {error && (
          <div className="mx-auto max-w-2xl mb-6 animate-slide-up">
            <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-4 flex items-center space-x-3">
              <svg className="w-6 h-6 text-red-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="flex-1">
                <p className="text-red-300 font-medium">Extraction Failed</p>
                <p className="text-red-400 text-sm">{error}</p>
              </div>
              <button 
                onClick={clearMessages}
                className="text-red-400 hover:text-red-300 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}
        
        {successMessage && (
          <div className="mx-auto max-w-2xl mb-6 animate-slide-up">
            <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-4 flex items-center space-x-3">
              <svg className="w-6 h-6 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="flex-1">
                <p className="text-green-300 font-medium">Extraction Successful</p>
                <p className="text-green-400 text-sm">{successMessage}</p>
              </div>
              <button 
                onClick={clearMessages}
                className="text-green-400 hover:text-green-300 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="max-w-7xl mx-auto space-y-8">
          {/* Input Section */}
          <div className="animate-slide-up max-w-2xl mx-auto">
            <InputBox onSubmit={handleExtract} isLoading={isLoading} />
          </div>
          
          {/* Results Section */}
          <div className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <DataTable extractions={extractions} isLoading={isLoadingData} />
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center">
          <div className="flex items-center justify-center space-x-6 text-sm text-gray-400">
            <div className="flex items-center space-x-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>Built with Flask + React</span>
            </div>
            <div className="flex items-center space-x-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2V7z" />
              </svg>
              <span>SQLite Database</span>
            </div>
          </div>
          
          <div className="mt-4">
            <a 
              href="https://github.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-gray-500 hover:text-gray-300 transition-colors text-sm underline"
            >
              View Source Code →
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
