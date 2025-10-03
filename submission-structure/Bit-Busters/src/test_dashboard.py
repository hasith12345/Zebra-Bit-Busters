#!/usr/bin/env python3
"""
Quick test for the enhanced dashboard
"""

import time
from data_processor import DataProcessor
from event_detector import EventDetector
from dashboard import SentinelDashboard


def test_dashboard():
    """Test the dashboard functionality"""
    print("Testing Enhanced Dashboard...")

    # Create components
    data_processor = DataProcessor()
    event_detector = EventDetector(data_processor)
    dashboard = SentinelDashboard(data_processor, event_detector)

    print("Components created")

    # Generate a test dashboard
    dashboard_path = dashboard.create_dashboard()
    print(f"Dashboard created at: {dashboard_path}")

    # Start auto-update
    dashboard.start_auto_update()
    print("Auto-update started")

    # Run for a short time
    print("Running for 30 seconds...")
    time.sleep(30)

    # Stop auto-update
    dashboard.stop_auto_update()
    print("Auto-update stopped")

    print("Test completed!")


if __name__ == "__main__":
    test_dashboard()
