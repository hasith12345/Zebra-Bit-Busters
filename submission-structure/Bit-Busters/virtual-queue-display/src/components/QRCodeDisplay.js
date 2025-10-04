import React from 'react';

const QRCodeDisplay = ({ queueToken }) => {
  // Static QR code content - in real implementation, this would be a URL to the queue status page
  const qrCodeContent = `https://queue.store.com/status/${queueToken}`;
  
  // Simple QR code placeholder - you can use a library like qrcode-generator for actual QR codes
  const generateQRCode = (text) => {
    // For demo purposes, showing a text representation
    // In production, use a proper QR code library
    return (
      <div className="w-32 h-32 bg-white border-2 border-gray-300 flex items-center justify-center">
        <div className="text-xs text-center p-2">
          <div className="font-bold">QR CODE</div>
          <div className="text-xs mt-1">Token: {queueToken}</div>
        </div>
      </div>
    );
  };

  return (
    <div className="qr-container text-center">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Your Queue Token</h3>
      <div className="flex justify-center mb-4">
        {generateQRCode(qrCodeContent)}
      </div>
      <p className="text-sm text-gray-600 mb-2">
        Token: <span className="font-bold text-queue-primary">{queueToken}</span>
      </p>
      <p className="text-xs text-gray-500">
        Scan this code or use your token to check queue status
      </p>
    </div>
  );
};

export default QRCodeDisplay;