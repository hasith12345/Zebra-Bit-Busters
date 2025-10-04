# 🛡️ PROJECT SENTINEL - Complete Setup Guide

## Project Overview

**Project Sentinel** is an advanced **Real-time Retail Intelligence System** that monitors supermarket operations and detects security/efficiency issues automatically. This is a comprehensive competition project developed by Team "Bit-Busters".

### 🎯 What It Does

- **Real-time Data Processing**: Handles 5 sensor types (RFID, POS, Queue, Product Recognition, Inventory)
- **Smart Event Detection**: 9 advanced algorithms detect theft, operational issues, and anomalies
- **Live Dashboard**: Beautiful web interface with real-time monitoring
- **Automated Alerts**: Generates actionable events in JSON format

### 🏗️ System Architecture

```
Sensor Data → Streaming Server → Data Processor → Event Detector → Dashboard
                                       ↓
                                 Events.jsonl (Output)
```

## 🚀 Quick Start (Automated)

### Option 1: 🔗 Synchronized Real-Time System (RECOMMENDED)

```bash
cd "d:\Application files - Do not delete\github\Zebra-Bit-Busters"
python launch_synchronized_system.py
```

**OR double-click: `START_PROJECT_SENTINEL.bat`**

**✨ Features:**

- ✅ **Real-time synchronization** between Python backend and React dashboard
- ✅ **Live API endpoints** (localhost:3001/api/dashboard)
- ✅ **React dashboard shows actual live data** (not dummy data)
- ✅ **Event detection reflects immediately** in both dashboards

### Judge Demo Script

```bash
cd "submission-structure\Bit-Busters\evidence\executables"
python run_demo.py
```

## 🛠️ Manual Setup

### Step 1: Start Data Streaming Server

```bash
cd "data\streaming-server"
python stream_server.py --port 8765 --speed 10 --loop
```

### Step 2: Run Main System (New Terminal)

```bash
cd "submission-structure\Bit-Busters\src"
python main.py
```

### Step 3: View Dashboard

- Open: `submission-structure\Bit-Busters\src\dashboard.html` in your browser
- Auto-refreshes every 3 seconds with live data

## 📁 Project Structure

```
Zebra-Bit-Busters/
├── setup_and_run.py              # 🆕 Complete automation script
├── getting-started.md             # Project overview
├── project-sentinel.pdf           # Detailed specifications
├── data/                          # Development data (streaming simulation)
│   ├── input/                     # Sample sensor data
│   ├── streaming-server/          # Data streaming simulator
│   └── streaming-clients/         # Sample clients (Python, Node.js, Java)
├── submission-structure/
│   └── Bit-Busters/              # Main project submission
│       ├── src/                   # Complete source code
│       │   ├── main.py           # Main application
│       │   ├── data_processor.py # Real-time data handler
│       │   ├── event_detector.py # 9 detection algorithms
│       │   └── dashboard.py      # Web dashboard generator
│       ├── react-dashboard/       # Modern React dashboard
│       └── evidence/
│           ├── executables/
│           │   └── run_demo.py   # Automated demo for judges
│           └── output/
│               └── test/events.jsonl  # Generated events
└── resources/                     # Documentation and terminology
```

## 🧠 Detection Algorithms

The system implements 9 advanced algorithms:

1. **Scanner Avoidance Detection** - Compares RFID vs POS data
2. **Barcode Switching Detection** - Identifies price manipulation
3. **Weight Discrepancy Analysis** - Self-checkout validation
4. **System Crash Detection** - Monitors station failures
5. **Queue Management** - Customer experience optimization
6. **Behavioral Pattern Analysis** - Suspicious customer behavior
7. **Inventory Discrepancy Prediction** - Predictive analytics
8. **Multi-Station Correlation** - Coordinated theft detection
9. **Dynamic Staffing Optimization** - Real-time recommendations

## 📊 Dashboard Features

### HTML Dashboard (`dashboard.html`)

- **Real-time Monitoring**: Live sensor data display
- **Event Alerts**: Visual notifications for detected incidents
- **Station Status**: Individual checkout station monitoring
- **Analytics**: Customer flow, revenue trends, system health
- **Auto-refresh**: Updates every 3 seconds

### React Dashboard (Modern Interface)

