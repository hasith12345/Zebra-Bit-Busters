import React, { useState, useEffect } from 'react';
import { CheckCircle, Clock, Users } from 'lucide-react';

// Simple QR Code Component with larger display
const LargeQRCode = ({ stationId }) => {
  // Generate QR code content - in production, use proper QR library
  const qrContent = `https://queue.store.com/join/${stationId}`;
  
  return (
    <div className="bg-white rounded-2xl shadow-2xl p-8 text-center max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Virtual Queue Available</h2>
      
      {/* Large QR Code Display */}
      <div className="w-64 h-64 bg-gradient-to-br from-blue-500 to-purple-600 mx-auto rounded-xl flex items-center justify-center mb-6">
        <div className="w-56 h-56 bg-white rounded-lg flex items-center justify-center">
          <div className="text-center p-4">
            <div className="text-4xl font-bold text-gray-800 mb-2">QR CODE</div>
            <div className="text-lg text-gray-600">Scan to Join</div>
            <div className="text-sm text-gray-500 mt-2">{stationId}</div>
            <div className="text-xs text-gray-400 mt-1">Virtual Queue</div>
          </div>
        </div>
      </div>
      
      <div className="space-y-2">
        <p className="text-xl font-semibold text-blue-600">
          Queue is busy - Skip the wait!
        </p>
        <p className="text-gray-600">
          Scan this code to join virtual queue for <span className="font-bold">{stationId}</span>
        </p>
        <p className="text-sm text-gray-500">
          You'll be notified when it's your turn
        </p>
      </div>
    </div>
  );
};

