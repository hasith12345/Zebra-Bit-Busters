#!/usr/bin/env python3
"""
Project Sentinel - Complete System Launcher
Team: Bit-Busters

This script launches the complete Project Sentinel system with:
1. Streaming server (sensor data simulation)
2. Python backend (detection + API server)
3. React dashboard (real-time frontend)

Usage: python run_complete_system.py
"""

import os
import sys
import time
import subprocess
import threading
import signal
from pathlib import Path


class ProjectSentinelLauncher:
    def __init__(self):
        self.processes = []
        self.base_path = Path(__file__).parent.parent.parent.parent
        self.src_path = Path(__file__).parent
        self.dashboard_path = self.src_path.parent / "react-dashboard"
        self.streaming_path = self.base_path / "data" / "streaming-server"

        # Use full npm path if needed
        self.npm_cmd = self._find_npm()

    def _find_npm(self):
        """Find npm executable"""
        try:
            # Try system PATH first
            result = subprocess.run(
                ['where', 'npm'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return 'npm'
        except:
            pass

        # Try common locations
        npm_paths = [
            "C:\\Program Files\\nodejs\\npm.cmd",
            "C:\\Program Files (x86)\\nodejs\\npm.cmd"
        ]

        for path in npm_paths:
            if os.path.exists(path):
                return f'"{path}"'

        return 'npm'  # Fallback

    def check_ports(self):
        """Check if required ports are available"""
        import socket

        ports = [8765, 3000, 3001]
        occupied = []

        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                result = sock.connect_ex(('127.0.0.1', port))
                if result == 0:
                    occupied.append(port)
            except:
                pass
            finally:
                sock.close()

        if occupied:
            print(
                f"⚠️  Ports {occupied} are occupied. Attempting to free them...")
            return False
        return True

    def start_streaming_server(self):
        """Start the TCP streaming server"""
        print("🌊 Starting streaming server...")

        cmd = [
            sys.executable,
            str(self.streaming_path / "stream_server.py"),
            "--port", "8765",
            "--speed", "10",
            "--loop"
        ]

        process = subprocess.Popen(
            cmd,
            cwd=str(self.streaming_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        self.processes.append(('Streaming Server', process))
        print("✅ Streaming server started on port 8765")
        return process

    def start_python_backend(self):
        """Start the Python backend with API server"""
        print("🐍 Starting Python backend with API server...")

        cmd = [sys.executable, "main.py"]

        process = subprocess.Popen(
            cmd,
            cwd=str(self.src_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        self.processes.append(('Python Backend', process))
        print("✅ Python backend started with API server on port 3001")
        return process

    def start_react_dashboard(self):
        """Start the React dashboard"""
        print("⚛️  Starting React dashboard...")

        # Check if dependencies are installed
        if not (self.dashboard_path / "node_modules").exists():
            print("📦 Installing React dependencies...")
            install_cmd = f'{self.npm_cmd} install'

            install_process = subprocess.run(
                install_cmd,
                cwd=str(self.dashboard_path),
                shell=True,
                capture_output=True,
                text=True
            )

            if install_process.returncode != 0:
                print(f"❌ npm install failed: {install_process.stderr}")
                return None
            print("✅ Dependencies installed")

        # Start React dev server
        cmd = f'{self.npm_cmd} start'

        process = subprocess.Popen(
            cmd,
            cwd=str(self.dashboard_path),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        self.processes.append(('React Dashboard', process))
        print("✅ React dashboard starting on port 3000")
        return process

    def wait_for_startup(self):
        """Wait for all services to start"""
        print("\n⏳ Waiting for services to initialize...")

        for i in range(10):
            time.sleep(1)
            print(f"   {i+1}/10 seconds...")

        print("\n🚀 All services should be running!")

    def show_status(self):
        """Show system status"""
        print("\n" + "="*60)
        print("📊 PROJECT SENTINEL - SYSTEM STATUS")
        print("="*60)

        urls = [
            ("🌊 Streaming Server", "tcp://localhost:8765"),
            ("🐍 Python Backend API", "http://localhost:3001/api/status"),
            ("📊 HTML Dashboard", "http://localhost:3001/dashboard"),
            ("⚛️  React Dashboard", "http://localhost:3000")
        ]

        for name, url in urls:
            print(f"{name:<25} → {url}")

        print("\n💡 Tips:")
        print("   • Open React Dashboard: http://localhost:3000")
        print("   • Check API status: http://localhost:3001/api/status")
        print("   • View events: http://localhost:3001/api/events")
        print("   • Press Ctrl+C to stop all services")
        print("="*60)

    def cleanup(self):
        """Stop all processes"""
        print("\n🛑 Stopping all services...")

        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"🔥 {name} force killed")
            except Exception as e:
                print(f"⚠️  Error stopping {name}: {e}")

        print("👋 All services stopped. Goodbye!")

    def run(self):
        """Main execution method"""
        print("🎯 PROJECT SENTINEL - COMPLETE SYSTEM LAUNCHER")
        print("=" * 50)

        try:
            # Pre-flight checks
            if not self.check_ports():
                print("Please stop conflicting processes and try again.")
                return

            # Start all services
            streaming = self.start_streaming_server()
            if not streaming:
                return

            time.sleep(2)  # Give streaming server time to start

            backend = self.start_python_backend()
            if not backend:
                return

            time.sleep(3)  # Give backend time to start

            react = self.start_react_dashboard()
            if not react:
                return

            # Wait and show status
            self.wait_for_startup()
            self.show_status()

            # Keep running until interrupted
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🔴 Shutdown requested...")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.cleanup()


def main():
    """Entry point"""
    launcher = ProjectSentinelLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
