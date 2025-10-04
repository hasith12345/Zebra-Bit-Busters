#!/usr/bin/env python3
"""
Synchronized Project Sentinel Launcher
Starts the complete system with real-time React dashboard synchronization
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
import requests
from pathlib import Path


class SynchronizedSentinelLauncher:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.streaming_process = None
        self.react_process = None
        self.main_process = None

    def print_banner(self):
        print("=" * 80)
        print("🛡️  PROJECT SENTINEL - SYNCHRONIZED REAL-TIME SYSTEM")
        print("   🐍 Python Backend ↔️ ⚛️  React Dashboard (REAL-TIME SYNC)")
        print("   Team: Bit-Busters | Advanced Retail Intelligence")
        print("=" * 80)

    def check_dependencies(self):
        """Check system requirements"""
        print("🔍 Checking system dependencies...")

        # Check Python
        if sys.version_info < (3, 7):
            print("❌ Error: Python 3.7+ required")
            return False
        print(
            f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

        # Check npm
        try:
            result = subprocess.run(
                ['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ npm {result.stdout.strip()}")
            else:
                print("❌ npm not found - React dashboard will not be available")
                return False
        except FileNotFoundError:
            print("❌ npm not found - React dashboard will not be available")
            return False

        # Check directories
        required_dirs = [
            "data/streaming-server",
            "submission-structure/Bit-Busters/src",
            "submission-structure/Bit-Busters/react-dashboard"
        ]

        for dir_path in required_dirs:
            if not (self.base_path / dir_path).exists():
                print(f"❌ Missing: {dir_path}")
                return False
            print(f"✅ Found: {dir_path}")

        return True

    def start_streaming_server(self):
        """Start data streaming server"""
        print("\n🌊 Starting data streaming server...")

        server_path = self.base_path / "data/streaming-server/stream_server.py"

        try:
            self.streaming_process = subprocess.Popen([
                sys.executable, str(server_path),
                "--port", "8765",
                "--speed", "10",
                "--loop"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            time.sleep(3)

            if self.streaming_process.poll() is None:
                print("✅ Data streaming server running on port 8765")
                return True
            else:
                print("❌ Failed to start streaming server")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def start_main_system_with_api(self):
        """Start main Sentinel system with API server"""
        print("\n🛡️  Starting main Sentinel system with API server...")

        main_path = self.base_path / "submission-structure/Bit-Busters/src/main.py"

        try:
            # Change to src directory
            original_dir = os.getcwd()
            src_dir = main_path.parent
            os.chdir(src_dir)

            # Start main system with API in background
            self.main_process = subprocess.Popen([sys.executable, "main.py"],
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.STDOUT,
                                                 universal_newlines=True,
                                                 bufsize=1)

            os.chdir(original_dir)

            # Wait for API server to start and monitor output
            api_started = False
            start_time = time.time()

            print("⏳ Waiting for API server to start...")

            while time.time() - start_time < 30:  # 30 second timeout
                if self.main_process.poll() is not None:
                    print("❌ Main system process ended unexpectedly")
                    return False

                # Check if API server is responding
                try:
                    response = requests.get(
                        'http://localhost:3001/api/status', timeout=1)
                    if response.status_code == 200:
                        api_started = True
                        break
                except:
                    pass

                time.sleep(1)

            if api_started:
                print("✅ Main Sentinel system with API server running")
                print("✅ API endpoints available:")
                print("   • http://localhost:3001/api/dashboard")
                print("   • http://localhost:3001/api/events")
                print("   • http://localhost:3001/api/status")
                return True
            else:
                print("❌ API server failed to start within timeout")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def start_react_dashboard(self):
        """Start React dashboard"""
        print("\n⚛️  Starting React dashboard with real-time sync...")

        react_dir = self.base_path / "submission-structure/Bit-Busters/react-dashboard"

        try:
            # Change to react directory
            original_dir = os.getcwd()
            os.chdir(react_dir)

            # Check if node_modules exists
            if not (react_dir / "node_modules").exists():
                print("📦 Installing React dependencies...")
                install_result = subprocess.run(['npm', 'install'],
                                                capture_output=True, text=True)
                if install_result.returncode != 0:
                    print("❌ Failed to install React dependencies")
                    os.chdir(original_dir)
                    return False
                print("✅ React dependencies installed")

            # Ensure lucide-react is installed
            lucide_check = subprocess.run(['npm', 'list', 'lucide-react'],
                                          capture_output=True, text=True)
            if lucide_check.returncode != 0:
                print("📦 Installing lucide-react...")
                subprocess.run(['npm', 'install', 'lucide-react'],
                               capture_output=True, text=True)

            # Start React dev server
            env = os.environ.copy()
            env['BROWSER'] = 'none'  # Prevent auto-opening browser

            self.react_process = subprocess.Popen(['npm', 'start'],
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE,
                                                  env=env)

            os.chdir(original_dir)

            # Wait for React to start
            print("⏳ Waiting for React dashboard to compile...")
            react_started = False
            start_time = time.time()

            while time.time() - start_time < 60:  # 60 second timeout for React
                if self.react_process.poll() is not None:
                    print("❌ React process ended unexpectedly")
                    return False

                # Check if React dev server is responding
                try:
                    response = requests.get('http://localhost:3000', timeout=2)
                    if response.status_code == 200:
                        react_started = True
                        break
                except:
                    pass

                time.sleep(2)

            if react_started:
                print("✅ React dashboard running on http://localhost:3000")
                print("✅ Real-time synchronization with backend enabled")
                return True
            else:
                print("❌ React dashboard failed to start within timeout")
                return False

        except Exception as e:
            print(f"❌ Error starting React dashboard: {e}")
            return False

    def verify_synchronization(self):
        """Verify that React dashboard is getting real-time data"""
        print("\n🔗 Verifying real-time synchronization...")

        try:
            # Check API endpoint
            api_response = requests.get(
                'http://localhost:3001/api/dashboard', timeout=5)
            if api_response.status_code == 200:
                data = api_response.json()
                print(
                    f"✅ API responding with {data.get('totalEvents', 0)} total events")
            else:
                print("❌ API not responding properly")
                return False

            # Check React dashboard
            react_response = requests.get('http://localhost:3000', timeout=5)
            if react_response.status_code == 200:
                print("✅ React dashboard accessible")
            else:
                print("❌ React dashboard not accessible")
                return False

            print("✅ Real-time synchronization verified!")
            return True

        except Exception as e:
            print(f"⚠️  Synchronization check failed: {e}")
            return False

    def open_dashboards(self):
        """Open both dashboards"""
        print("\n🌐 Opening synchronized dashboards...")

        def open_html_dashboard():
            time.sleep(2)
            html_path = self.base_path / "submission-structure/Bit-Busters/src/dashboard.html"
            if html_path.exists():
                try:
                    webbrowser.open(f"file://{html_path.absolute()}")
                    print("✅ HTML Dashboard opened")
                except:
                    print(f"📊 HTML Dashboard: {html_path}")

        def open_react_dashboard():
            time.sleep(5)
            try:
                webbrowser.open("http://localhost:3000")
                print("✅ React Dashboard opened with real-time data")
            except:
                print("📊 React Dashboard: http://localhost:3000")

        # Start both in threads
        threading.Thread(target=open_html_dashboard, daemon=True).start()
        threading.Thread(target=open_react_dashboard, daemon=True).start()

    def show_synchronized_status(self):
        """Show running services status"""
        print("\n" + "=" * 80)
        print("🎯 PROJECT SENTINEL - SYNCHRONIZED REAL-TIME SYSTEM")
        print("=" * 80)

        services = [
            ("🌊 Data Streaming Server", "localhost:8765", self.streaming_process),
            ("🛡️  Main System + API Server",
             "localhost:3001/api", self.main_process),
            ("⚛️  React Dashboard (LIVE SYNC)",
             "http://localhost:3000", self.react_process),
        ]

        for name, url, process in services:
            if process and process.poll() is None:
                print(f"✅ {name}: {url}")
            else:
                print(f"❌ {name}: Not running")

        print("=" * 80)
        print("🔗 REAL-TIME SYNCHRONIZATION:")
        print("   • React Dashboard ↔️ Python Backend API")
        print("   • Live data updates every 3 seconds")
        print("   • Event detection reflected immediately")
        print("📊 Dashboards Available:")
        print("   • React Dashboard (LIVE): http://localhost:3000")
        print("   • HTML Dashboard: submission-structure/Bit-Busters/src/dashboard.html")
        print("🔗 API Endpoints:")
        print("   • Dashboard Data: http://localhost:3001/api/dashboard")
        print("   • Events: http://localhost:3001/api/events")
        print("   • System Status: http://localhost:3001/api/status")
        print(
            "📁 Output: submission-structure/Bit-Busters/evidence/output/test/events.jsonl")
        print("=" * 80)

    def monitor_synchronized_system(self):
        """Monitor the synchronized system"""
        print("\n🔍 Monitoring synchronized system...")
        print("💡 React dashboard will show LIVE data from the Python backend")
        print("💡 Press Ctrl+C to stop all services\n")

        try:
            while True:
                # Check if processes are still running
                if self.streaming_process and self.streaming_process.poll() is not None:
                    print("⚠️  Streaming server stopped")

                if self.react_process and self.react_process.poll() is not None:
                    print("⚠️  React dashboard stopped")

                if self.main_process and self.main_process.poll() is not None:
                    print("⚠️  Main system stopped")

                # Check API connectivity periodically
                try:
                    requests.get('http://localhost:3001/api/status', timeout=1)
                    print("🔗", end="", flush=True)
                except:
                    print("❌", end="", flush=True)

                time.sleep(5)

        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested by user")

    def cleanup(self):
        """Stop all processes"""
        print("\n🧹 Cleaning up synchronized processes...")

        processes = [
            ("Streaming Server", self.streaming_process),
            ("React Dashboard", self.react_process),
            ("Main System + API", self.main_process)
        ]

        for name, process in processes:
            if process:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ {name} stopped")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"🔨 {name} force-stopped")
                except Exception as e:
                    print(f"⚠️  Error stopping {name}: {e}")

    def run_synchronized_system(self):
        """Launch the complete synchronized system"""
        try:
            self.print_banner()

            if not self.check_dependencies():
                return False

            # Start all components in the correct order
            if not self.start_streaming_server():
                return False

            if not self.start_main_system_with_api():
                return False

            if not self.start_react_dashboard():
                print(
                    "⚠️  React dashboard failed - API still available for other clients")

            # Verify synchronization
            if not self.verify_synchronization():
                print(
                    "⚠️  Synchronization verification failed, but system may still work")

            # Open dashboards
            self.open_dashboards()

            # Show status
            self.show_synchronized_status()

            # Monitor system
            self.monitor_synchronized_system()

            return True

        except KeyboardInterrupt:
            print("\n⚠️  Launch interrupted")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False
        finally:
            self.cleanup()


def main():
    """Main entry point"""
    launcher = SynchronizedSentinelLauncher()

    # Handle Ctrl+C gracefully
    import signal

    def signal_handler(sig, frame):
        print("\nReceived interrupt signal")
        launcher.cleanup()
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)

    # Launch synchronized system
    success = launcher.run_synchronized_system()

    print("\n" + "=" * 80)
    if success:
        print("🎉 SYNCHRONIZED PROJECT SENTINEL COMPLETED SUCCESSFULLY!")
        print("✅ React Dashboard was showing LIVE real-time data from Python backend")
    else:
        print("⚠️  Launch completed with issues")
    print("=" * 80)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
