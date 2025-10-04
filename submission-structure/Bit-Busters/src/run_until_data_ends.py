#!/usr/bin/env python3
"""
Project Sentinel - Complete System Startup Script
This script starts the streaming server without loop and runs the monitoring system
until all dataset is processed.
"""

import subprocess
import time
import sys
import os
import signal
from pathlib import Path

def start_streaming_server():
    """Start the streaming server without loop"""
    print("🚀 Starting streaming server...")
    
    # Navigate to streaming server directory
    server_dir = Path(__file__).parent.parent.parent / "data" / "streaming-server"
    
    # Start server without --loop flag so it ends when data is done
    cmd = [
        sys.executable, "stream_server.py", 
        "--port", "8765", 
        "--speed", "10"
        # Note: No --loop flag, so server will end when dataset is complete
    ]
    
    try:
        server_process = subprocess.Popen(
            cmd, 
            cwd=server_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"✅ Streaming server started (PID: {server_process.pid})")
        print("📊 Server will process dataset once and end naturally")
        return server_process
        
    except Exception as e:
        print(f"❌ Failed to start streaming server: {e}")
        return None

def start_monitoring_system():
    """Start the monitoring system"""
    print("\n🧠 Starting AI monitoring system...")
    
    # Navigate to src directory
    src_dir = Path(__file__).parent
    
    cmd = [sys.executable, "main.py"]
    
    try:
        monitoring_process = subprocess.Popen(
            cmd,
            cwd=src_dir,
            text=True
        )
        
        print(f"✅ Monitoring system started (PID: {monitoring_process.pid})")
        return monitoring_process
        
    except Exception as e:
        print(f"❌ Failed to start monitoring system: {e}")
        return None

def main():
    """Main function to orchestrate the complete system"""
    print("=" * 70)
    print("🧠 PROJECT SENTINEL - COMPLETE DATASET PROCESSING")
    print("=" * 70)
    print("📊 Processing entire dataset until completion...")
    print("🔄 System will run until all 13,463+ data points are processed")
    print("=" * 70)
    
    server_process = None
    monitoring_process = None
    
    try:
        # Start streaming server first
        server_process = start_streaming_server()
        if not server_process:
            return 1
            
        # Wait a moment for server to start
        time.sleep(3)
        
        # Start monitoring system
        monitoring_process = start_monitoring_system()
        if not monitoring_process:
            return 1
        
        print("\n🎯 Both systems running...")
        print("💡 The system will automatically stop when all dataset is processed")
        print("🛑 Press Ctrl+C to stop manually if needed")
        print("-" * 50)
        
        # Wait for monitoring process to complete
        monitoring_process.wait()
        
        print("\n✅ Monitoring system completed!")
        print("📊 All dataset has been processed")
        
        # Give server a moment to finish
        time.sleep(2)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  System interrupted by user")
        return 0
        
    except Exception as e:
        print(f"\n❌ System error: {e}")
        return 1
        
    finally:
        # Cleanup processes
        if monitoring_process and monitoring_process.poll() is None:
            print("🛑 Stopping monitoring system...")
            monitoring_process.terminate()
            
        if server_process and server_process.poll() is None:
            print("🛑 Stopping streaming server...")
            server_process.terminate()
            
        print("🏁 System shutdown complete")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)