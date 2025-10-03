import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import SystemOverview from './components/SystemOverview';
import EventTypes from './components/EventTypes';
import StationStatus from './components/StationStatus';
import RecentEvents from './components/RecentEvents';
import SystemStatus from './components/SystemStatus';
import AIDetectionStatus from './components/AIDetectionStatus';
import Footer from './components/Footer';
import './index.css';

function App() {
  const [dashboardData, setDashboardData] = useState({
    totalEvents: 35,
    activeStations: 3,
    averageEfficiency: 96.0,
    eventTypes: [
      { name: 'System Crash', count: 12, percentage: 34.3 },
      { name: 'Inventory Discrepancy', count: 12, percentage: 34.3 },
      { name: 'Scanner Avoidance', count: 11, percentage: 31.4 },
    ],
    stations: [
      { id: 'SC-01', efficiency: 93.0, isActive: true },
      { id: 'SC-02', efficiency: 96.0, isActive: true },
      { id: 'SC-03', efficiency: 99.0, isActive: true },
    ],
    recentEvents: [
      { id: 'E035', type: 'Inventory Discrepancy', timestamp: '2025-10-04T02:26:21' },
      { id: 'E034', type: 'System Crash', timestamp: '2025-10-04T02:26:21' },
      { id: 'E033', type: 'Scanner Avoidance', timestamp: '2025-10-04T02:26:21' },
      { id: 'E032', type: 'Inventory Discrepancy', timestamp: '2025-10-04T02:26:11' },
      { id: 'E031', type: 'System Crash', timestamp: '2025-10-04T02:26:11' },
      { id: 'E030', type: 'Scanner Avoidance', timestamp: '2025-10-04T02:26:11' },
      { id: 'E029', type: 'Inventory Discrepancy', timestamp: '2025-10-04T02:26:01' },
      { id: 'E028', type: 'System Crash', timestamp: '2025-10-04T02:26:01' },
      { id: 'E027', type: 'Scanner Avoidance', timestamp: '2025-10-04T02:26:01' },
      { id: 'E026', type: 'Inventory Discrepancy', timestamp: '2025-10-04T02:25:51' },
    ],
    lastUpdated: new Date().toLocaleString(),
  });

  // Simulate auto-refresh functionality
  useEffect(() => {
    const interval = setInterval(() => {
      // In a real app, this would fetch data from an API
      setDashboardData(prevData => ({
        ...prevData,
        lastUpdated: new Date().toLocaleString(),
        // Simulate slight changes in efficiency
        stations: prevData.stations.map(station => ({
          ...station,
          efficiency: Math.max(85, Math.min(100, station.efficiency + (Math.random() - 0.5) * 2))
        }))
      }));
    }, 3000); // Update every 3 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-main">
      <div className="p-6">
        <Header lastUpdated={dashboardData.lastUpdated} />
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <SystemOverview 
            totalEvents={dashboardData.totalEvents}
            activeStations={dashboardData.activeStations}
            averageEfficiency={dashboardData.averageEfficiency}
          />
          <EventTypes eventTypes={dashboardData.eventTypes} />
          <StationStatus stations={dashboardData.stations} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <RecentEvents events={dashboardData.recentEvents} />
          <SystemStatus totalEvents={dashboardData.totalEvents} />
          <AIDetectionStatus />
        </div>

        <Footer />
      </div>
    </div>
  );
}

export default App;