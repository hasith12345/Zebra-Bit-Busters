import React from 'react';
import { Activity, Award, Zap, Users } from 'lucide-react';

const LiveIndicator = () => (
  <div className="flex items-center">
    <span className="inline-block w-3 h-3 bg-green-400 rounded-full animate-pulse-slow mr-2 shadow-glow"></span>
    <span className="text-green-400 font-semibold text-sm">LIVE</span>
  </div>
);

const Footer = () => {
  return (
    <div className="text-center bg-glass-light backdrop-blur-xl border border-white border-opacity-20 p-6 rounded-2xl shadow-glass animate-fade-in">
      <div className="flex items-center justify-center flex-wrap gap-4 text-sm text-gray-300">
        <div className="flex items-center">
          <Award className="w-4 h-4 text-yellow-400 mr-2" />
          <span className="font-semibold">Project Sentinel</span>
        </div>
        
        <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
        
        <span>Advanced Retail Intelligence System</span>
        
        <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
        
        <div className="flex items-center">
          <Zap className="w-4 h-4 text-blue-400 mr-1" />
          <span>Powered by Real-time Analytics & ML</span>
        </div>
        
        <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
        
        <div className="flex items-center">
          <Users className="w-4 h-4 text-purple-400 mr-1" />
          <span className="font-semibold text-purple-300">Team Bit-Busters</span>
        </div>
        
        <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
        
        <span>© 2025</span>
        
        <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
        
        <LiveIndicator />
      </div>
    </div>
  );
};

export default Footer;