#!/usr/bin/env python3
"""
Automation script for Project Sentinel - Bit-Busters Team
This script runs the complete Retail Intelligence System for judges.

Usage: python3 run_demo.py
"""

import sys
import os
import subprocess
import time
import json
import signal
from pathlib import Path


class SentinelDemo:
    def __init__(self):
        self.streaming_process = None
        self.results_dir = "./results"

    def setup_environment(self):
        """Set up the environment and verify dependencies"""
        print("Setting up Project Sentinel environment...")

        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)

        # Check Python version
        if sys.version_info < (3, 7):
            print("Error: Python 3.7+ required")
            return False

        print("Environment ready")
        return True

    def start_streaming_server(self):
        """Start the data streaming server"""
        print("Starting data streaming server...")

        # Path to streaming server (relative to this script)
        server_path = "../../../../data/streaming-server/stream_server.py"

        if not os.path.exists(server_path):
            print(f"Error: Streaming server not found at {server_path}")
            return False

        try:
            # Start streaming server in background
            self.streaming_process = subprocess.Popen([
                sys.executable, server_path,
                "--port", "8765",
                "--speed", "20",  # 20x speed for faster demo
                "--loop"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for server to start
            time.sleep(3)

            # Check if process is still running
            if self.streaming_process.poll() is None:
                print("Streaming server started (port 8765)")
                return True
            else:
                print("Error: Streaming server failed to start")
                return False

        except Exception as e:
            print(f"Error starting streaming server: {e}")
            return False

    def run_sentinel_system(self):
        """Run the main Sentinel monitoring system"""
        print("Starting Sentinel monitoring system...")

        # Path to main application
        main_app_path = "../../src/main.py"

        if not os.path.exists(main_app_path):
            print(f"Error: Main application not found at {main_app_path}")
            return False

        try:
            # Change to src directory to run the application
            original_dir = os.getcwd()
            src_dir = os.path.dirname(os.path.abspath(main_app_path))
            os.chdir(src_dir)

            # Run the main application
            result = subprocess.run([
                sys.executable, "main.py"
            ], capture_output=True, text=True, timeout=180)  # 3 minute timeout

            # Return to original directory
            os.chdir(original_dir)

            if result.returncode == 0:
                print("Sentinel system completed successfully")
                print("Output:")
                print(result.stdout)
                return True
            else:
                print("Error running Sentinel system")
                print("Error output:", result.stderr)
                return False

        except subprocess.TimeoutExpired:
            print("Sentinel system completed (timeout reached)")
            return True
        except Exception as e:
            print(f"Error running Sentinel system: {e}")
            return False

    def copy_results(self):
        """Copy generated results to the results directory"""
        print("Copying results...")

        try:
            # Copy events.jsonl from evidence/output/test to results
            source_file = "../output/test/events.jsonl"
            dest_file = os.path.join(self.results_dir, "events.jsonl")

            if os.path.exists(source_file):
                import shutil
                shutil.copy2(source_file, dest_file)
                print(f"Results copied to {dest_file}")

                # Show summary
                with open(dest_file, 'r') as f:
                    events = [json.loads(line) for line in f if line.strip()]
                    print(f"Generated {len(events)} events")

                    # Count event types
                    event_types = {}
                    for event in events:
                        event_name = event['event_data']['event_name']
                        event_types[event_name] = event_types.get(
                            event_name, 0) + 1

                    for event_type, count in event_types.items():
                        print(f"   • {event_type}: {count}")

                return True
            else:
                print(f"Warning: Results file not found at {source_file}")
                return False

        except Exception as e:
            print(f"Error copying results: {e}")
            return False

    def cleanup(self):
        """Clean up processes and temporary files"""
        print("Cleaning up...")

        if self.streaming_process:
            try:
                self.streaming_process.terminate()
                self.streaming_process.wait(timeout=5)
                print("Streaming server stopped")
            except subprocess.TimeoutExpired:
                self.streaming_process.kill()
                print("Streaming server force-stopped")
            except Exception as e:
                print(f"Error stopping streaming server: {e}")

    def run_demo(self):
        """Run the complete demo"""
        print("=" * 60)
        print("PROJECT SENTINEL DEMO - BIT-BUSTERS TEAM")
        print("=" * 60)

        success = True

        try:
            # Step 1: Setup
            if not self.setup_environment():
                return False

            # Step 2: Start streaming server
            if not self.start_streaming_server():
                return False

            # Step 3: Run Sentinel system
            if not self.run_sentinel_system():
                success = False

            # Step 4: Copy results
            if not self.copy_results():
                success = False

        except KeyboardInterrupt:
            print("\nDemo interrupted by user")
            success = False
        except Exception as e:
            print(f"Unexpected error: {e}")
            success = False
        finally:
            self.cleanup()

        if success:
            print("\nDemo completed successfully!")
            print(f"Results available in: {os.path.abspath(self.results_dir)}")
        else:
            print("\nDemo completed with errors")

        return success


def main():
    """Main function"""
    demo = SentinelDemo()

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\nReceived interrupt signal")
        demo.cleanup()
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)

    # Run the demo
    success = demo.run_demo()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
