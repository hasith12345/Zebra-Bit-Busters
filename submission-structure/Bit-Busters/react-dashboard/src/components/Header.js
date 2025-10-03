import React from 'react';
import { Activity } from 'lucide-react';

const LiveIndicator = () => (
  <div className="flex items-center">
    <span className="inline-block w-3 h-3 bg-green-400 rounded-full animate-pulse-slow mr-2 shadow-glow"></span>
    <span className="text-green-400 font-semibold text-sm">LIVE</span>
  </div>
);

const Header = ({ lastUpdated }) => {
  return (
    <div className="text-center bg-glass-light backdrop-blur-xl border border-white border-opacity-20 p-8 rounded-3xl mb-6 shadow-glass animate-fade-in">
      <div className="flex items-center justify-center mb-4">
        <Activity className="w-8 h-8 text-sentinel-blue mr-3" />
        <h1 className="text-4xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
          Project Sentinel
        </h1>
      </div>
      <p className="text-xl text-gray-300 mb-2">Retail Intelligence Dashboard</p>
      <div className="flex items-center justify-center space-x-4 mb-4">
        <span className="text-sentinel-accent font-semibold">Team Bit-Busters</span>
        <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
        <LiveIndicator />
        <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
        <span className="text-gray-400">Real-time Analytics & Threat Detection</span>
      </div>
      <div className="text-sm text-gray-400 bg-black bg-opacity-20 px-4 py-2 rounded-full inline-block">
        Last Updated: {lastUpdated} | Auto-refresh: 3 seconds
      </div>
    </div>
  );
};

export default Header;