**🚀 Now Available - Automatic Launch!**

```bash
# Automatically started with complete system launcher
python launch_complete_system.py
```

**Manual Setup:**

```bash
cd "submission-structure\Bit-Busters\react-dashboard"
npm install
npm start
```

- **🌐 URL**: http://localhost:3000
- **✨ Features**: Modern UI, interactive charts, real-time updates
- **🎨 Design**: Professional interface with Tailwind CSS
- **📱 Responsive**: Mobile-friendly design

## 🎮 How to Use

### 1. **For Judges/Quick Demo**

```bash
python setup_and_run.py
```

- Automatically starts everything
- Opens dashboard in browser
- Runs for 2 minutes
- Shows detected events summary

### 2. **For Development**

1. Start streaming server (Terminal 1)
2. Run main system (Terminal 2)
3. Open dashboard.html in browser
4. Monitor real-time events

### 3. **For Competition Testing**

- Use automated `run_demo.py` script
- Generates `events.jsonl` output
- Perfect for judge evaluation

## 📈 Expected Output

### Console Output:

```
PROJECT SENTINEL - RETAIL MONITORING SYSTEM
Starting system components...
Data processor started
Event detector ready
Dashboard available at: dashboard.html

ALERT: 3 new event(s) detected!
   * Scanner Avoidance at SCC1
   * System Crash at SCC1
   * Inventory Discrepancy at Unknown

Status: RFID:1 | POS:1 | Queue:1 | Recognition:0 | Alerts:23
```

### Generated Files:

- `events.jsonl` - All detected events in JSON format
- `dashboard.html` - Live monitoring interface
- Results in `evidence/output/test/` directory

## 🔧 Technical Details

### Requirements:

- **Python 3.7+**
- **Standard Library Only** (no external dependencies)
- **Windows/macOS/Linux** compatible

### Performance:

- **Real-time Processing**: 100+ sensor readings per minute
- **Event Detection**: ~35 events in 2 minutes
- **System Uptime**: 100% during monitoring

### Data Flow:

1. Streaming server simulates 5 sensor types
2. Data processor connects via TCP socket
3. Event detector analyzes patterns
4. Dashboard displays real-time results
5. Events saved to JSONL format

## 🏆 Competitive Advantages

1. **Advanced Algorithms**: Beyond basic detection, includes ML-style features
2. **Real-time Performance**: Handles continuous data streams efficiently
3. **Professional UI**: Enterprise-grade dashboard interface
4. **Complete Solution**: End-to-end system ready for deployment
5. **Scalable Architecture**: Production-ready design
6. **Innovation**: Behavioral analysis and predictive capabilities

## 🚨 Troubleshooting

### Common Issues:

**"Streaming server not running"**

```bash
cd "data\streaming-server"
python stream_server.py --port 8765 --speed 10 --loop
```

**"Dashboard not updating"**

- Refresh browser (F5)
- Check if main.py is running
- Verify streaming server is active

**"No events detected"**

- Ensure data is streaming (check console output)
- Wait 10-20 seconds for detection cycle
- Verify algorithms are running

## 📚 Additional Resources

- `project-sentinel.pdf` - Complete project specifications
- `data/README.md` - Data format documentation
- `resources/documents/` - Terminology and context
- `submission-structure/Bit-Busters/README.md` - Detailed submission guide

## 👥 Team Information

- **Team Name**: Bit-Busters
- **Project**: Advanced Retail Intelligence System
- **Focus**: Real-time security and operational efficiency
- **Approach**: Professional-grade solution with innovative features

---

## 🎯 Quick Commands Summary

```bash
# 🚀 Complete synchronized system
python launch_synchronized_system.py
# OR double-click: START_PROJECT_SENTINEL.bat

# 🎯 Judge demo
cd "submission-structure\Bit-Busters\evidence\executables"
python run_demo.py

# ⚛️ React dashboard only
cd "submission-structure\Bit-Busters\react-dashboard"
npm install && npm start

# 🔧 Manual start
cd "data\streaming-server"
python stream_server.py --port 8765 --speed 10 --loop

# 🛡️ Run system (new terminal)
cd "submission-structure\Bit-Busters\src"
python main.py
```

**🎉 Project Sentinel is now ready to monitor and protect your retail environment!**
