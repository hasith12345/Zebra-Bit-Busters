import React from 'react';
import { Clock, AlertCircle, Bug, Shield } from 'lucide-react';

const getEventIcon = (type) => {
  switch (type.toLowerCase()) {
    case 'system crash':
      return <Bug className="w-4 h-4 text-red-400" />;
    case 'inventory discrepancy':
      return <AlertCircle className="w-4 h-4 text-yellow-400" />;
    case 'scanner avoidance':
      return <Shield className="w-4 h-4 text-orange-400" />;
    default:
      return <AlertCircle className="w-4 h-4 text-blue-400" />;
  }
};

const EventItem = ({ event }) => {
  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="p-3 mb-3 rounded-xl bg-gradient-card border border-white border-opacity-10 hover:border-opacity-20 transition-all duration-300 hover:transform hover:scale-105">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center">
          {getEventIcon(event.type)}
          <span className="font-semibold text-white ml-2">{event.type}</span>
        </div>
        <div className="bg-blue-500 bg-opacity-20 text-blue-300 px-2 py-1 rounded-full text-xs font-mono">
          {event.id}
        </div>
      </div>
      <div className="flex items-center text-xs text-gray-400">
        <Clock className="w-3 h-3 mr-1" />
        {formatTimestamp(event.timestamp)}
      </div>
    </div>
  );
};

const RecentEvents = ({ events }) => {
  return (
    <div className="bg-glass-light backdrop-blur-xl border border-white border-opacity-20 p-6 rounded-2xl shadow-glass animate-slide-up">
      <div className="flex items-center mb-6">
        <Clock className="w-6 h-6 text-green-400 mr-3" />
        <h2 className="text-2xl font-bold text-white">Recent Events</h2>
      </div>
      <div className="max-h-72 overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
        {events.map((event, index) => (
          <EventItem key={index} event={event} />
        ))}
      </div>
    </div>
  );
};

export default RecentEvents;