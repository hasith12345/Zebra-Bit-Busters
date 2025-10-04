import React, { useState, useEffect } from 'react';
import { CheckCircle, Clock, Users } from 'lucide-react';

// Simple QR Code Component with larger display
const LargeQRCode = ({ stationId, customerCount }) => {
  return (
    <div className="bg-white rounded-2xl shadow-2xl p-8 text-center max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-red-600 mb-6">🚨 QUEUE ALERT</h2>
      
      {/* Large QR Code Display */}
      <div className="w-64 h-64 bg-gradient-to-br from-red-500 to-orange-600 mx-auto rounded-xl flex items-center justify-center mb-6 shadow-2xl animate-pulse">
        <div className="w-56 h-56 bg-white rounded-lg flex items-center justify-center">
          <div className="text-center p-4">
            <div className="text-4xl font-bold text-gray-800 mb-2">📱 QR CODE</div>
            <div className="text-lg text-gray-600 font-bold">SCAN HERE</div>
            <div className="text-sm text-red-600 font-bold mt-2">{stationId}</div>
            <div className="text-xs text-gray-400 mt-1">Virtual Queue</div>
          </div>
        </div>
      </div>
      
      <div className="space-y-2">
        <p className="text-xl font-bold text-red-600">
          ⚠️ {customerCount} customers waiting!
        </p>
        <p className="text-gray-700 font-semibold">
          Skip the wait - Scan this code to join virtual queue for <span className="font-bold text-blue-600">{stationId}</span>
        </p>
        <p className="text-sm text-gray-600">
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
        <h1 className="text-5xl font-bold mb-4">✅ Your Turn is Ready!</h1>
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
      <h1 className="text-4xl font-bold mb-6">⏰ Please Wait</h1>
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

function TestApp() {
  const [showQR, setShowQR] = useState(true);
  const [showAlert, setShowAlert] = useState(false);
  const [isReady, setIsReady] = useState(false);

  // Demo: Always show busy station for testing QR code
  const busyStation = {
    id: 'SCC1',
    customerCount: 8 // Always busy for demo
  };

  // Get URL parameters
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const station = urlParams.get('station');
    
    if (token || station) {
      setShowAlert(true);
      setShowQR(false);
      
      // Demo: Show ready alert after 5 seconds
      setTimeout(() => {
        setIsReady(true);
      }, 5000);
    }
  }, []);

  // Show customer alert if URL has token/station
  if (showAlert) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-teal-500 flex items-center justify-center p-8">
        <CustomerAlert 
          stationId={busyStation.id}
          isReady={isReady}
          estimatedTime={3}
          customerCount={busyStation.customerCount}
        />
      </div>
    );
  }

  // Always show QR code for demo (since we want to test it)
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-600 via-orange-600 to-yellow-500 flex items-center justify-center p-8">
      <div className="text-center">
        {/* Station Info Header */}
        <div className="bg-white bg-opacity-90 rounded-2xl p-6 mb-8 shadow-2xl">
          <h1 className="text-4xl font-bold text-red-600 mb-2">
            🚨 {busyStation.id} - QUEUE ALERT
          </h1>
          <p className="text-2xl text-red-700 font-bold">
            {busyStation.customerCount} customers waiting
          </p>
          <p className="text-lg text-gray-700 font-semibold">
            Virtual queue available - skip the wait!
          </p>
        </div>

        {/* Large QR Code - THIS SHOULD ALWAYS SHOW NOW */}
        <LargeQRCode 
          stationId={busyStation.id} 
          customerCount={busyStation.customerCount} 
        />

        {/* Test Buttons */}
        <div className="mt-8 space-x-4">
          <button
            onClick={() => {
              setShowAlert(true);
              setShowQR(false);
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow-lg"
          >
            Test Customer Alert
          </button>
          <button
            onClick={() => window.open('?station=SCC1', '_blank')}
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg shadow-lg"
          >
            Test QR Scan (New Tab)
          </button>
        </div>

        {/* Demo Info */}
        <div className="mt-8 bg-white bg-opacity-90 rounded-xl p-4 shadow-xl">
          <p className="text-gray-700 font-semibold">
            🎯 QR Code Demo - Station {busyStation.id} has {busyStation.customerCount} customers
          </p>
          <p className="text-sm text-gray-600 mt-1">
            This large QR code appears when customer count ≥ 6
          </p>
        </div>
      </div>
    </div>
  );
}

export default TestApp;