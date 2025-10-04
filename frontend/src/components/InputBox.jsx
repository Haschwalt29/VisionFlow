import React, { useState } from 'react';

const InputBox = ({ onSubmit, isLoading }) => {
  const [url, setUrl] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim() && onSubmit) {
      onSubmit(url.trim());
    }
  };
  
  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };
  
  return (
    <div className="glass rounded-2xl p-8 shadow-xl">
      <div className="mb-6">
        <h1 className="text-4xl font-bold gradient-text mb-2">
          VisionFlow
        </h1>
        <p className="text-lg text-gray-400">
          AI Workflow Automation Agent
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Extract structured data from any webpage using advanced AI
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg 
              className="h-5 w-5 text-gray-400" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 01-5.656 5.656l-1.102-1.101m0 0L16 11l-4-4m0 0L8 13l4 4" 
              />
            </svg>
          </div>
          <input
            type="url"
            value={url}
            onChange={handleUrlChange}
            placeholder="Enter webpage URL (e.g., https://openai.com)"
            className="block w-full pl-12 pr-4 py-4 border border-gray-600 rounded-lg bg-gray-800/50 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            disabled={isLoading}
          />
        </div>
        
        <button
          type="submit"
          disabled={!url.trim() || isLoading}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02] disabled:hover:scale-100 disabled:cursor-not-allowed shadow-lg"
        >
          {isLoading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="dots-loader">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span>Extracting Data...</span>
            </div>
          ) : (
            <div className="flex items-center justify-center space-x-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span>Extract Data</span>
            </div>
          )}
        </button>
      </form>
      
      <div className="mt-6 grid grid-cols-3 gap-4 text-center">
        <div className="text-sm">
          <div className="font-semibold text-green-400">✓ Fast</div>
          <div className="text-gray-500">2-5 seconds</div>
        </div>
        <div className="text-sm">
          <div className="font-semibold text-blue-400">🖥️ Smart</div>
          <div className="text-gray-500">Smart AI</div>
        </div>
        <div className="text-sm">
          <div className="font-semibold text-purple-400">📦 JSON</div>
          <div className="text-gray-500">Structured output</div>
        </div>
      </div>
    </div>
  );
};

export default InputBox;
