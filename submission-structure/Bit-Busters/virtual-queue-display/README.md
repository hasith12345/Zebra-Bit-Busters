# Virtual Queue Display System

A React-based virtual queue display system that shows queue status and customer alerts for retail environments.

## Features

- **Real-time Queue Monitoring**: Displays current queue status for all checkout stations
- **Virtual Queue System**: Allows customers to join virtual queues when stations have 6+ customers
- **Customer Alerts**: Notifies customers when their turn is ready
- **QR Code Integration**: Provides static QR codes for easy access to queue status
- **Responsive Design**: Works on displays and mobile devices

## Directory Structure

```
virtual-queue-display/
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── CustomerAlert.js     # Alert component for ready customers
│   │   ├── QRCodeDisplay.js     # QR code display component
│   │   └── QueueDisplay.js      # Main queue status display
│   ├── services/
│   │   └── queueService.js      # Data service for queue management
│   ├── App.js                   # Main application component
│   ├── index.js                 # Entry point
│   └── index.css                # Styles and animations
├── tailwind.config.js           # Tailwind CSS configuration
└── postcss.config.js            # PostCSS configuration
```

## Installation and Setup

1. Navigate to the virtual-queue-display directory:
   ```bash
   cd virtual-queue-display
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser to `http://localhost:3000`

## Usage

### Main Queue Display
- Shows all checkout stations (SCC1, SCC2, SCC3, SCC4, RC1)
- Displays customer count and average dwell time for each station
- Highlights stations that need virtual queue (6+ customers)
- Shows total customers in all queues

### Virtual Queue System
- Customers can join virtual queues for busy stations
- Static QR codes provide easy access to queue status
- Real-time notifications when customer's turn is ready

### URL Parameters
- `?station=SCC1` - Generate new virtual queue token for station
- `?token=VQ-SCC1-ABC123` - Access existing queue status

## Data Integration

The system currently uses a mock data service (`queueService.js`) that simulates the queue monitoring data structure:

```javascript
{
  "timestamp": "2025-08-13T16:00:00",
  "station_id": "SCC1", 
  "status": "Active",
  "data": {
    "customer_count": 7,
    "average_dwell_time": 162.9
  }
}
```

### To Connect Real Data
1. Replace `queueService.js` with actual API calls to your backend
2. Update the data fetching logic to read from `queue_monitoring.jsonl`
3. Implement WebSocket connections for real-time updates

## Key Components

### CustomerAlert
Displays customer notifications with different states:
- Waiting state: Shows estimated wait time and queue position
- Ready state: Animated alert when customer's turn is ready

### QRCodeDisplay  
Shows static QR code with queue token for easy access to status updates.

### QueueDisplay
Main display showing all station statuses with color-coded indicators:
- Green: Low queue (< 3 customers)  
- Yellow: Medium queue (3-5 customers)
- Red: High queue (6+ customers, virtual queue available)

## Configuration

### Queue Threshold
The virtual queue threshold is set to 6+ customers. This can be modified in:
- `QueueDisplay.js` - Visual indicators
- `queueService.js` - Virtual queue logic
- `App.js` - Join queue filtering

### Styling
The system uses Tailwind CSS with custom queue-themed colors defined in `tailwind.config.js`:
- `queue-primary`: Blue (#2563eb)
- `queue-secondary`: Amber (#f59e0b) 
- `queue-success`: Green (#10b981)
- `queue-danger`: Red (#ef4444)

## Future Enhancements

1. **Real Data Integration**: Connect to actual queue monitoring system
2. **Push Notifications**: Browser notifications for ready alerts
3. **Mobile App**: Native mobile app integration
4. **Analytics**: Queue performance metrics and reporting
5. **Dynamic QR Codes**: QR codes that update with queue status
6. **Multi-language**: Support for multiple languages