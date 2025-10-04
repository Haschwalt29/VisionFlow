import React, { useMemo } from 'react';

const DataTable = React.memo(({ extractions, isLoading }) => {
  // Memoize formatted extractions to prevent unnecessary re-renders
  const formattedExtractions = useMemo(() => {
    if (!extractions || extractions.length === 0) return [];
    return extractions.map(extraction => ({
      ...extraction,
      formattedDate: new Date(extraction.extracted_at),
    }));
  }, [extractions]);

  if (isLoading) {
    return (
      <div className="glass rounded-2xl p-8 shadow-xl">
        <div className="flex items-center justify-center py-12">
          <div className="dots-loader text-blue-400">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span className="ml-3 text-gray-400">Loading extractions...</span>
        </div>
      </div>
    );
  }
  
  if (!extractions || extractions.length === 0) {
    return (
      <div className="glass rounded-2xl p-8 shadow-xl">
        <div className="text-center py-12">
          <div className="w-16 h-16 mx-auto mb-4 bg-gray-700 rounded-full flex items-center justify-center">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-300 mb-2">No extractions yet</h3>
          <p className="text-gray-500">Extract data from a webpage to see results here</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="glass rounded-2xl p-8 shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">Extracted Data</h2>
          <p className="text-gray-400">{formattedExtractions.length} extraction{formattedExtractions.length !== 1 ? 's' : ''}</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-400">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span>Live updates</span>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b-2 border-gray-600/50">
              <th className="pb-6 pr-6 text-sm font-bold text-gray-200 uppercase tracking-wide w-1/6">Name</th>
              <th className="pb-6 pr-6 text-sm font-bold text-gray-200 uppercase tracking-wide w-1/3">Description</th>
              <th className="pb-6 pr-6 text-sm font-bold text-gray-200 uppercase tracking-wide w-1/4">Features</th>
              <th className="pb-6 pr-6 text-sm font-bold text-gray-200 uppercase tracking-wide w-1/6">Pricing</th>
              <th className="pb-6 pr-6 text-sm font-bold text-gray-200 uppercase tracking-wide w-1/12">URL</th>
              <th className="pb-6 text-sm font-bold text-gray-200 uppercase tracking-wide w-1/12">Extracted</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-600/30">
            {formattedExtractions.map((extraction, index) => (
              <tr key={extraction.id || index} className="hover:bg-gray-700/30 transition-all duration-200 group">
                <td className="py-8 pr-6 align-top">
                  <div className="font-semibold text-white text-base leading-6">
                    {extraction.name || 'N/A'}
                  </div>
                </td>
                <td className="py-8 pr-6 align-top">
                  <div className="text-gray-300 text-sm leading-6 pr-4">
                    {extraction.description ? (
                      extraction.description.length > 150 
                        ? `${extraction.description.substring(0, 150)}...`
                        : extraction.description
                    ) : 'N/A'}
                  </div>
                </td>
                <td className="py-8 pr-6 align-top">
                  <div className="text-sm text-gray-300">
                    {extraction.features ? (
                      <div className="flex flex-wrap gap-2">
                        {extraction.features.split(',').slice(0, 4).map((feature, fIndex) => (
                          <span 
                            key={fIndex}
                            className="inline-block bg-blue-500/20 text-blue-300 text-xs px-3 py-1.5 rounded-lg font-medium hover:bg-blue-500/30 transition-colors"
                          >
                            {feature.trim()}
                          </span>
                        ))}
                        {extraction.features.split(',').length > 4 && (
                          <span className="text-gray-400 text-xs bg-gray-600/20 px-2 py-1 rounded-lg">
                            +{extraction.features.split(',').length - 4} more
                          </span>
                        )}
                      </div>
                    ) : 'N/A'}
                  </div>
                </td>
                <td className="py-8 pr-6 align-top">
                  <div className="text-sm font-medium text-green-400 bg-green-500/10 px-3 py-2 rounded-lg border border-green-500/20">
                    {extraction.pricing || 'N/A'}
                  </div>
                </td>
                <td className="py-8 pr-6 align-top">
                  <a 
                    href={extraction.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 text-sm underline hover:no-underline transition-colors bg-blue-500/10 px-2 py-1 rounded font-medium"
                  >
                    {new URL(extraction.url).hostname}
                  </a>
                </td>
                <td className="py-8 pr-6 align-top">
                  <div className="text-sm text-gray-300 font-medium">
                    {extraction.formattedDate.toLocaleDateString()}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {extraction.formattedDate.toLocaleTimeString()}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="mt-6 flex items-center justify-between text-sm text-gray-500">
        <div className="flex items-center space-x-4">
          <span>
            <span className="font-medium text-gray-400">{formattedExtractions.length}</span> total extractions
          </span>
        </div>
      </div>
    </div>
  );
});

export default DataTable;
