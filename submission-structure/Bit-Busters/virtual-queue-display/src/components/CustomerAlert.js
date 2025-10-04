import React from 'react';
import { Clock, Users, CheckCircle } from 'lucide-react';

const CustomerAlert = ({ 
  isReady, 
  stationId, 
  estimatedTime, 
  queuePosition, 
  totalInQueue 
}) => {
  if (isReady) {
    return (
      <div className="ready-alert bg-green-500 text-white p-8 rounded-lg text-center mb-6">
        <CheckCircle className="w-16 h-16 mx-auto mb-4" />
        <h1 className="text-3xl font-bold mb-2">Your Turn is Ready!</h1>
        <p className="text-xl mb-4">
          Please proceed to <span className="font-bold">{stationId}</span>
        </p>
        <p className="text-lg">
          Your checkout counter is ready now!
        </p>
      </div>
    );
  }

  return (
    <div className="alert-glow bg-blue-500 text-white p-8 rounded-lg text-center mb-6">
      <Clock className="w-16 h-16 mx-auto mb-4" />
      <h1 className="text-3xl font-bold mb-2">Please Wait</h1>
      <p className="text-xl mb-4">
        Estimated wait time: <span className="font-bold">{estimatedTime} minutes</span>
      </p>
      <div className="flex justify-center items-center space-x-6 text-lg">
        <div className="flex items-center">
          <Users className="w-6 h-6 mr-2" />
          <span>Position: {queuePosition}</span>
        </div>
        <div className="flex items-center">
          <Users className="w-6 h-6 mr-2" />
          <span>Total in Queue: {totalInQueue}</span>
        </div>
      </div>
    </div>
  );
};

export default CustomerAlert;