// Customer Alert Component
const CustomerAlert = ({ stationId, isReady, estimatedTime, customerCount }) => {
  if (isReady) {
    return (
      <div className="ready-alert bg-green-500 text-white p-12 rounded-2xl text-center shadow-2xl animate-bounce">
        <CheckCircle className="w-24 h-24 mx-auto mb-6" />
        <h1 className="text-5xl font-bold mb-4">Your Turn is Ready!</h1>
        <p className="text-3xl mb-6">
          Please proceed to <span className="font-bold bg-white text-green-500 px-4 py-2 rounded-lg">{stationId}</span>
        </p>
        <p className="text-xl">
          Your checkout counter is ready now!
        </p>
      </div>
    );
  }

  return (
    <div className="alert-glow bg-blue-500 text-white p-12 rounded-2xl text-center shadow-2xl">
      <Clock className="w-24 h-24 mx-auto mb-6" />
      <h1 className="text-4xl font-bold mb-6">Please Wait</h1>
      <p className="text-2xl mb-6">
        Estimated wait time: <span className="font-bold text-yellow-300">{estimatedTime} minutes</span>
      </p>
      <div className="flex justify-center items-center space-x-8 text-xl">
        <div className="flex items-center bg-white bg-opacity-20 px-4 py-2 rounded-lg">
          <Users className="w-6 h-6 mr-2" />
          <span>Queue: {customerCount} customers</span>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [stationData, setStationData] = useState([]);
  const [busyStations, setBusyStations] = useState([]);
  const [customerToken, setCustomerToken] = useState(null);
  const [alertStation, setAlertStation] = useState(null);
  const [isCustomerReady, setIsCustomerReady] = useState(false);

  // Load real queue data from the dataset
  const loadQueueData = async () => {
    try {
      // Try to fetch from backend API
      const response = await fetch('http://localhost:5001/api/stations');
      if (response.ok) {
        const data = await response.json();
        console.log('📊 Loaded station data:', data);
        setStationData(data.stations);
        
        // Find stations with 6+ customers
        const busy = data.stations.filter(station => station.customerCount >= 6);
        console.log('🚨 Busy stations found:', busy);
        setBusyStations(busy);
      } else {
        console.log('API not available, using simulated data');
        simulateRealData();
      }
    } catch (error) {
      console.log('Backend not running, using simulated data from queue monitoring dataset');
      simulateRealData();
    }
  };

  // Simulate data based on actual queue_monitoring.jsonl patterns
  const simulateRealData = () => {
    const stations = [
      { id: 'SCC1', customerCount: 7, averageDwellTime: 162.9 }, // Force busy for demo
      { id: 'SCC2', customerCount: 3, averageDwellTime: 45.2 },
      { id: 'SCC3', customerCount: 6, averageDwellTime: 76.2 }, // At threshold
      { id: 'SCC4', customerCount: 2, averageDwellTime: 32.1 },
      { id: 'RC1', customerCount: 1, averageDwellTime: 15.5 }
    ];

    console.log('📊 Using simulated data with busy stations');
    setStationData(stations);
    const busy = stations.filter(station => station.customerCount >= 6);
    console.log('🚨 Simulated busy stations:', busy);
    setBusyStations(busy);
  };

  // Simulate customer flow
  const simulateCustomerAlert = () => {
    if (busyStations.length > 0) {
      const randomStation = busyStations[Math.floor(Math.random() * busyStations.length)];
      setAlertStation(randomStation.id);
      
      // Simulate wait time, then ready notification
      setTimeout(() => {
        setIsCustomerReady(true);
      }, 5000); // Show "ready" after 5 seconds for demo
    }
  };

  // Get URL parameters for customer token
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const station = urlParams.get('station');
    
    if (token) {
      setCustomerToken(token);
      setAlertStation(token.split('-')[1] || 'SCC1');
    } else if (station) {
      setAlertStation(station);
    }
  }, []);

  // Load data on mount and refresh periodically
  useEffect(() => {
    loadQueueData();
    const interval = setInterval(loadQueueData, 3000); // Refresh every 3 seconds
    return () => clearInterval(interval);
  }, []);

  // Auto-trigger customer alert demo
  useEffect(() => {
    if (busyStations.length > 0 && !customerToken && !alertStation) {
      const timer = setTimeout(simulateCustomerAlert, 2000);
      return () => clearTimeout(timer);
    }
  }, [busyStations]);

  // Show customer alert if we have an alert station
  if (alertStation) {
    const stationInfo = stationData.find(s => s.id === alertStation) || { customerCount: 6 };
    const estimatedTime = Math.ceil(stationInfo.customerCount * 1.5); // Rough estimate
    
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-teal-500 flex items-center justify-center p-8">
        <CustomerAlert 
          stationId={alertStation}
          isReady={isCustomerReady}
          estimatedTime={estimatedTime}
          customerCount={stationInfo.customerCount}
        />
      </div>
    );
  }

  // Show large QR code for the busiest station
  if (busyStations.length > 0) {
    const busiestStation = busyStations.reduce((prev, current) => 
      (prev.customerCount > current.customerCount) ? prev : current
    );

    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-teal-500 flex items-center justify-center p-8">
        <div className="text-center">
          {/* Station Info Header */}
          <div className="bg-white bg-opacity-90 rounded-2xl p-6 mb-8 shadow-2xl">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              {busiestStation.id} - Queue Alert
            </h1>
            <p className="text-xl text-red-600 font-semibold">
              {busiestStation.customerCount} customers waiting
            </p>
            <p className="text-gray-600">
              Virtual queue available - skip the wait!
            </p>
          </div>

          {/* Large QR Code */}
          <LargeQRCode stationId={busiestStation.id} />

          {/* Additional Info */}
          <div className="mt-8 bg-white bg-opacity-90 rounded-xl p-4 shadow-xl">
            <p className="text-gray-700">
              <span className="font-bold">All Stations Status:</span>
            </p>
            <div className="flex justify-center space-x-4 mt-2">
              {stationData.map(station => (
                <div key={station.id} className={`px-3 py-1 rounded-lg text-sm font-medium ${
                  station.customerCount >= 6 ? 'bg-red-200 text-red-800' :
                  station.customerCount >= 3 ? 'bg-yellow-200 text-yellow-800' :
                  'bg-green-200 text-green-800'
                }`}>
                  {station.id}: {station.customerCount}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Show normal status when no stations are busy
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-500 via-blue-500 to-purple-500 flex items-center justify-center p-8">
      <div className="bg-white rounded-2xl shadow-2xl p-12 text-center max-w-2xl">
        <h1 className="text-4xl font-bold text-gray-800 mb-6">
          All Stations Running Smoothly
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          No virtual queues needed at this time
        </p>
        
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {stationData.map(station => (
            <div key={station.id} className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="font-bold text-green-800">{station.id}</div>
              <div className="text-sm text-green-600">{station.customerCount} customers</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;