import React from 'react';
import { Settings, CheckCircle, AlertTriangle, XCircle, Database, Wifi, BarChart3 } from 'lucide-react';

const StatusItem = ({ icon: Icon, text, status = 'success' }) => {
  const statusConfig = {
    success: {
      bgColor: 'bg-green-500 bg-opacity-20',
      borderColor: 'border-green-400 border-opacity-30',
      textColor: 'text-green-400',
      iconColor: 'text-green-400'
    },
    warning: {
      bgColor: 'bg-yellow-500 bg-opacity-20',
      borderColor: 'border-yellow-400 border-opacity-30',
      textColor: 'text-yellow-400',
      iconColor: 'text-yellow-400'
    },
    error: {
      bgColor: 'bg-red-500 bg-opacity-20',
      borderColor: 'border-red-400 border-opacity-30',
      textColor: 'text-red-400',
      iconColor: 'text-red-400'
    }
  };

  const config = statusConfig[status];

  return (
    <div className={`p-3 mb-3 rounded-xl border ${config.bgColor} ${config.borderColor} ${config.textColor} flex items-center transition-all duration-300 hover:scale-105`}>
      <Icon className={`w-5 h-5 mr-3 ${config.iconColor}`} />
      <span className="font-medium">{text}</span>
    </div>
  );
};

const MetricRow = ({ label, value, icon: Icon }) => (
  <div className="flex justify-between items-center py-3 border-b border-gray-600 last:border-b-0">
    <div className="flex items-center">
      <Icon className="w-4 h-4 text-gray-400 mr-2" />
      <span className="text-gray-300">{label}:</span>
    </div>
    <span className="text-cyan-400 font-bold text-lg">{value}</span>
  </div>
);

const SystemStatus = ({ totalEvents }) => {
  return (
    <div className="bg-glass-light backdrop-blur-xl border border-white border-opacity-20 p-6 rounded-2xl shadow-glass animate-slide-up">
      <div className="flex items-center mb-6">
        <Settings className="w-6 h-6 text-purple-400 mr-3" />
        <h2 className="text-2xl font-bold text-white">System Status</h2>
      </div>
      
      <div className="space-y-2 mb-6">
        <StatusItem icon={Database} text="Data Processor: Online" />
        <StatusItem icon={CheckCircle} text="Event Detector: Active" />
        <StatusItem icon={BarChart3} text="Dashboard: Live Auto-Update" />
        <StatusItem icon={Wifi} text="Streaming Client: Connected" />
      </div>
      
      <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
        <BarChart3 className="w-5 h-5 mr-2 text-cyan-400" />
        Live Metrics
      </h3>
      <div className="bg-gradient-card border border-white border-opacity-10 p-4 rounded-xl">
        <MetricRow label="Total Events" value={totalEvents} icon={Database} />
        <MetricRow label="System Uptime" value="100%" icon={CheckCircle} />
        <MetricRow label="Last Refresh" value="Live" icon={Wifi} />
      </div>
    </div>
  );
};

export default SystemStatus;