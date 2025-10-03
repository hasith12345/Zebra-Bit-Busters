import React from 'react';
import { Monitor, Wifi, WifiOff } from 'lucide-react';

const StatusIndicator = ({ isActive }) => (
  <div className="flex items-center">
    {isActive ? (
      <Wifi className="w-4 h-4 text-green-400 mr-2" />
    ) : (
      <WifiOff className="w-4 h-4 text-red-400 mr-2" />
    )}
    <span className={`inline-block w-3 h-3 rounded-full mr-2 shadow-glow ${
      isActive ? 'bg-green-400 animate-pulse-slow' : 'bg-red-400'
    }`}></span>
  </div>
);

const StationCard = ({ station }) => {
  const getEfficiencyColor = (efficiency) => {
    if (efficiency >= 95) return 'from-green-500 to-emerald-400';
    if (efficiency >= 90) return 'from-blue-500 to-cyan-400';
    if (efficiency >= 80) return 'from-yellow-500 to-orange-400';
    return 'from-red-500 to-pink-400';
  };

  return (
    <div className="p-4 mb-3 bg-gradient-card border border-white border-opacity-10 rounded-xl hover:border-opacity-20 transition-all duration-300 hover:transform hover:scale-105">
      <div className="flex justify-between items-center mb-3">
        <div className="flex items-center">
          <StatusIndicator isActive={station.isActive} />
          <strong className="text-white text-lg">Station {station.id}</strong>
        </div>
        <div className={`text-xs px-3 py-1 rounded-full font-semibold ${
          station.isActive 
            ? 'bg-green-500 bg-opacity-20 text-green-400 border border-green-400 border-opacity-30' 
            : 'bg-red-500 bg-opacity-20 text-red-400 border border-red-400 border-opacity-30'
        }`}>
          {station.isActive ? 'ACTIVE' : 'INACTIVE'}
        </div>
      </div>
      <div className="mt-3">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-300">Efficiency</span>
          <span className="text-lg font-bold text-white">{station.efficiency.toFixed(1)}%</span>
        </div>
        <div className="bg-gray-700 h-2 rounded-full overflow-hidden">
          <div 
            className={`bg-gradient-to-r ${getEfficiencyColor(station.efficiency)} h-full rounded-full transition-all duration-500 shadow-inner`}
            style={{ width: `${station.efficiency}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

const StationStatus = ({ stations }) => {
  return (
    <div className="bg-glass-light backdrop-blur-xl border border-white border-opacity-20 p-6 rounded-2xl shadow-glass animate-slide-up">
      <div className="flex items-center mb-6">
        <Monitor className="w-6 h-6 text-blue-400 mr-3" />
        <h2 className="text-2xl font-bold text-white">Station Status</h2>
      </div>
      <div className="space-y-2">
        {stations.map((station, index) => (
          <StationCard key={index} station={station} />
        ))}
      </div>
    </div>
  );
};

export default StationStatus;