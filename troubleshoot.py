#!/usr/bin/env python3
"""
Project Sentinel - Troubleshooting and Health Check Script
Diagnoses common issues and provides solutions
"""

import sys
import os
import socket
import subprocess
import time
import requests
from pathlib import Path

class SentinelTroubleshooter:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.issues_found = []
        self.solutions = []
        
    def print_header(self):
        print("=" * 70)
        print("🛡️  PROJECT SENTINEL - TROUBLESHOOTING & HEALTH CHECK")
        print("=" * 70)
        
    def check_python_version(self):
        """Check Python version"""
        print("🐍 Checking Python version...")
        if sys.version_info >= (3, 7):
            print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - OK")
            return True
        else:
            print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Need 3.7+")
            self.issues_found.append("Python version too old")
            self.solutions.append("Upgrade to Python 3.7 or higher")
            return False
    
    def check_npm_availability(self):
        """Check if npm is available"""
        print("📦 Checking npm availability...")
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ npm {result.stdout.strip()} - OK")
                return True
            else:
                print("❌ npm not responding")
                self.issues_found.append("npm not working")
                self.solutions.append("Reinstall Node.js from https://nodejs.org/")
                return False
        except FileNotFoundError:
            print("❌ npm not found")
            self.issues_found.append("npm not installed")
            self.solutions.append("Install Node.js from https://nodejs.org/")
            return False
    
    def check_ports(self):
        """Check if required ports are available"""
        print("🔌 Checking port availability...")
        ports_to_check = [
            (8765, "Data streaming server"),
            (3000, "React development server"),
            (3001, "API server")
        ]
        
        all_clear = True
        for port, description in ports_to_check:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(('localhost', port))
                    if result == 0:
                        print(f"⚠️  Port {port} ({description}) is in use")
                        self.issues_found.append(f"Port {port} occupied")
                        self.solutions.append(f"Stop process using port {port} or restart computer")
                        all_clear = False
                    else:
                        print(f"✅ Port {port} ({description}) - Available")
            except Exception as e:
                print(f"❓ Port {port} ({description}) - Could not check: {e}")
        
        return all_clear
    
    def check_file_structure(self):
        """Check essential files exist"""
        print("📁 Checking file structure...")
        
        essential_files = [
            "launch_synchronized_system.py",
            "data/streaming-server/stream_server.py",
            "submission-structure/Bit-Busters/src/main.py",
            "submission-structure/Bit-Busters/src/api_server.py",
            "submission-structure/Bit-Busters/react-dashboard/package.json",
            "submission-structure/Bit-Busters/react-dashboard/src/App.js"
        ]
        
        all_present = True
        for file_path in essential_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ Missing: {file_path}")
                self.issues_found.append(f"Missing file: {file_path}")
                self.solutions.append(f"Restore missing file: {file_path}")
                all_present = False
        
        return all_present
    
    def check_react_dependencies(self):
        """Check React dependencies"""
        print("⚛️  Checking React dependencies...")
        
        react_dir = self.base_path / "submission-structure/Bit-Busters/react-dashboard"
        node_modules = react_dir / "node_modules"
        
        if not node_modules.exists():
            print("❌ node_modules not found")
            self.issues_found.append("React dependencies not installed")
            self.solutions.append(f"Run: cd \"{react_dir}\" && npm install")
            return False
        
        # Check for lucide-react specifically
        lucide_path = node_modules / "lucide-react"
        if not lucide_path.exists():
            print("❌ lucide-react not installed")
            self.issues_found.append("lucide-react missing")
            self.solutions.append(f"Run: cd \"{react_dir}\" && npm install lucide-react")
            return False
        
        print("✅ React dependencies look good")
        return True
    
    def test_api_connectivity(self):
        """Test if API server can be reached"""
        print("🔗 Testing API connectivity...")
        
        # This assumes the system might be running
        try:
            response = requests.get('http://localhost:3001/api/status', timeout=2)
            if response.status_code == 200:
                print("✅ API server responding")
                return True
            else:
                print(f"⚠️  API server returned status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❓ API server not running (this is OK if system is not started)")
            return True  # Not an error if system isn't running
        except Exception as e:
            print(f"❌ API connectivity issue: {e}")
            self.issues_found.append("API connectivity problem")
            self.solutions.append("Check if main system is running correctly")
            return False
    
    def test_streaming_server_connectivity(self):
        """Test streaming server connectivity"""
        print("🌊 Testing streaming server connectivity...")
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                result = s.connect_ex(('localhost', 8765))
                if result == 0:
                    print("✅ Streaming server port reachable")
                    return True
                else:
                    print("❓ Streaming server not running (this is OK if system is not started)")
                    return True  # Not an error if system isn't running
        except Exception as e:
            print(f"❌ Streaming server connectivity issue: {e}")
            self.issues_found.append("Streaming server connectivity problem")
            self.solutions.append("Check firewall settings or restart system")
            return False
    
    def run_health_check(self):
        """Run complete health check"""
        self.print_header()
        
        print("Running comprehensive health check...\n")
        
        checks = [
            ("Python Version", self.check_python_version),
            ("npm Availability", self.check_npm_availability),
            ("Port Availability", self.check_ports),
            ("File Structure", self.check_file_structure),
            ("React Dependencies", self.check_react_dependencies),
            ("API Connectivity", self.test_api_connectivity),
            ("Streaming Server", self.test_streaming_server_connectivity)
        ]
        
        results = []
        for check_name, check_func in checks:
            print(f"\n--- {check_name} ---")
            try:
                result = check_func()
                results.append((check_name, result))
            except Exception as e:
                print(f"❌ Error during {check_name}: {e}")
                results.append((check_name, False))
                self.issues_found.append(f"Error in {check_name}: {e}")
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 HEALTH CHECK SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for check_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {check_name}")
        
        print(f"\nOverall: {passed}/{total} checks passed")
        
        if self.issues_found:
            print("\n🔧 ISSUES FOUND:")
            for i, issue in enumerate(self.issues_found, 1):
                print(f"{i}. {issue}")
            
            print("\n💡 RECOMMENDED SOLUTIONS:")
            for i, solution in enumerate(self.solutions, 1):
                print(f"{i}. {solution}")
        else:
            print("\n🎉 No issues found! System should work correctly.")
        
        print("\n" + "=" * 70)
        
        return len(self.issues_found) == 0
    
    def quick_fix_attempt(self):
        """Attempt to fix common issues automatically"""
        print("\n🔧 ATTEMPTING QUICK FIXES...")
        
        # Fix React dependencies
        react_dir = self.base_path / "submission-structure/Bit-Busters/react-dashboard"
        if not (react_dir / "node_modules").exists():
            print("📦 Installing React dependencies...")
            try:
                subprocess.run(['npm', 'install'], cwd=react_dir, check=True)
                print("✅ React dependencies installed")
            except subprocess.CalledProcessError:
                print("❌ Failed to install React dependencies")
        
        # Install lucide-react if missing
        if not (react_dir / "node_modules" / "lucide-react").exists():
            print("📦 Installing lucide-react...")
            try:
                subprocess.run(['npm', 'install', 'lucide-react'], cwd=react_dir, check=True)
                print("✅ lucide-react installed")
            except subprocess.CalledProcessError:
                print("❌ Failed to install lucide-react")

def main():
    """Main function"""
    troubleshooter = SentinelTroubleshooter()
    
    print("Would you like to:")
    print("1. Run health check only")
    print("2. Run health check + attempt fixes")
    print("3. Just attempt fixes")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return
    
    if choice in ['1', '2']:
        healthy = troubleshooter.run_health_check()
        
        if choice == '2' and not healthy:
            troubleshooter.quick_fix_attempt()
            print("\n🔄 Re-running health check after fixes...")
            troubleshooter.issues_found = []
            troubleshooter.solutions = []
            troubleshooter.run_health_check()
    
    elif choice == '3':
        troubleshooter.quick_fix_attempt()
    
    else:
        print("Invalid choice. Running health check only.")
        troubleshooter.run_health_check()
    
    print("\n💡 To start the system after fixes:")
    print("python launch_synchronized_system.py")

if __name__ == "__main__":
    main()