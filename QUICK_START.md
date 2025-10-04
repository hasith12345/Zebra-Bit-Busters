# 🚀 Project Sentinel - Quick Launch Guide

## Option 1: Complete System Launcher (Recommended)

```bash
cd "d:\Application files - Do not delete\github\Zebra-Bit-Busters\submission-structure\Bit-Busters\src"
python run_complete_system.py
```

This will automatically start:
- 🌊 Streaming server on port 8765
- 🐍 Python backend + API server on port 3001
- ⚛️ React dashboard on port 3000

## Option 2: Manual Step-by-Step Launch

### Step 1: Start Streaming Server
```bash
cd "d:\Application files - Do not delete\github\Zebra-Bit-Busters\data\streaming-server"
python stream_server.py --port 8765 --speed 10 --loop
```

### Step 2: Start Python Backend (New Terminal)
```bash
cd "d:\Application files - Do not delete\github\Zebra-Bit-Busters\submission-structure\Bit-Busters\src"
python main.py
```

### Step 3: Start React Dashboard (New Terminal)
```bash
cd "d:\Application files - Do not delete\github\Zebra-Bit-Busters\submission-structure\Bit-Busters\react-dashboard"
& "C:\Program Files\nodejs\npm.cmd" start
```

## 🌐 Access URLs

- **React Dashboard**: http://localhost:3000 (Main Interface)
- **API Status**: http://localhost:3001/api/status
- **Live Events**: http://localhost:3001/api/events
- **Dashboard Data**: http://localhost:3001/api/dashboard

## 🔧 Troubleshooting

If ports are occupied:
```bash
cd "d:\Application files - Do not delete\github\Zebra-Bit-Busters"
python troubleshoot.py
```

## 📊 System Features

- **Real-time sync** between Python backend and React frontend
- **Live connection status** indicators
- **9 detection algorithms** for retail monitoring
- **5 sensor types**: RFID, POS, Queue, Product Recognition, Inventory
- **Automatic error handling** for Windows connection issues