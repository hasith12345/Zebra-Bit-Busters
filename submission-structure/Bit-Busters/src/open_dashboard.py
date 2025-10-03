#!/usr/bin/env python3
"""
Dashboard Viewer - Opens the dashboard in the default browser
"""

import webbrowser
import os
import sys


def open_dashboard():
    """Open the dashboard in default browser"""
    dashboard_path = os.path.join(os.getcwd(), "dashboard.html")

    if os.path.exists(dashboard_path):
        webbrowser.open(f"file://{dashboard_path}")
        print(f"Dashboard opened in browser: {dashboard_path}")
    else:
        print("Dashboard not found! Please run the system first to generate the dashboard.")
        sys.exit(1)


if __name__ == "__main__":
    open_dashboard()
