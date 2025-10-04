#!/usr/bin/env python3
"""
Enhanced Clean Production Demo for Project Sentinel AI System
Production-ready demonstration of intelligent retail monitoring capabilities

This script demonstrates the complete Project Sentinel system with:
- Real-time data processing from multiple sensor inputs
- AI-powered event detection and threat assessment
- Predictive analytics and forecasting
- Intelligent automation and optimization
- Comprehensive reporting and analytics
"""

import sys
import os
import time
import json
from datetime import datetime

# Add the src directory to the path
current_file_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(os.path.dirname(current_file_dir)), 'src')
sys.path.insert(0, src_dir)

from data_processor import DataProcessor
from event_detector import EventDetector


def print_system_banner():
    """Print clean system banner"""
    print("="*70)
    print("🛡️  PROJECT SENTINEL - AI RETAIL MONITORING SYSTEM")
    print("="*70)
    print("🤖 Enhanced with Artificial Intelligence & Machine Learning")
    print("📊 Real-time Analytics & Predictive Intelligence")
    print("🎯 Advanced Security & Fraud Detection")
    print("="*70)
    print()


def check_data_availability():
    """Check if required data files are available"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    data_dir = os.path.join(project_root, "data", "input")
    
    required_files = [
        "pos_transactions.jsonl",
        "inventory_snapshots.jsonl", 
        "queue_monitoring.jsonl",
        "rfid_readings.jsonl",
        "product_recognition.jsonl",
        "products_list.csv",
        "customer_data.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(data_dir, file)):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️ Warning: Missing data files: {missing_files}")
        print("   System will use simulated data for demonstration")
    else:
        print("✅ All required data files found")
    
    return len(missing_files) == 0


def run_production_demo():
    """Run the production demonstration"""
    print_system_banner()
    
    # Check system prerequisites
    print("🔍 SYSTEM CHECK...")
    data_available = check_data_availability()
    
    # Initialize system components
    print("\n🚀 INITIALIZING SYSTEM COMPONENTS...")
    data_processor = DataProcessor()
    event_detector = EventDetector(data_processor)
    
    # Load reference data
    print("📚 Loading reference data...")
    data_processor.load_reference_data()
    data_processor.load_historical_data()
    
    print(f"   Products loaded: {len(data_processor.products_db)}")
    print(f"   Historical transactions: {len(data_processor.historical_transactions)}")
    print(f"   Historical inventory: {len(data_processor.historical_inventory)}")
    
    # Simulate real-time processing
    print("\n⚡ STARTING REAL-TIME MONITORING...")
    print("   Monitoring for anomalies and security events...")
    print("   Press Ctrl+C to stop monitoring\n")
    
    monitoring_start = time.time()
    event_count = 0
    
    try:
        # Run monitoring loop
        for cycle in range(20):  # 20 monitoring cycles
            current_time = datetime.now()
            print(f"🕐 {current_time.strftime('%H:%M:%S')} - Monitoring Cycle {cycle + 1}")
            
            # Simulate some data processing
            if data_available and data_processor.historical_transactions:
                # Use historical data to simulate real-time events
                transaction_sample = data_processor.historical_transactions[cycle % len(data_processor.historical_transactions)]
                data_processor.pos_data.append(transaction_sample)
            
            # Run event detection
            detected_events = event_detector.detect_all_events()
            
            if detected_events:
                event_count += len(detected_events)
                print(f"   ⚠️ {len(detected_events)} new event(s) detected!")
                
                # Show summary of detected events
                for event in detected_events[-3:]:  # Show last 3 events
                    event_data = event.get('event_data', {})
                    event_name = event_data.get('event_name', 'Unknown Event')
                    severity = event_data.get('severity', 'medium')
                    station = event_data.get('station_id', 'N/A')
                    
                    severity_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(severity, '⚪')
                    print(f"      {severity_icon} {event_name} at {station}")
            else:
                print("   ✅ No anomalies detected - system operating normally")
            
            # Brief pause between monitoring cycles
            time.sleep(1)
            
            # Show periodic summary
            if (cycle + 1) % 5 == 0:
                print(f"\n📊 Monitoring Summary (Cycle {cycle + 1}):")
                print(f"   Events detected: {event_count}")
                elapsed = time.time() - monitoring_start
                print(f"   Monitoring duration: {elapsed:.1f} seconds")
                
                # Show system health
                health_score = event_detector.calculate_system_health_score()
                print(f"   System health: {health_score:.1f}/100")
                print()
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Monitoring stopped by user")
    
    # Generate final results
    print("\n📋 GENERATING FINAL REPORT...")
    
    # Save events to required output files
    output_dir_test = "../output/test"
    output_dir_final = "../output/final"
    
    os.makedirs(output_dir_test, exist_ok=True)
    os.makedirs(output_dir_final, exist_ok=True)
    
    # Save to test output
    test_file = os.path.join(output_dir_test, "events.jsonl")
    event_detector.save_events_to_file(test_file)
    
    # Save to final output (same events for demo)
    final_file = os.path.join(output_dir_final, "events.jsonl")
    event_detector.save_events_to_file(final_file)
    
    # Generate summary report
    summary = event_detector.get_detection_summary()
    
    print("\n" + "="*70)
    print("📊 FINAL MONITORING REPORT")
    print("="*70)
    print(f"🕐 Monitoring Duration: {time.time() - monitoring_start:.1f} seconds")
    print(f"🎯 Total Events Detected: {summary['total_events']}")
    print(f"🛡️ System Health Score: {summary['risk_metrics']['system_health_score']:.1f}/100")
    print(f"⚠️ High-Risk Customers: {summary['risk_metrics']['high_risk_customers']}")
    print(f"🚨 Active Security Threats: {summary['risk_metrics']['active_threats']}")
    
    print("\n📋 Event Type Distribution:")
    for event_type, count in summary['event_types'].items():
        print(f"   • {event_type}: {count}")
    
    if summary['severity_distribution']:
        print("\n⚡ Severity Distribution:")
        for severity, count in summary['severity_distribution'].items():
            print(f"   • {severity.capitalize()}: {count}")
    
    print(f"\n💾 Reports saved to:")
    print(f"   • Test output: {test_file}")
    print(f"   • Final output: {final_file}")
    
    print("\n🎉 PROJECT SENTINEL MONITORING COMPLETED SUCCESSFULLY!")
    print("="*70)


def main():
    """Main entry point"""
    run_production_demo()


if __name__ == "__main__":
    main()