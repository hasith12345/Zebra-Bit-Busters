import React, { useState, useEffect } from 'react';
import CustomerAlert from './components/CustomerAlert';
import QRCodeDisplay from './components/QRCodeDisplay';
import QueueDisplay from './components/QueueDisplay';
import queueService from './services/queueService';

function App() {
  const [stations, setStations] = useState([]);
  const [totalInQueue, setTotalInQueue] = useState(0);
  const [queueToken, setQueueToken] = useState(null);
  const [queueStatus, setQueueStatus] = useState(null);
  const [selectedStation, setSelectedStation] = useState(null);

  // Get queue token from URL params (simulate customer accessing via QR code)
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const station = urlParams.get('station');
    
    if (token) {
      setQueueToken(token);
    } else if (station) {
      // Generate new token for station if no token provided
      const newToken = queueService.generateVirtualQueueToken(station);
      setQueueToken(newToken);
    }
  }, []);

  // Subscribe to real-time queue updates
  useEffect(() => {
    const unsubscribe = queueService.subscribe((stationData) => {
      setStations(stationData);
      setTotalInQueue(queueService.getTotalCustomersInQueue());
    });

    // Initial data load
    setStations(queueService.getCurrentStationData());
    setTotalInQueue(queueService.getTotalCustomersInQueue());

    return unsubscribe;
  }, []);

  // Check queue status for token holder
  useEffect(() => {
    if (queueToken) {
      const interval = setInterval(() => {
        const status = queueService.checkQueueStatus(queueToken);
        setQueueStatus(status);
      }, 2000);

      return () => clearInterval(interval);
    }
  }, [queueToken]);

  // Handle joining virtual queue
  const handleJoinVirtualQueue = (stationId) => {
    const token = queueService.generateVirtualQueueToken(stationId);
    setQueueToken(token);
    setSelectedStation(stationId);
    
    // In a real app, you might redirect to a new URL with the token
    // window.location.href = `?token=${token}`;
  };

  // Render customer alert view if they have a token
  if (queueToken && queueStatus) {
    return (
      <div className="min-h-screen p-4">
        <div className="max-w-4xl mx-auto">
          <CustomerAlert 
            isReady={queueStatus.isReady}
            stationId={queueStatus.stationId}
            estimatedTime={queueStatus.estimatedTime}
            queuePosition={queueStatus.queuePosition}
            totalInQueue={queueStatus.totalInQueue}
          />
          
          <div className="grid md:grid-cols-2 gap-6">
            <QRCodeDisplay queueToken={queueToken} />
            
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Queue Summary</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Your Station:</span>
                  <span className="font-semibold text-queue-primary">{queueStatus.stationId}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Your Position:</span>
                  <span className="font-semibold">{queueStatus.queuePosition}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Total in All Queues:</span>
                  <span className="font-semibold">{totalInQueue}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Estimated Wait:</span>
                  <span className="font-semibold text-queue-warning">
                    {queueStatus.estimatedTime} min{queueStatus.estimatedTime !== 1 ? 's' : ''}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Render main queue display view
  return (
    <div className="min-h-screen p-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            Virtual Queue System
          </h1>
          <div className="bg-white rounded-lg shadow-lg p-4 inline-block">
            <div className="text-3xl font-bold text-queue-primary">
              {totalInQueue}
            </div>
            <div className="text-sm text-gray-600">Total Customers in Queue</div>
          </div>
        </div>

        <QueueDisplay stations={stations} />

        {/* Virtual Queue Options */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Join Virtual Queue</h2>
          <p className="text-gray-600 mb-6">
            When queues have 6+ customers, you can join a virtual queue and get notified when it's your turn!
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stations
              .filter(station => station.customerCount >= 6)
              .map(station => (
                <div key={station.id} className="border border-red-300 rounded-lg p-4 bg-red-50">
                  <h3 className="font-semibold text-lg text-red-800 mb-2">{station.id}</h3>
                  <p className="text-sm text-red-600 mb-3">
                    {station.customerCount} customers waiting
                  </p>
                  <button
                    onClick={() => handleJoinVirtualQueue(station.id)}
                    className="w-full bg-queue-primary hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors"
                  >
                    Join Virtual Queue
                  </button>
                </div>
              ))}
          </div>

          {stations.filter(station => station.customerCount >= 6).length === 0 && (
            <div className="text-center text-gray-500 py-8">
              <p>No virtual queues currently needed.</p>
              <p className="text-sm mt-1">All stations have fewer than 6 customers.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;