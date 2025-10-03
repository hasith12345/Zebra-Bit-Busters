import React from 'react';
import { AlertTriangle } from 'lucide-react';

const EventTypeBar = ({ name, count, percentage }) => (
  <div className="mb-4 p-4 bg-gradient-card border border-white border-opacity-10 rounded-xl hover:border-opacity-20 transition-all duration-300">
    <div className="flex justify-between items-center mb-3">
      <span className="font-semibold text-white text-lg">{name}</span>
      <div className="bg-gradient-accent text-white px-3 py-1 rounded-full font-bold text-sm shadow-glow">
        {count}
      </div>
    </div>
    <div className="bg-gray-700 h-2 rounded-full mb-2 overflow-hidden">
      <div 
        className="bg-gradient-to-r from-blue-500 to-cyan-400 h-full rounded-full transition-all duration-500 shadow-inner"
        style={{ width: `${percentage}%` }}
      ></div>
    </div>
    <span className="text-xs text-gray-400 font-medium">{percentage.toFixed(1)}% of total events</span>
  </div>
);

const EventTypes = ({ eventTypes }) => {
  return (
    <div className="bg-glass-light backdrop-blur-xl border border-white border-opacity-20 p-6 rounded-2xl shadow-glass animate-slide-up">
      <div className="flex items-center mb-6">
        <AlertTriangle className="w-6 h-6 text-red-400 mr-3" />
        <h2 className="text-2xl font-bold text-white">Event Types</h2>
      </div>
      <div className="space-y-2">
        {eventTypes.map((event, index) => (
          <EventTypeBar
            key={index}
            name={event.name}
            count={event.count}
            percentage={event.percentage}
          />
        ))}
      </div>
    </div>
  );
};

export default EventTypes;