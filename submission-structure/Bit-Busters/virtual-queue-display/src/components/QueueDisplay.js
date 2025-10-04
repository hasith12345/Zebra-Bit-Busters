import React from 'react';
import { Users, Clock } from 'lucide-react';

const QueueDisplay = ({ stations }) => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Queue Status</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stations.map((station) => (
          <div 
            key={station.id} 
            className={`p-4 rounded-lg border-2 ${
              station.customerCount >= 6 
                ? 'border-red-400 bg-red-50' 
                : station.customerCount >= 3 
                ? 'border-yellow-400 bg-yellow-50' 
                : 'border-green-400 bg-green-50'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-semibold text-lg">{station.id}</h3>
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                station.customerCount >= 6 
                  ? 'bg-red-200 text-red-800' 
                  : station.customerCount >= 3 
                  ? 'bg-yellow-200 text-yellow-800' 
                  : 'bg-green-200 text-green-800'
              }`}>
                {station.status}
              </div>
            </div>
            <div className="flex items-center space-x-4 text-sm">
              <div className="flex items-center">
                <Users className="w-4 h-4 mr-1" />
                <span>{station.customerCount} customers</span>
              </div>
              <div className="flex items-center">
                <Clock className="w-4 h-4 mr-1" />
                <span>{Math.round(station.averageDwellTime)}s avg</span>
              </div>
            </div>
            {station.customerCount >= 6 && (
              <div className="mt-2 text-xs text-red-600 font-medium">
                Virtual Queue Available
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default QueueDisplay;