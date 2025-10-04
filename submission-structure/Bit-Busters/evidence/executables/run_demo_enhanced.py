#!/usr/bin/env python3
"""
Enhanced Demo Runner for Project Sentinel
Demonstrates AI-powered retail monitoring with intelligent analytics and predictive insights

Features Demonstrated:
1. Enhanced Scan Avoidance Detection with AI confidence scoring
2. Advanced Barcode Switching Detection with ML pattern recognition  
3. Smart Weight Discrepancy Detection with product category intelligence
4. Intelligent System Health Monitoring with predictive failure detection
5. Predictive Queue Forecasting with AI-powered congestion management
6. Theft Risk Scoring Engine with real-time threat assessment
7. Enhanced Inventory Intelligence with predictive modeling
8. Multi-Station Coordinated Fraud Detection with correlation analysis
9. Intelligent Staffing Optimization with dynamic workforce management
10. Sustainability & Efficiency Intelligence with green retail optimization
"""

import sys
import os
import time
import json
from datetime import datetime, timedelta

# Add the src directory to the path
current_file_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(os.path.dirname(current_file_dir)), 'src')
sys.path.insert(0, src_dir)

from data_processor import DataProcessor
from event_detector import EventDetector


class EnhancedSentinelDemo:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.event_detector = EventDetector(self.data_processor)
        self.demo_running = False

    def print_banner(self):
        """Print enhanced demo banner"""
        print("=" * 80)
        print("🛡️  PROJECT SENTINEL - ENHANCED AI RETAIL MONITORING DEMO")
        print("=" * 80)
        print("🤖 Featuring Advanced AI & Machine Learning Algorithms")
        print("📊 Real-time Analytics & Predictive Intelligence")
        print("🎯 Multi-layered Security & Fraud Detection")
        print("⚡ Intelligent Automation & Optimization")
        print("🌱 Sustainability & Efficiency Intelligence")
        print("=" * 80)
        print()

    def simulate_enhanced_scenarios(self):
        """Simulate comprehensive retail scenarios to demonstrate all AI features"""
        print("🎬 SIMULATING ENHANCED RETAIL SCENARIOS...")
        print("-" * 50)
        
        # Load and process historical data first
        self.data_processor.load_reference_data()
        self.data_processor.load_historical_data()
        
        scenarios = [
            self.scenario_1_scan_avoidance_ai,
            self.scenario_2_barcode_switching_ml,
            self.scenario_3_weight_discrepancy_intelligence,
            self.scenario_4_system_health_monitoring,
            self.scenario_5_predictive_queue_forecasting,
            self.scenario_6_theft_risk_scoring,
            self.scenario_7_inventory_intelligence,
            self.scenario_8_coordinated_fraud_detection,
            self.scenario_9_intelligent_staffing,
            self.scenario_10_sustainability_optimization
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🎭 SCENARIO {i}: {scenario.__name__.replace('_', ' ').upper()}")
            print("-" * 40)
            scenario()
            time.sleep(2)  # Brief pause between scenarios

    def scenario_1_scan_avoidance_ai(self):
        """AI-Enhanced Scan Avoidance Detection"""
        print("🔍 Testing AI-enhanced scan avoidance detection...")
        
        # Simulate RFID detection without corresponding POS scan
        rfid_events = [
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'SCO-003',
                'data': {
                    'location': 'IN_SCAN_AREA',
                    'sku': 'ELECTRONICS_HEADPHONES_001',
                    'customer_id': 'CUST_12345'
                }
            },
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'SCO-003', 
                'data': {
                    'location': 'IN_SCAN_AREA',
                    'sku': 'GROCERY_PREMIUM_COFFEE_002',
                    'customer_id': 'CUST_12345'
                }
            }
        ]
        
        # Add to processor
        for event in rfid_events:
            self.data_processor.rfid_data.append(event)
        
        # Run AI detection
        events = self.event_detector.detect_scan_avoidance()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   ⚠️ AI DETECTION: {data['event_name']}")
                print(f"      Station: {data['station_id']}")
                print(f"      Product: {data['SKU']}")
                print(f"      Confidence: {data['confidence']:.2f}")
                print(f"      Value at Risk: {data.get('product_value', 0):.2f} LKR")
                if 'risk_factors' in data:
                    print(f"      Risk Factors: {list(data['risk_factors'].keys())}")
        else:
            print("   ✅ No scan avoidance detected")

    def scenario_2_barcode_switching_ml(self):
        """Machine Learning Enhanced Barcode Switching Detection"""
        print("🧠 Testing ML-enhanced barcode switching detection...")
        
        # Simulate product recognition seeing expensive item
        recognition_event = {
            'timestamp': datetime.now().isoformat(),
            'station_id': 'SCO-001',
            'data': {
                'sku': 'ELECTRONICS_SMARTPHONE_001',  # Expensive item
                'customer_id': 'CUST_67890'
            }
        }
        
        # Simulate POS scanning cheaper item
        pos_event = {
            'timestamp': datetime.now().isoformat(),
            'station_id': 'SCO-001',
            'status': 'Active',
            'data': {
                'sku': 'HOUSEHOLD_BASIC_CLEANER_001',  # Cheap item
                'customer_id': 'CUST_67890',
                'price': 120.00
            }
        }
        
        self.data_processor.product_recognition_data.append(recognition_event)
        self.data_processor.pos_data.append(pos_event)
        
        # Run ML detection
        events = self.event_detector.detect_barcode_switching()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   🚨 ML DETECTION: {data['event_name']}")
                print(f"      Station: {data['station_id']}")
                print(f"      Recognized: {data['recognized_product']}")
                print(f"      Scanned: {data['scanned_product']}")
                print(f"      Price Difference: {data['price_difference']:.2f} LKR")
                print(f"      Detection Triggers: {data['detection_triggers']}")
                print(f"      Risk Score: {data['risk_score']:.2f}")
        else:
            print("   ✅ No barcode switching detected")

    def scenario_3_weight_discrepancy_intelligence(self):
        """Intelligent Weight Discrepancy Detection"""
        print("⚖️ Testing intelligent weight discrepancy detection...")
        
        # Simulate weight discrepancy at self-checkout
        pos_event = {
            'timestamp': datetime.now().isoformat(),
            'station_id': 'SCO-002',
            'status': 'Active',
            'data': {
                'sku': 'GROCERY_RICE_5KG_001',
                'customer_id': 'CUST_11111',
                'price': 850.00,
                'weight': 3.2  # Expected: 5.0kg, Actual: 3.2kg
            }
        }
        
        self.data_processor.pos_data.append(pos_event)
        
        # Run intelligent detection
        events = self.event_detector.detect_weight_discrepancies()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   ⚠️ INTELLIGENT DETECTION: {data['event_name']}")
                print(f"      Station: {data['station_id']}")
                print(f"      Product: {data['product_name']}")
                print(f"      Expected Weight: {data['expected_weight']}kg")
                print(f"      Actual Weight: {data['actual_weight']}kg")
                print(f"      Variance: {data['variance_percentage']:.1f}%")
                print(f"      Potential Fraud: {'Yes' if data.get('potential_fraud') else 'No'}")
        else:
            print("   ✅ No weight discrepancies detected")

    def scenario_4_system_health_monitoring(self):
        """Intelligent System Health Monitoring"""
        print("🔧 Testing intelligent system health monitoring...")
        
        # Simulate system performance issues
        error_events = [
            {
                'timestamp': (datetime.now() - timedelta(minutes=15)).isoformat(),
                'station_id': 'CHECKOUT-005',
                'status': 'System Error',
                'data': {'error_type': 'scanner_malfunction'}
            },
            {
                'timestamp': (datetime.now() - timedelta(minutes=12)).isoformat(),
                'station_id': 'CHECKOUT-005',
                'status': 'Read Error',
                'data': {'retry_count': 3}
            }
        ]
        
        for event in error_events:
            self.data_processor.pos_data.append(event)
        
        # Run health monitoring
        events = self.event_detector.detect_system_crashes()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   🚨 HEALTH ALERT: {data['event_name']}")
                print(f"      Station: {data['station_id']}")
                if 'error_rate' in data:
                    print(f"      Error Rate: {data['error_rate']:.1%}")
                    print(f"      Recommendation: {data.get('recommendation', 'Monitor')}")
                if 'estimated_loss' in data:
                    print(f"      Estimated Impact: {data['estimated_loss']:.2f} LKR")
        else:
            print("   ✅ All systems operating normally")

    def scenario_5_predictive_queue_forecasting(self):
        """Predictive Queue Forecasting"""
        print("📈 Testing predictive queue forecasting...")
        
        # Simulate queue congestion
        queue_events = [
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'CHECKOUT-001',
                'data': {
                    'customer_count': 8,
                    'average_dwell_time': 420  # 7 minutes
                }
            },
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'CHECKOUT-002',
                'data': {
                    'customer_count': 6,
                    'average_dwell_time': 380  # 6.3 minutes
                }
            }
        ]
        
        for event in queue_events:
            self.data_processor.queue_data.append(event)
        
        # Run predictive forecasting
        events = self.event_detector.detect_long_queues_and_forecast()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   📊 PREDICTION: {data['event_name']}")
                print(f"      Station: {data['station_id']}")
                if 'current_queue_length' in data:
                    print(f"      Current Queue: {data['current_queue_length']} customers")
                    print(f"      Wait Time: {data.get('average_wait_time', 0)/60:.1f} minutes")
                if 'predicted_peak_length' in data:
                    print(f"      Predicted Peak: {data['predicted_peak_length']} customers")
                print(f"      Customer Impact: {data.get('customer_satisfaction_impact', 'N/A')}")
        else:
            print("   ✅ Queue levels optimal")

    def scenario_6_theft_risk_scoring(self):
        """Theft Risk Scoring Engine"""
        print("🎯 Testing theft risk scoring engine...")
        
        # Build up customer risk profile through multiple suspicious events
        customer_id = 'CUST_SUSPICIOUS_001'
        
        # Add customer to risk profiles with suspicious behavior
        self.event_detector.customer_risk_profiles[customer_id] = {
            'risk_score': 0.85,  # High risk
            'transaction_history': [],
            'anomaly_count': 5,
            'visit_frequency': 12,
            'avg_basket_value': 1200.0,
            'station_preferences': {'SCO-001': 3, 'SCO-002': 2, 'CHECKOUT-001': 1},
            'time_patterns': {}
        }
        
        # Simulate recent high-value transactions
        recent_transactions = [
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'SCO-001',
                'data': {
                    'customer_id': customer_id,
                    'sku': 'ELECTRONICS_LAPTOP_001',
                    'price': 2500.00
                }
            },
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'SCO-002',
                'data': {
                    'customer_id': customer_id,
                    'sku': 'ELECTRONICS_TABLET_001',
                    'price': 1800.00
                }
            }
        ]
        
        for tx in recent_transactions:
            self.data_processor.pos_data.append(tx)
        
        # Run risk scoring
        events = self.event_detector.detect_theft_risk_patterns()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   🚨 RISK ALERT: {data['event_name']}")
                print(f"      Customer: {data['customer_id']}")
                print(f"      Risk Score: {data['risk_score']:.2f}")
                print(f"      Value at Risk: {data['total_value_at_risk']:.2f} LKR")
                print(f"      Stations Involved: {data['stations_involved']}")
                print(f"      Action Required: {data['recommended_action']}")
        else:
            print("   ✅ No high-risk patterns detected")

    def scenario_7_inventory_intelligence(self):
        """Enhanced Inventory Intelligence"""
        print("📦 Testing enhanced inventory intelligence...")
        
        # Simulate inventory discrepancy scenario
        # Add multiple sales for a product
        product_sku = 'ELECTRONICS_GAMING_CONTROLLER_001'
        
        sales_events = [
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'CHECKOUT-001',
                'data': {'sku': product_sku, 'price': 850.00}
            },
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'SCO-001',
                'data': {'sku': product_sku, 'price': 850.00}
            }
        ]
        
        # Add corresponding RFID detections (more than sales = potential theft)
        rfid_events = [
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'CHECKOUT-001',
                'data': {'sku': product_sku, 'location': 'SCAN_AREA'}
            },
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'SCO-001',
                'data': {'sku': product_sku, 'location': 'SCAN_AREA'}
            },
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'SCO-002',
                'data': {'sku': product_sku, 'location': 'SCAN_AREA'}
            },
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'SCO-003',
                'data': {'sku': product_sku, 'location': 'SCAN_AREA'}
            }
        ]
        
        for event in sales_events:
            self.data_processor.pos_data.append(event)
        for event in rfid_events:
            self.data_processor.rfid_data.append(event)
        
        # Run inventory intelligence
        events = self.event_detector.detect_inventory_discrepancies_enhanced()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   📊 INVENTORY ALERT: {data['event_name']}")
                print(f"      Product: {data['product_name']}")
                print(f"      Sales Recorded: {data['sales_recorded']}")
                print(f"      RFID Detections: {data['rfid_detections']}")
                print(f"      Risk Score: {data['risk_score']:.2f}")
                print(f"      Anomaly Indicators: {data['anomaly_indicators']}")
                if 'financial_impact' in data:
                    impact = data['financial_impact']
                    print(f"      Potential Loss: {impact.get('potential_theft_loss', 0):.2f} LKR")
        else:
            print("   ✅ Inventory levels consistent")

    def scenario_8_coordinated_fraud_detection(self):
        """Multi-Station Coordinated Fraud Detection"""
        print("🕸️ Testing coordinated fraud detection...")
        
        # Simulate coordinated activity across multiple stations
        coordinated_time = datetime.now()
        
        # High-value transactions happening simultaneously
        coordinated_events = [
            {
                'timestamp': coordinated_time.isoformat(),
                'station_id': 'SCO-001',
                'status': 'Active',
                'data': {
                    'customer_id': 'CUST_COORD_001',
                    'sku': 'ELECTRONICS_SMARTPHONE_001',
                    'price': 1500.00
                }
            },
            {
                'timestamp': coordinated_time.isoformat(),
                'station_id': 'SCO-002',
                'status': 'System Error',
                'data': {
                    'customer_id': 'CUST_COORD_002',
                    'sku': 'ELECTRONICS_LAPTOP_001',
                    'price': 2800.00
                }
            },
            {
                'timestamp': coordinated_time.isoformat(),
                'station_id': 'SCO-003',
                'status': 'Read Error',
                'data': {
                    'customer_id': 'CUST_COORD_003',
                    'sku': 'ELECTRONICS_TABLET_001',
                    'price': 1200.00
                }
            }
        ]
        
        for event in coordinated_events:
            self.data_processor.pos_data.append(event)
        
        # Run coordination detection
        events = self.event_detector.detect_multi_station_coordinated_fraud()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   🚨 COORDINATION ALERT: {data['event_name']}")
                print(f"      Stations Involved: {data['stations_involved']}")
                print(f"      Coordination Score: {data['overall_coordination_score']:.2f}")
                print(f"      Total Value at Risk: {data['total_value_at_risk']:.2f} LKR")
                print(f"      Indicators: {data['coordination_indicators']}")
                print(f"      Action Required: {data['recommended_action']}")
        else:
            print("   ✅ No coordinated activity detected")

    def scenario_9_intelligent_staffing(self):
        """Intelligent Staffing Optimization"""
        print("👥 Testing intelligent staffing optimization...")
        
        # Simulate staffing crisis scenario
        staffing_events = [
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'CHECKOUT-001',
                'data': {
                    'customer_count': 9,
                    'average_dwell_time': 650  # 10+ minutes
                }
            },
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'CHECKOUT-002',
                'data': {
                    'customer_count': 7,
                    'average_dwell_time': 580  # 9+ minutes
                }
            }
        ]
        
        for event in staffing_events:
            self.data_processor.queue_data.append(event)
        
        # Add transaction volume data
        for i in range(15):  # Simulate high transaction volume
            self.data_processor.pos_data.append({
                'timestamp': datetime.now().isoformat(),
                'station_id': 'CHECKOUT-001',
                'data': {'sku': f'ITEM_{i}', 'price': 100.0}
            })
        
        # Run staffing optimization
        events = self.event_detector.detect_intelligent_staffing_needs()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   👥 STAFFING ALERT: {data['event_name']}")
                if 'station_id' in data:
                    print(f"      Station: {data['station_id']}")
                if 'current_queue_length' in data:
                    print(f"      Queue Length: {data['current_queue_length']} customers")
                    print(f"      Wait Time: {data['current_wait_time']/60:.1f} minutes")
                    print(f"      Priority: {data['priority']}")
                    print(f"      Resolution Time: {data.get('estimated_resolution_time', 'N/A')}")
                if 'immediate_actions' in data:
                    print(f"      Immediate Actions: {data['immediate_actions']}")
                if 'affected_stations' in data:
                    print(f"      Affected Stations: {data['affected_stations']}")
                    print(f"      Total Queue Pressure: {data.get('total_queue_pressure', 'N/A')}")
        else:
            print("   ✅ Staffing levels optimal")

    def scenario_10_sustainability_optimization(self):
        """Sustainability & Efficiency Intelligence"""
        print("🌱 Testing sustainability optimization...")
        
        # Simulate low-utilization scenario
        # Create idle queue data
        idle_events = [
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'CHECKOUT-005',
                'data': {'customer_count': 0, 'average_dwell_time': 0}
            },
            {
                'timestamp': datetime.now().isoformat(),
                'station_id': 'SCO-004',
                'data': {'customer_count': 0, 'average_dwell_time': 0}
            }
        ]
        
        # Repeat to show consistent idle state
        for _ in range(12):  # 12 observations of idle state
            for event in idle_events:
                self.data_processor.queue_data.append(event.copy())
        
        # Add old last activity to trigger idle detection
        old_time = (datetime.now() - timedelta(minutes=15)).isoformat()
        self.data_processor.pos_data.append({
            'timestamp': old_time,
            'station_id': 'CHECKOUT-005',
            'data': {'sku': 'OLD_TRANSACTION', 'price': 50.0}
        })
        
        # Run sustainability optimization
        events = self.event_detector.detect_sustainability_opportunities()
        
        if events:
            for event in events:
                data = event['event_data']
                print(f"   🌱 SUSTAINABILITY: {data['event_name']}")
                if 'station_id' in data:
                    print(f"      Station: {data['station_id']}")
                    print(f"      Idle Duration: {data.get('idle_duration_minutes', 0):.1f} minutes")
                    print(f"      Energy Savings: {data.get('estimated_energy_savings', 0):.2f} LKR/hour")
                if 'underutilized_stations' in data:
                    print(f"      Underutilized Stations: {data['underutilized_stations']}")
                    print(f"      Potential Savings: {data.get('potential_energy_savings', 0):.2f} LKR/hour")
                    print(f"      Environmental Impact: {data.get('environmental_impact', 'N/A')}")
        else:
            print("   ✅ All stations optimally utilized")

    def run_comprehensive_detection(self):
        """Run comprehensive detection and generate intelligence report"""
        print("\n🔍 RUNNING COMPREHENSIVE AI DETECTION SUITE...")
        print("-" * 60)
        
        # Run all detection algorithms
        all_events = self.event_detector.detect_all_events()
        
        print(f"\n📊 DETECTION RESULTS:")
        print(f"   Total Events Detected: {len(all_events)}")
        
        # Display events by category
        event_categories = {}
        for event in all_events:
            category = event.get('event_data', {}).get('event_name', 'Unknown')
            event_categories[category] = event_categories.get(category, 0) + 1
        
        for category, count in event_categories.items():
            print(f"   • {category}: {count}")
        
        # Display recent events with details
        self.event_detector.display_recent_events()
        
        return all_events

    def generate_final_reports(self):
        """Generate comprehensive final reports"""
        print("\n📄 GENERATING FINAL REPORTS...")
        print("-" * 40)
        
        # Generate events.jsonl for test output
        test_output_file = "../output/test/events.jsonl"
        self.event_detector.save_events_to_file(test_output_file)
        
        # Generate events.jsonl for final output
        final_output_file = "../output/final/events.jsonl"
        self.event_detector.save_events_to_file(final_output_file)
        
        # Generate intelligence report
        intelligence_report_file = "../output/final/intelligence_report.json"
        self.event_detector.export_intelligence_report(intelligence_report_file)
        
        print(f"📋 Reports generated:")
        print(f"   • Test Events: {test_output_file}")
        print(f"   • Final Events: {final_output_file}")
        print(f"   • Intelligence Report: {intelligence_report_file}")

    def run_demo(self):
        """Run the complete enhanced demo"""
        self.print_banner()
        
        try:
            # Initialize system
            print("🚀 INITIALIZING ENHANCED SENTINEL SYSTEM...")
            self.data_processor.load_reference_data()
            self.data_processor.load_historical_data()
            print(f"✅ Loaded {len(self.data_processor.products_db)} products")
            print(f"✅ Loaded {len(self.data_processor.historical_transactions)} historical transactions")
            
            # Run enhanced scenarios
            self.simulate_enhanced_scenarios()
            
            # Run comprehensive detection
            detected_events = self.run_comprehensive_detection()
            
            # Generate reports
            self.generate_final_reports()
            
            # Show final summary
            print("\n" + "="*80)
            print("🎯 ENHANCED DEMO COMPLETION SUMMARY")
            print("="*80)
            
            summary = self.event_detector.get_detection_summary()
            print(f"🔍 Total Events Detected: {summary['total_events']}")
            print(f"🛡️ System Health Score: {summary['risk_metrics']['system_health_score']:.1f}/100")
            print(f"⚠️ High-Risk Customers: {summary['risk_metrics']['high_risk_customers']}")
            print(f"🚨 Active Threats: {summary['risk_metrics']['active_threats']}")
            print(f"📈 Detection Accuracy: {summary['operational_metrics']['detection_accuracy']:.1f}%")
            
            print("\n🏆 ENHANCED AI FEATURES DEMONSTRATED:")
            print("   ✅ AI-Enhanced Scan Avoidance Detection")
            print("   ✅ ML-Powered Barcode Switching Detection")
            print("   ✅ Intelligent Weight Discrepancy Analysis")
            print("   ✅ Predictive System Health Monitoring")
            print("   ✅ AI-Driven Queue Forecasting")
            print("   ✅ Real-time Theft Risk Scoring")
            print("   ✅ Advanced Inventory Intelligence")
            print("   ✅ Multi-Station Fraud Correlation")
            print("   ✅ Dynamic Staffing Optimization")
            print("   ✅ Sustainability Intelligence")
            
            print("\n🎉 ENHANCED PROJECT SENTINEL DEMO COMPLETED SUCCESSFULLY!")
            print("="*80)
            
        except Exception as e:
            print(f"\n❌ Demo Error: {e}")
            raise


def main():
    """Main demo execution"""
    demo = EnhancedSentinelDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()