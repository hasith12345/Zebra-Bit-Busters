#!/usr/bin/env python3
"""
Main Application for Project Sentinel
Integrates data processing, event detection, and dashboard
"""

import time
import json
import sys
import os
from datetime import datetime
from data_processor import DataProcessor
from event_detector import EventDetector
from dashboard import SentinelDashboard
from api_server import SentinelAPIServer


class SentinelSystem:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.event_detector = EventDetector(self.data_processor)
        self.dashboard = SentinelDashboard(
            self.data_processor, self.event_detector)
        self.api_server = SentinelAPIServer(port=3001)
        self.is_running = False

    def start_system(self):
        """Start the complete sentinel system"""
        print("=" * 50)
        print("PROJECT SENTINEL - RETAIL MONITORING SYSTEM")
        print("=" * 50)
        print("Starting system components...")

        # Start data processing
        thread = self.data_processor.start_processing()
        self.is_running = True

        # Wait a moment for data to start flowing
        time.sleep(3)

        print("Data processor started")
        print("Event detector ready")

        # Start API server for React dashboard
        self.api_server.set_system_components(
            self.data_processor, self.event_detector)
        if self.api_server.start_server():
            print("API server started for React dashboard integration")
        else:
            print(
                "Warning: API server failed to start - React dashboard won't have real-time data")

        print("Starting live dashboard...")

        # Start the dashboard auto-update
        self.dashboard.start_auto_update()
        print("Dashboard auto-update started")

        # Create initial dashboard
        dashboard_path = self.dashboard.create_dashboard()
        if dashboard_path:
            print(f"Dashboard available at: {dashboard_path}")

        print("Monitoring for anomalies...")
        print("-" * 50)

        return thread

    def run_monitoring_cycle(self, max_duration_seconds=None):
        """Run monitoring until data stream ends or max duration reached"""
        start_time = time.time()
        last_status_time = 0
        data_stream_active = True

        try:
            while self.is_running and data_stream_active:
                current_time = time.time()

                # Check if max duration exceeded (if specified)
                if max_duration_seconds and (current_time - start_time) > max_duration_seconds:
                    print(f"\n⏱️  Maximum duration ({max_duration_seconds}s) reached")
                    break

                # Check if data stream is still active
                if not self.data_processor.is_running:
                    print(f"\n📊 Data stream ended - all dataset processed")
                    data_stream_active = False
                    break

                # Run event detection every 10 seconds
                if current_time - last_status_time >= 10:
                    self.check_for_events()
                    self.print_status()
                    last_status_time = current_time

                time.sleep(1)

        except KeyboardInterrupt:
            print("\n⚠️  Monitoring interrupted by user")

        elapsed_time = int(time.time() - start_time)
        if data_stream_active:
            print(f"\n✅ Monitoring completed ({elapsed_time} seconds)")
        else:
            print(f"\n✅ Monitoring completed - dataset fully processed ({elapsed_time} seconds)")

    def check_for_events(self):
        """Check for new events and alert if found"""
        try:
            new_events = self.event_detector.detect_all_events()

            if new_events:
                print(f"\nALERT: {len(new_events)} new event(s) detected!")
                for event in new_events[-3:]:  # Show last 3 events
                    event_name = event['event_data']['event_name']
                    station = event['event_data'].get('station_id', 'Unknown')
                    timestamp = event.get('timestamp', 'Unknown time')
                    print(f"   * {event_name} at {station} ({timestamp})")
                print("-" * 50)

        except Exception as e:
            print(f"Error in event detection: {e}")

    def print_status(self):
        """Print current system status"""
        status = self.data_processor.get_current_status()
        total_events = len(self.event_detector.detected_events)

        print(f"Status: RFID:{status['rfid_events']} | POS:{status['pos_events']} | "
              f"Queue:{status['queue_events']} | Recognition:{status['recognition_events']} | "
              f"Alerts:{total_events}")

    def generate_final_report(self, output_file="events.jsonl"):
        """Generate final events report"""
        print(f"\nGenerating final report...")

        # Save all detected events
        try:
            os.makedirs(os.path.dirname(output_file) if os.path.dirname(
                output_file) else ".", exist_ok=True)

            with open(output_file, 'w') as f:
                for event in self.event_detector.detected_events:
                    f.write(json.dumps(event) + '\n')

            print(f"Report saved: {output_file}")
            print(
                f"Total events detected: {len(self.event_detector.detected_events)}")

            # Print summary
            event_types = {}
            for event in self.event_detector.detected_events:
                event_name = event['event_data']['event_name']
                event_types[event_name] = event_types.get(event_name, 0) + 1

            print("\nEvent Summary:")
            for event_type, count in event_types.items():
                print(f"   • {event_type}: {count}")

        except Exception as e:
            print(f"Error saving report: {e}")

    def stop_system(self):
        """Stop the sentinel system"""
        self.is_running = False
        self.data_processor.stop_processing()

        # Stop API server
        self.api_server.stop_server()

        # Stop dashboard auto-update
        self.dashboard.stop_auto_update()
        print("Dashboard auto-update stopped")

        print("System stopped")


def main():
    """Main function to run the Sentinel system"""
    print("Initializing Project Sentinel...")

    # Check if streaming server is running
    try:
        import socket
        with socket.create_connection(("127.0.0.1", 8765), timeout=5):
            pass
    except:
        print("Error: Streaming server not running!")
        print("Please start the streaming server first:")
        print("cd ../../data/streaming-server")
        print("python stream_server.py --port 8765 --speed 10")
        print("Note: Remove --loop flag to process dataset once and end naturally")
        return

    system = SentinelSystem()

    try:
        # Start the system
        thread = system.start_system()

        # Run monitoring until data stream ends naturally (no fixed duration)
        # Optional: Set max_duration_seconds if you want a safety timeout
        system.run_monitoring_cycle(max_duration_seconds=3600)  # 1 hour max safety timeout

        # Generate final report
        system.generate_final_report("../evidence/output/test/events.jsonl")

    except Exception as e:
        print(f"System error: {e}")
    finally:
        system.stop_system()


if __name__ == "__main__":
    main()
