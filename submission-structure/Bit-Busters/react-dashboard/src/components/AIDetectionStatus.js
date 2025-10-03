import React from 'react';
import { Brain, Eye, BarChart, Users, Package, Network, Clock, Shield, Zap } from 'lucide-react';

const getCapabilityIcon = (capability) => {
  switch (capability.toLowerCase()) {
    case 'scanner avoidance detection':
      return <Eye className="w-4 h-4 text-blue-400" />;
    case 'barcode switching detection':
      return <Shield className="w-4 h-4 text-red-400" />;
    case 'weight discrepancy analysis':
      return <BarChart className="w-4 h-4 text-yellow-400" />;
    case 'behavioral pattern analysis':
      return <Users className="w-4 h-4 text-purple-400" />;
    case 'inventory prediction':
      return <Package className="w-4 h-4 text-green-400" />;
    case 'multi-station correlation':
      return <Network className="w-4 h-4 text-cyan-400" />;
    case 'dynamic staffing optimization':
      return <Users className="w-4 h-4 text-orange-400" />;
    case 'queue management':
      return <Clock className="w-4 h-4 text-indigo-400" />;
    case 'system performance monitoring':
      return <Zap className="w-4 h-4 text-pink-400" />;
    default:
      return <Brain className="w-4 h-4 text-blue-400" />;
  }
};

const DetectionItem = ({ text }) => (
  <div className="flex items-center p-3 mb-2 rounded-xl bg-gradient-card border border-white border-opacity-10 hover:border-opacity-20 transition-all duration-300 hover:transform hover:scale-105">
    {getCapabilityIcon(text)}
    <span className="text-sm text-white font-medium ml-3">{text}</span>
    <div className="ml-auto">
      <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse-slow"></div>
    </div>
  </div>
);

const AIDetectionStatus = () => {
  const detectionCapabilities = [
    'Scanner Avoidance Detection',
    'Barcode Switching Detection',
    'Weight Discrepancy Analysis',
    'Behavioral Pattern Analysis',
    'Inventory Prediction',
    'Multi-Station Correlation',
    'Dynamic Staffing Optimization',
    'Queue Management',
    'System Performance Monitoring'
  ];

  return (
    <div className="bg-glass-light backdrop-blur-xl border border-white border-opacity-20 p-6 rounded-2xl shadow-glass animate-slide-up">
      <div className="flex items-center mb-6">
        <Brain className="w-6 h-6 text-pink-400 mr-3 animate-glow" />
        <h2 className="text-2xl font-bold text-white">AI Detection Status</h2>
      </div>
      <div className="space-y-2 max-h-64 overflow-y-auto pr-2">
        {detectionCapabilities.map((capability, index) => (
          <DetectionItem key={index} text={capability} />
        ))}
      </div>
    </div>
  );
};

export default AIDetectionStatus;