# Virtual Queue System Demo

This demo shows how the Virtual Queue System works with the Zebra queue monitoring data.

## 🎯 System Overview

The Virtual Queue System consists of two main components:

1. **React Frontend** (`src/`) - Customer-facing display interface
2. **Python Backend** (`queue_backend.py`) - API server that reads queue data

## 📊 Key Features Implemented

### ✅ Queue Monitoring Integration
- Reads real data from `queue_monitoring.jsonl`
- Displays live queue status for all stations (SCC1, SCC2, SCC3, SCC4, RC1)
- Shows customer count and average dwell time per station

### ✅ Virtual Queue System
- **Threshold**: Automatically offers virtual queue when stations have 6+ customers
- **Token Generation**: Creates unique tokens like `VQ-SCC1-ABC123`
- **Static QR Codes**: Non-changing QR codes that link to queue status pages

### ✅ Customer Alert System
- **Waiting State**: Shows estimated wait time and queue position
- **Ready State**: Animated notification when customer's turn is ready
- **Total Queue Count**: Displays total customers across all stations (as requested)

### ✅ Removed Elements (as requested)
- ❌ Max wait time indicator removed
- ❌ "Stations Need Virtual Queue" section removed
- ✅ Focus on total queue count only

## 🚀 Quick Start

### Option 1: Automatic Setup
```bash
cd virtual-queue-display
./start.sh
```

### Option 2: Manual Setup
```bash
# Terminal 1 - Start Backend
cd virtual-queue-display
pip3 install -r requirements.txt
python3 queue_backend.py

# Terminal 2 - Start Frontend  
cd virtual-queue-display
npm install
npm start
```

## 🔗 Access URLs

- **Main Queue Display**: http://localhost:3000
- **Join Virtual Queue**: http://localhost:3000?station=SCC1
- **Check Queue Status**: http://localhost:3000?token=VQ-SCC1-ABC123
- **API Health Check**: http://localhost:5001/api/health

## 📱 Usage Scenarios

### Scenario 1: Store Display
- Open http://localhost:3000 on store displays
- Shows real-time queue status for all stations
- Customers can see total customers in queue
- Virtual queue options appear when stations have 6+ customers

### Scenario 2: Customer Gets QR Code
- Customer scans QR code or enters URL manually
- Gets redirected to: http://localhost:3000?station=SCC1
- System generates virtual queue token automatically
- Customer sees personalized alert screen

### Scenario 3: Customer Alert Display
- Customer accesses: http://localhost:3000?token=VQ-SCC1-ABC123
- Sees waiting state with estimated time
- Gets animated ready notification when turn is ready

## 🎨 QR Code Solution

### Static QR Code Approach
The system uses **static QR codes** that don't change dynamically:

1. **Station QR Codes**: Point to `?station=SCC1` URLs
2. **Token QR Codes**: Point to `?token=ABC123` URLs  
3. **Generic QR Code**: Points to main display page

**Benefits:**
- ✅ Easy to print and place at stations
- ✅ No need to update QR codes when queues change
- ✅ Works offline - customers can bookmark URLs
- ✅ Simple to implement and maintain

### QR Code Placement Strategy
```
Station SCC1 QR Code → http://localhost:3000?station=SCC1
Station SCC2 QR Code → http://localhost:3000?station=SCC2
Station SCC3 QR Code → http://localhost:3000?station=SCC3
```

## 📊 Data Integration

### Real Queue Data
- Reads from: `../../../data/input/queue_monitoring.jsonl`
- Parses JSON lines with station data
- Updates display every 2 seconds

### API Endpoints
```
GET  /api/stations                      - All station data
POST /api/virtual-queue/join           - Join virtual queue
GET  /api/virtual-queue/status/<token> - Check queue status
GET  /api/health                       - System health
```

## 🎯 System Behavior

### Queue Threshold Logic
- **Green** (0-2 customers): Normal operation
- **Yellow** (3-5 customers): Moderate queue
- **Red** (6+ customers): Virtual queue available

### Customer Flow
1. Customer arrives → Sees queue length
2. If 6+ customers → Option to join virtual queue
3. Gets QR code/token → Can leave station area  
4. Monitors status → Gets notified when ready
5. Returns to station → Completes transaction

## 📈 Future Enhancements

While this demo uses mock progression, the system is designed for:
- Real-time WebSocket connections
- Push notifications
- Mobile app integration
- Analytics and reporting
- Multi-language support

---

**Note**: This system demonstrates the core functionality with the Zebra queue monitoring data. In production, you would integrate with your actual POS/queue management systems for real-time updates.