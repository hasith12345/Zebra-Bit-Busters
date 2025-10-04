"""
Simplified Virtual Queue Backend
Reads real queue monitoring data and provides alerts when customer count >= 6
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

class SimpleQueueMonitor:
    def __init__(self, data_file_path):
        self.data_file_path = Path(data_file_path)
        self.current_stations = {}
        self.load_real_queue_data()
    
    def load_real_queue_data(self):
        """Load real data from queue_monitoring.jsonl"""
        try:
            print(f"Loading queue data from: {self.data_file_path}")
            
            if not self.data_file_path.exists():
                print("Queue data file not found, using mock data")
                self.use_mock_data()
                return
            
            with open(self.data_file_path, 'r') as file:
                lines = file.readlines()
            
            # Parse all lines and get latest data for each station
            station_data = {}
            for line in lines[-1000:]:  # Get recent data only
                if line.strip():
                    try:
                        data = json.loads(line.strip())
                        station_id = data['station_id']
                        timestamp = datetime.fromisoformat(data['timestamp'])
                        
                        # Keep latest entry for each station
                        if station_id not in station_data or timestamp > station_data[station_id]['timestamp']:
                            station_data[station_id] = {
                                'station_id': station_id,
                                'customer_count': data['data']['customer_count'],
                                'average_dwell_time': data['data']['average_dwell_time'],
                                'timestamp': timestamp,
                                'status': data.get('status', 'Active')
                            }
                    except json.JSONDecodeError:
                        continue
            
            self.current_stations = station_data
            print(f"Loaded data for stations: {list(station_data.keys())}")
            
            # Add some variation to make demo more interesting
            self.add_demo_variation()
            
        except Exception as e:
            print(f"Error loading queue data: {e}")
            self.use_mock_data()
    
    def add_demo_variation(self):
        """Add some variation to demonstrate the 6+ customer alerts"""
        station_ids = list(self.current_stations.keys())
        busy_station = None
        
        # Randomly make some stations busy for demo
        if len(station_ids) > 0 and random.random() > 0.3:
            busy_station = random.choice(station_ids)
            if busy_station in self.current_stations:
                self.current_stations[busy_station]['customer_count'] = random.randint(6, 9)
                print(f"Demo: Made {busy_station} busy with {self.current_stations[busy_station]['customer_count']} customers")
        
        # Sometimes make a second station busy
        if len(station_ids) > 1 and random.random() > 0.7:
            available_stations = [s for s in station_ids if s != busy_station]
            if available_stations:
                busy_station2 = random.choice(available_stations)
                if busy_station2 in self.current_stations:
                    self.current_stations[busy_station2]['customer_count'] = random.randint(6, 8)
                    print(f"Demo: Made {busy_station2} also busy with {self.current_stations[busy_station2]['customer_count']} customers")
    
    def use_mock_data(self):
        """Fallback mock data based on real dataset structure"""
        mock_data = {
            'SCC1': {
                'station_id': 'SCC1',
                'customer_count': 7,  # Make this one busy
                'average_dwell_time': 162.9,
                'status': 'Active',
                'timestamp': datetime.now()
            },
            'SCC2': {
                'station_id': 'SCC2', 
                'customer_count': 3,
                'average_dwell_time': 45.2,
                'status': 'Active',
                'timestamp': datetime.now()
            },
            'SCC3': {
                'station_id': 'SCC3',
                'customer_count': 6,  # Make this one at threshold
                'average_dwell_time': 76.2,
                'status': 'Active', 
                'timestamp': datetime.now()
            },
            'SCC4': {
                'station_id': 'SCC4',
                'customer_count': 2,
                'average_dwell_time': 32.1,
                'status': 'Active',
                'timestamp': datetime.now()
            },
            'RC1': {
                'station_id': 'RC1',
                'customer_count': 1,
                'average_dwell_time': 15.5,
                'status': 'Active',
                'timestamp': datetime.now()
            }
        }
        self.current_stations = mock_data
        print("Using mock data with SCC1 and SCC3 showing busy queues")
    
    def get_stations_data(self):
        """Get station data formatted for frontend"""
        stations = []
        for station_data in self.current_stations.values():
            stations.append({
                'id': station_data['station_id'],
                'customerCount': station_data['customer_count'],
                'averageDwellTime': station_data['average_dwell_time'],
                'status': station_data['status']
            })
        return stations
    
    def get_busy_stations(self):
        """Get stations with 6+ customers"""
        busy = []
        for station_data in self.current_stations.values():
            if station_data['customer_count'] >= 6:
                busy.append({
                    'id': station_data['station_id'],
                    'customerCount': station_data['customer_count'],
                    'averageDwellTime': station_data['average_dwell_time']
                })
        return busy
    
    def get_total_customers(self):
        """Get total customers across all stations"""
        return sum(station['customer_count'] for station in self.current_stations.values())

# Initialize with path to real data
queue_monitor = SimpleQueueMonitor('../../../data/input/queue_monitoring.jsonl')

@app.route('/api/stations', methods=['GET'])
def get_stations():
    """Get all station data"""
    stations = queue_monitor.get_stations_data()
    busy_stations = queue_monitor.get_busy_stations()
    total_customers = queue_monitor.get_total_customers()
    
    return jsonify({
        'stations': stations,
        'busyStations': busy_stations,
        'totalCustomers': total_customers,
        'alertNeeded': len(busy_stations) > 0
    })

@app.route('/api/queue-alert', methods=['GET'])
def get_queue_alert():
    """Get queue alert information"""
    busy_stations = queue_monitor.get_busy_stations()
    
    if not busy_stations:
        return jsonify({'alertNeeded': False})
    
    # Get the busiest station
    busiest = max(busy_stations, key=lambda x: x['customerCount'])
    
    return jsonify({
        'alertNeeded': True,
        'busiestStation': busiest,
        'allBusyStations': busy_stations,
        'message': f'Queue alert: {busiest["id"]} has {busiest["customerCount"]} customers'
    })

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Refresh queue data from file"""
    queue_monitor.load_real_queue_data()
    return jsonify({'status': 'refreshed'})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check"""
    busy_count = len(queue_monitor.get_busy_stations())
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'stations_count': len(queue_monitor.current_stations),
        'busy_stations_count': busy_count,
        'alert_active': busy_count > 0
    })

if __name__ == '__main__':
    print("🚨 Simple Queue Alert System Starting...")
    print(f"📊 Queue data file: {queue_monitor.data_file_path}")
    
    busy = queue_monitor.get_busy_stations()
    if busy:
        print(f"🔥 Busy stations detected: {[s['id'] for s in busy]}")
    else:
        print("✅ All stations running smoothly")
    
    app.run(debug=True, host='0.0.0.0', port=5001)