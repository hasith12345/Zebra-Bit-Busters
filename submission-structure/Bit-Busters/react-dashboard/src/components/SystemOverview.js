import React from 'react';
import { Target, Activity, TrendingUp } from 'lucide-react';

const MetricCard = ({ value, label, icon: Icon, color }) => (
  <div className="text-center p-6 m-2 rounded-2xl bg-gradient-card border border-white border-opacity-10 hover:border-opacity-20 transition-all duration-300 hover:transform hover:scale-105">
    <div className="flex items-center justify-center mb-3">
      <Icon className={`w-8 h-8 ${color} mr-3`} />
    </div>
    <div className={`text-4xl font-bold mb-2 ${color}`}>{value}</div>
    <div className="text-gray-300 text-sm font-medium">{label}</div>
  </div>
);

const SystemOverview = ({ totalEvents, activeStations, averageEfficiency }) => {
  return (
    <div className="bg-glass-light backdrop-blur-xl border border-white border-opacity-20 p-6 rounded-2xl shadow-glass animate-slide-up">
      <div className="flex items-center mb-6">
        <Target className="w-6 h-6 text-sentinel-blue mr-3" />
        <h2 className="text-2xl font-bold text-white">System Overview</h2>
      </div>
      <div className="space-y-2">
        <MetricCard 
          value={totalEvents} 
          label="Total Events Detected" 
          icon={Activity}
          color="text-blue-400"
        />
        <MetricCard 
          value={activeStations} 
          label="Active Stations" 
          icon={Activity}
          color="text-green-400"
        />
        <MetricCard 
          value={`${averageEfficiency.toFixed(1)}%`} 
          label="Average Efficiency" 
          icon={TrendingUp}
          color="text-cyan-400"
        />
      </div>
    </div>
  );
};

export default SystemOverview;