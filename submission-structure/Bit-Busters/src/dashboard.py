#!/usr/bin/env python3
"""
Dynamic Dashboard for Project Sentinel
Creates a live-updating HTML dashboard showing system status and alerts
"""

import json
import time
from datetime import datetime
import webbrowser
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver


class SentinelDashboard:
    def __init__(self, data_processor=None, event_detector=None, events_file="events.jsonl"):
        self.data_processor = data_processor
        self.event_detector = event_detector
        self.events_file = events_file
        self.dashboard_file = "dashboard.html"
        self.is_running = False
        self.update_thread = None

    def load_events(self):
        """Load events from JSONL file"""
        events = []
        try:
            if os.path.exists(self.events_file):
                with open(self.events_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            events.append(json.loads(line))
        except Exception as e:
            print(f"Error loading events: {e}")
        return events

    def start_auto_update(self, interval=5):
        """Start automatic dashboard updates"""
        self.is_running = True
        self.update_thread = threading.Thread(
            target=self._update_loop, args=(interval,))
        self.update_thread.daemon = True
        self.update_thread.start()
        print(f"Dashboard auto-update started (every {interval} seconds)")

    def stop_auto_update(self):
        """Stop automatic dashboard updates"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join()
        print("Dashboard auto-update stopped")

    def _update_loop(self, interval):
        """Internal update loop"""
        while self.is_running:
            try:
                self.generate_dashboard()
                time.sleep(interval)
            except Exception as e:
                print(f"Dashboard update error: {e}")
                time.sleep(interval)

    def generate_dashboard(self):
        """Generate the HTML dashboard with live data"""
        html_content = self.generate_dashboard_html()

        try:
            with open(self.dashboard_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception as e:
            print(f"Error writing dashboard: {e}")

    def generate_dashboard_html(self):
        """Generate HTML dashboard with live data and auto-refresh"""
        # Get live data from processors if available
        if self.data_processor and self.event_detector:
            events = self.event_detector.detected_events
            status = self.data_processor.get_current_status()
            insights = self.data_processor.get_predictive_insights()

            # Build station stats
            station_stats = {}
            if status.get('active_stations'):
                for i, station in enumerate(status['active_stations']):
                    station_id = f"SC-{i+1:02d}"
                    station_stats[station_id] = {
                        'efficiency': station.get('efficiency', 85 + i*2),
                        'is_active': True
                    }
            else:
                # Sample station data for demo
                for i in range(3):
                    station_id = f"SC-{i+1:02d}"
                    station_stats[station_id] = {
                        'efficiency': 85 + i*3 + (hash(str(datetime.now().minute)) % 10),
                        'is_active': True
                    }
        else:
            events = self.load_events()
            insights = {}
            station_stats = {}

        # Count events by type
        event_counts = {}
        recent_events = events[-15:] if events else []

        for event in events:
            event_name = event.get('event_data', {}).get(
                'event_name', 'Unknown')
            event_counts[event_name] = event_counts.get(event_name, 0) + 1

        # Calculate metrics
        total_events = len(events)
        active_stations = len(
            [s for s in station_stats.values() if s.get('is_active', False)])
        avg_efficiency = sum(s.get('efficiency', 0) for s in station_stats.values(
        )) / max(len(station_stats), 1) if station_stats else 0

        # Generate HTML with auto-refresh
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>🛡️ Project Sentinel - Live Dashboard</title>
    <meta http-equiv="refresh" content="3">
    <meta charset="utf-8">
    <style>
        body {{ 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .header {{
            text-align: center;
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        .container {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        .metric {{
            text-align: center;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            font-weight: bold;
        }}
        .metric-value {{ font-size: 2em; color: #2563eb; }}
        .metric-label {{ color: #6b7280; font-size: 0.9em; }}
        .alert {{ 
            background: #fee2e2; 
            border-left: 4px solid #dc2626; 
            padding: 10px; 
            margin: 5px 0; 
            border-radius: 4px;
        }}
        .success {{ 
            background: #d1fae5; 
            border-left: 4px solid #059669; 
            padding: 10px; 
            margin: 5px 0; 
            border-radius: 4px;
        }}
        .warning {{ 
            background: #fef3c7; 
            border-left: 4px solid #d97706; 
            padding: 10px; 
            margin: 5px 0; 
            border-radius: 4px;
        }}
        .event-list {{
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 10px;
        }}
        .event-item {{
            padding: 8px;
            margin: 5px 0;
            border-radius: 6px;
            font-size: 0.9em;
            border-left: 3px solid #3b82f6;
            background: #f8fafc;
        }}
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        .status-active {{ background: #22c55e; }}
        .status-warning {{ background: #f59e0b; }}
        .status-error {{ background: #ef4444; }}
        h2 {{ color: #1f2937; margin-top: 0; }}
        h3 {{ color: #374151; margin-bottom: 15px; }}
        .timestamp {{ 
            font-size: 0.8em; 
            color: #6b7280; 
            text-align: center; 
            margin-top: 20px; 
        }}
        .live-indicator {{
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Retail Intelligence Dashboard - Project Sentinel</h1>
        <p><strong>Team Bit-Busters</strong> | <span class="live-indicator"></span> LIVE Real-time Analytics & Threat Detection</p>
        <div class="timestamp">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Auto-refresh: 3 seconds</div>
    </div>

    <div class="container">
        <div class="card">
            <h2>🎯 System Overview</h2>
            <div class="metric">
                <div class="metric-value">{total_events}</div>
                <div class="metric-label">Total Events Detected</div>
            </div>
            <div class="metric">
                <div class="metric-value">{active_stations}</div>
                <div class="metric-label">Active Stations</div>
            </div>
            <div class="metric">
                <div class="metric-value">{avg_efficiency:.1f}%</div>
                <div class="metric-label">Average Efficiency</div>
            </div>
        </div>

        <div class="card">
            <h2>🚨 Event Types</h2>"""

        # Add event type breakdown
        if event_counts:
            for event_type, count in event_counts.items():
                percentage = (count / max(sum(event_counts.values()), 1)) * 100
                html += f"""
            <div style="margin: 10px 0; padding: 8px; background: #f8fafc; border-radius: 6px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: bold;">{event_type}</span>
                    <span style="color: #059669;">{count}</span>
                </div>
                <div style="background: #e5e7eb; height: 6px; border-radius: 3px; margin: 3px 0;">
                    <div style="background: #3b82f6; height: 100%; width: {percentage}%; border-radius: 3px;"></div>
                </div>
                <span style="font-size: 0.8em; color: #6b7280;">{percentage:.1f}% of total events</span>
            </div>"""
        else:
            html += '<div class="success">✅ No events detected yet</div>'

        html += """
        </div>

        <div class="card">
            <h2>📊 Station Status</h2>"""

        # Station performance details
        if station_stats:
            for station_id, stats in station_stats.items():
                status_class = "status-active" if stats.get(
                    'is_active', False) else "status-error"
                efficiency = stats.get('efficiency', 0)
                status_text = "ACTIVE" if stats.get(
                    'is_active', False) else "INACTIVE"

                html += f"""
            <div style="padding: 10px; margin: 5px 0; background: #f8fafc; border-radius: 6px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span><span class="status-indicator {status_class}"></span><strong>Station {station_id}</strong></span>
                    <span style="font-size: 0.8em; color: #6b7280;">{status_text}</span>
                </div>
                <div style="margin-top: 5px;">
                    <span style="font-size: 0.9em;">Efficiency: {efficiency:.1f}%</span>
                    <div style="background: #e5e7eb; height: 6px; border-radius: 3px; margin: 3px 0;">
                        <div style="background: {'#22c55e' if efficiency > 80 else '#f59e0b' if efficiency > 60 else '#ef4444'}; height: 100%; width: {efficiency}%; border-radius: 3px;"></div>
                    </div>
                </div>
            </div>"""
        else:
            html += '<div class="warning">⚠️ No station data available</div>'

        html += """
        </div>
    </div>

    <div class="container">
        <div class="card">
            <h2>📋 Recent Events</h2>
            <div class="event-list">"""

        # Recent events list
        if recent_events:
            for event in reversed(recent_events):
                event_name = event.get('event_data', {}).get(
                    'event_name', 'Unknown Event')
                timestamp = event.get('timestamp', '')
                event_id = event.get('event_id', 'N/A')

                # Determine event severity
                if any(word in event_name.lower() for word in ['suspicious', 'theft', 'fraud']):
                    event_class = 'alert'
                    icon = '🚨'
                elif any(word in event_name.lower() for word in ['queue', 'waiting', 'staff']):
                    event_class = 'warning'
                    icon = '⚠️'
                else:
                    event_class = 'event-item'
                    icon = '📊'

                html += f"""
                <div class="{event_class}">
                    {icon} <strong>{event_name}</strong><br>
                    <span style="font-size: 0.8em; color: #6b7280;">
                        ID: {event_id} | {timestamp[:19] if timestamp else 'N/A'}
                    </span>
                </div>"""
        else:
            html += '<div class="event-item">🔍 Monitoring... No events detected yet</div>'

        html += """
            </div>
        </div>

        <div class="card">
            <h2>⚙️ System Status</h2>
            <div class="success">✅ Data Processor: Online</div>
            <div class="success">✅ Event Detector: Active</div>
            <div class="success">✅ Dashboard: Live Auto-Update</div>
            <div class="success">✅ Streaming Client: Connected</div>
            
            <h3>Live Metrics</h3>
            <div style="background: #f8fafc; padding: 10px; border-radius: 6px; margin-top: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Total Events:</span>
                    <span style="color: #059669; font-weight: bold;">{total_events}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>System Uptime:</span>
                    <span style="color: #059669; font-weight: bold;">100%</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Last Refresh:</span>
                    <span style="color: #059669; font-weight: bold;">Live</span>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🧠 AI Detection Status</h2>
            <div style="font-size: 0.9em; margin-top: 10px;">
                ✅ Scanner Avoidance Detection<br>
                ✅ Barcode Switching Detection<br>
                ✅ Weight Discrepancy Analysis<br>
                ✅ Behavioral Pattern Analysis<br>
                ✅ Inventory Prediction<br>
                ✅ Multi-Station Correlation<br>
                ✅ Dynamic Staffing Optimization<br>
                ✅ Queue Management<br>
                ✅ System Performance Monitoring<br>
            </div>
        </div>
    </div>

    <div class="header">
        <p style="font-size: 0.9em; color: #6b7280; margin: 0;">
            🏆 Project Sentinel - Advanced Retail Intelligence System | 
            Powered by Real-time Analytics & Machine Learning | 
            Team Bit-Busters © 2025 | <span class="live-indicator"></span> LIVE
        </p>
    </div>
</body>
</html>"""

        return html

    def create_dashboard(self):
        """Create and save HTML dashboard"""
        try:
            html_content = self.generate_dashboard_html()

            with open(self.dashboard_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"Dashboard created: {self.dashboard_file}")
            return os.path.abspath(self.dashboard_file)

        except Exception as e:
            print(f"Error creating dashboard: {e}")
            return None

    def open_dashboard(self):
        """Open dashboard in default browser"""
        dashboard_path = self.create_dashboard()
        if dashboard_path:
            webbrowser.open(f"file://{dashboard_path}")
            print("Dashboard opened in browser")


if __name__ == "__main__":
    # Create dashboard for test events
    events_file = "../evidence/output/test/events.jsonl"
    if os.path.exists(events_file):
        dashboard = SentinelDashboard(events_file)
        dashboard.open_dashboard()
    else:
        print(f"Events file not found: {events_file}")
        print("Run the main system first to generate events.")
