"""
Virtual Queue Backend Service
Reads queue monitoring data and provides API endpoints for the React display
"""

import json
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

class VirtualQueueService:
    def __init__(self, data_file_path):
        self.data_file_path = Path(data_file_path)
        self.current_queue_data = {}
        self.virtual_tokens = {}
        self.load_queue_data()
    
    def load_queue_data(self):
        """Load and parse queue monitoring data"""
        try:
            with open(self.data_file_path, 'r') as file:
                lines = file.readlines()
                
            # Get the latest data for each station
            latest_data = {}
            for line in lines:
                if line.strip():
                    data = json.loads(line.strip())
                    station_id = data['station_id']
                    timestamp = datetime.fromisoformat(data['timestamp'])
                    
                    # Keep only the most recent entry for each station
                    if station_id not in latest_data or timestamp > latest_data[station_id]['timestamp']:
                        latest_data[station_id] = {
                            'station_id': station_id,
                            'status': data['status'],
                            'customer_count': data['data']['customer_count'],
                            'average_dwell_time': data['data']['average_dwell_time'],
                            'timestamp': timestamp
                        }
            
            self.current_queue_data = latest_data
            print(f"Loaded data for {len(latest_data)} stations")
            
        except Exception as e:
            print(f"Error loading queue data: {e}")
            # Use mock data as fallback
            self.use_mock_data()
    
    def use_mock_data(self):
        """Use mock data when real data is unavailable"""
        mock_stations = ['SCC1', 'SCC2', 'SCC3', 'SCC4', 'RC1']
        current_time = datetime.now()
        
        for i, station_id in enumerate(mock_stations):
            self.current_queue_data[station_id] = {
                'station_id': station_id,
                'status': 'Active',
                'customer_count': [7, 3, 6, 2, 1][i],  # Sample counts
                'average_dwell_time': [162.9, 45.2, 76.2, 32.1, 15.5][i],
                'timestamp': current_time
            }
    
    def get_stations_data(self):
        """Get all station data formatted for frontend"""
        return [
            {
                'id': data['station_id'],
                'status': data['status'],
                'customerCount': data['customer_count'],
                'averageDwellTime': data['average_dwell_time']
            }
            for data in self.current_queue_data.values()
        ]
    
    def get_total_customers(self):
        """Get total customers across all stations"""
        return sum(data['customer_count'] for data in self.current_queue_data.values())
    
    def get_stations_needing_virtual_queue(self):
        """Get stations with 6+ customers"""
        return [
            data['station_id'] 
            for data in self.current_queue_data.values() 
            if data['customer_count'] >= 6
        ]
    
    def generate_virtual_token(self, station_id):
        """Generate a virtual queue token"""
        if station_id not in self.current_queue_data:
            return None
            
        token = f"VQ-{station_id}-{int(time.time())}"
        station_data = self.current_queue_data[station_id]
        
        self.virtual_tokens[token] = {
            'station_id': station_id,
            'position': station_data['customer_count'],
            'created_at': datetime.now(),
            'estimated_wait': self.calculate_wait_time(station_id, station_data['customer_count'])
        }
        
        return token
    
    def calculate_wait_time(self, station_id, position):
        """Calculate estimated wait time in minutes"""
        if station_id not in self.current_queue_data:
            return 0
            
        avg_dwell_time = self.current_queue_data[station_id]['average_dwell_time']
        return max(1, int((avg_dwell_time * position) / 60))
    
    def check_queue_status(self, token):
        """Check status for a virtual queue token"""
        if token not in self.virtual_tokens:
            return None
            
        token_data = self.virtual_tokens[token]
        station_id = token_data['station_id']
        
        if station_id not in self.current_queue_data:
            return None
        
        current_station = self.current_queue_data[station_id]
        time_elapsed = (datetime.now() - token_data['created_at']).total_seconds()
        
        # Simulate queue progression - customer is ready if enough time passed or queue shortened
        is_ready = time_elapsed > 60 or current_station['customer_count'] < 3
        
        return {
            'token': token,
            'stationId': station_id,
            'isReady': is_ready,
            'estimatedTime': 0 if is_ready else max(1, token_data['estimated_wait'] - int(time_elapsed / 60)),
            'queuePosition': 0 if is_ready else max(1, current_station['customer_count'] - 1),
            'totalInQueue': self.get_total_customers()
        }

# Initialize service with path to queue monitoring data
queue_service = VirtualQueueService('../../../data/input/queue_monitoring.jsonl')

@app.route('/api/stations', methods=['GET'])
def get_stations():
    """Get all station data"""
    return jsonify({
        'stations': queue_service.get_stations_data(),
        'totalCustomers': queue_service.get_total_customers(),
        'virtualQueueStations': queue_service.get_stations_needing_virtual_queue()
    })

@app.route('/api/virtual-queue/join', methods=['POST'])
def join_virtual_queue():
    """Join virtual queue for a station"""
    data = request.get_json()
    station_id = data.get('station_id')
    
    if not station_id:
        return jsonify({'error': 'Station ID required'}), 400
    
    token = queue_service.generate_virtual_token(station_id)
    
    if not token:
        return jsonify({'error': 'Invalid station ID'}), 400
    
    return jsonify({'token': token})

@app.route('/api/virtual-queue/status/<token>', methods=['GET'])
def check_queue_status(token):
    """Check status of virtual queue token"""
    status = queue_service.check_queue_status(token)
    
    if not status:
        return jsonify({'error': 'Invalid token'}), 404
    
    return jsonify(status)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'stations_count': len(queue_service.current_queue_data)
    })

if __name__ == '__main__':
    print("Starting Virtual Queue Backend Service...")
    print(f"Queue data file: {queue_service.data_file_path}")
    print(f"Loaded {len(queue_service.current_queue_data)} stations")
    
    app.run(debug=True, host='0.0.0.0', port=5001)