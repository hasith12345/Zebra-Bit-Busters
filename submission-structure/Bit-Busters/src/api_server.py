#!/usr/bin/env python3
"""
API Server for Project Sentinel
Provides REST API endpoints for React dashboard to get real-time data
"""

import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socketserver
from datetime import datetime


class SentinelAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Enable CORS for React development server
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        try:
            if path == '/api/status':
                self.handle_status()
            elif path == '/api/events':
                self.handle_events()
            elif path == '/api/dashboard':
                self.handle_dashboard_data()
            elif path == '/api/stations':
                self.handle_stations()
            else:
                self.send_error_response(404, "Endpoint not found")
        except Exception as e:
            self.send_error_response(500, str(e))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def handle_status(self):
        """Return system status"""
        if hasattr(self.server, 'data_processor') and hasattr(self.server, 'event_detector'):
            status = self.server.data_processor.get_current_status()
            total_events = len(self.server.event_detector.detected_events)

            response = {
                'status': 'running',
                'timestamp': datetime.now().isoformat(),
                'rfid_events': status.get('rfid_events', 0),
                'pos_events': status.get('pos_events', 0),
                'queue_events': status.get('queue_events', 0),
                'recognition_events': status.get('recognition_events', 0),
                'total_alerts': total_events,
                'is_connected': True
            }
        else:
            response = {
                'status': 'disconnected',
                'timestamp': datetime.now().isoformat(),
                'is_connected': False
            }

        self.wfile.write(json.dumps(response).encode())

    def handle_events(self):
        """Return recent events"""
        if hasattr(self.server, 'event_detector'):
            events = self.server.event_detector.detected_events
            recent_events = events[-20:] if len(events) > 20 else events

            # Convert to API format
            formatted_events = []
            for i, event in enumerate(reversed(recent_events)):
                formatted_events.append({
                    'id': f'E{len(events) - i:03d}',
                    'type': event['event_data']['event_name'],
                    'timestamp': event.get('timestamp', datetime.now().isoformat()),
                    'station_id': event['event_data'].get('station_id', 'Unknown'),
                    'severity': event['event_data'].get('severity', 'medium'),
                    'details': event['event_data'].get('details', '')
                })

            response = {
                'events': formatted_events,
                'total_count': len(events),
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {
                'events': [],
                'total_count': 0,
                'timestamp': datetime.now().isoformat()
            }

        self.wfile.write(json.dumps(response).encode())

    def handle_dashboard_data(self):
        """Return complete dashboard data"""
        if hasattr(self.server, 'data_processor') and hasattr(self.server, 'event_detector'):
            # Get real data from the system
            status = self.server.data_processor.get_current_status()
            events = self.server.event_detector.detected_events

            # Calculate event type distribution
            event_types = {}
            for event in events:
                event_name = event['event_data']['event_name']
                event_types[event_name] = event_types.get(event_name, 0) + 1

            # Format event types for frontend
            total_events = len(events)
            formatted_event_types = []
            for event_type, count in event_types.items():
                percentage = (count / total_events *
                              100) if total_events > 0 else 0
                formatted_event_types.append({
                    'name': event_type,
                    'count': count,
                    'percentage': round(percentage, 1)
                })

            # Station data (based on real data)
            stations = [
                {
                    'id': 'SCC1',
                    'efficiency': 95.0 + (status.get('pos_events', 0) * 0.5),
                    'isActive': status.get('pos_events', 0) > 0
                },
                {
                    'id': 'SC-02',
                    'efficiency': 92.0 + (status.get('rfid_events', 0) * 0.3),
                    'isActive': status.get('rfid_events', 0) > 0
                },
                {
                    'id': 'SC-03',
                    'efficiency': 98.0 + (status.get('queue_events', 0) * 0.2),
                    'isActive': status.get('queue_events', 0) > 0
                }
            ]

            # Recent events
            recent_events = events[-10:] if len(events) > 10 else events
            formatted_recent_events = []
            for i, event in enumerate(reversed(recent_events)):
                formatted_recent_events.append({
                    'id': f'E{len(events) - i:03d}',
                    'type': event['event_data']['event_name'],
                    'timestamp': event.get('timestamp', datetime.now().isoformat()),
                    'station_id': event['event_data'].get('station_id', 'Unknown')
                })

            # Calculate active stations
            active_stations = sum(
                1 for station in stations if station['isActive'])
            avg_efficiency = sum(station['efficiency']
                                 for station in stations) / len(stations)

            response = {
                'totalEvents': total_events,
                'activeStations': active_stations,
                'averageEfficiency': round(avg_efficiency, 1),
                'eventTypes': formatted_event_types,
                'stations': stations,
                'recentEvents': formatted_recent_events,
                'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'systemStatus': {
                    'rfid_events': status.get('rfid_events', 0),
                    'pos_events': status.get('pos_events', 0),
                    'queue_events': status.get('queue_events', 0),
                    'recognition_events': status.get('recognition_events', 0)
                }
            }
        else:
            # Fallback dummy data when system not connected
            response = {
                'totalEvents': 0,
                'activeStations': 0,
                'averageEfficiency': 0,
                'eventTypes': [],
                'stations': [],
                'recentEvents': [],
                'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'systemStatus': {
                    'rfid_events': 0,
                    'pos_events': 0,
                    'queue_events': 0,
                    'recognition_events': 0
                },
                'error': 'System not connected'
            }

        self.wfile.write(json.dumps(response).encode())

    def handle_stations(self):
        """Return station-specific data"""
        if hasattr(self.server, 'data_processor'):
            status = self.server.data_processor.get_current_status()

            stations = [
                {
                    'id': 'SCC1',
                    'name': 'Self-Checkout 1',
                    'status': 'active' if status.get('pos_events', 0) > 0 else 'idle',
                    'efficiency': 95.0,
                    'transactions': status.get('pos_events', 0),
                    'last_activity': datetime.now().isoformat()
                },
                {
                    'id': 'SC-02',
                    'name': 'Station 2',
                    'status': 'active' if status.get('rfid_events', 0) > 0 else 'idle',
                    'efficiency': 92.0,
                    'transactions': status.get('rfid_events', 0),
                    'last_activity': datetime.now().isoformat()
                },
                {
                    'id': 'SC-03',
                    'name': 'Station 3',
                    'status': 'active' if status.get('queue_events', 0) > 0 else 'idle',
                    'efficiency': 98.0,
                    'transactions': status.get('queue_events', 0),
                    'last_activity': datetime.now().isoformat()
                }
            ]

            response = {
                'stations': stations,
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {
                'stations': [],
                'timestamp': datetime.now().isoformat(),
                'error': 'System not connected'
            }

        self.wfile.write(json.dumps(response).encode())

    def send_error_response(self, code, message):
        """Send error response"""
        response = {
            'error': message,
            'timestamp': datetime.now().isoformat()
        }
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        pass


class SentinelAPIServer:
    def __init__(self, port=3001):
        self.port = port
        self.server = None
        self.server_thread = None
        self.data_processor = None
        self.event_detector = None

    def set_system_components(self, data_processor, event_detector):
        """Set references to the main system components"""
        self.data_processor = data_processor
        self.event_detector = event_detector

        if self.server:
            self.server.data_processor = data_processor
            self.server.event_detector = event_detector

    def start_server(self):
        """Start the API server"""
        try:
            self.server = HTTPServer(
                ('localhost', self.port), SentinelAPIHandler)
            self.server.data_processor = self.data_processor
            self.server.event_detector = self.event_detector

            self.server_thread = threading.Thread(
                target=self.server.serve_forever, daemon=True)
            self.server_thread.start()

            print(f"✅ API Server started on http://localhost:{self.port}")
            print(
                f"   • Dashboard data: http://localhost:{self.port}/api/dashboard")
            print(f"   • Events: http://localhost:{self.port}/api/events")
            print(f"   • Status: http://localhost:{self.port}/api/status")
            return True

        except Exception as e:
            print(f"❌ Failed to start API server: {e}")
            return False

    def stop_server(self):
        """Stop the API server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("🛑 API Server stopped")


if __name__ == "__main__":
    # Test the API server standalone
    api_server = SentinelAPIServer(3001)

    try:
        if api_server.start_server():
            print("API Server running... Press Ctrl+C to stop")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        api_server.stop_server()
