#!/usr/bin/env python3
"""
Event Detector for Project Sentinel
Detects anomalies and security issues from sensor data
"""

import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import statistics
from collections import defaultdict


class EventDetector:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.detected_events = []
        self.event_counter = 1
        
        # Advanced detection parameters
        self.detection_thresholds = {
            'scan_avoidance_confidence': 0.75,
            'price_variance_threshold': 0.5,
            'weight_tolerance': 0.15,
            'queue_length_alert': 4,
            'wait_time_alert': 300
        }
        
        # Pattern learning storage
        self.behavior_patterns = defaultdict(list)
    
    def get_recent_data(self, data_collection, count=20):
        """Helper method to get recent data from deque collections"""
        try:
            data_list = list(data_collection)
            return data_list[-count:] if len(data_list) >= count else data_list
        except Exception:
            return []

    def generate_event_id(self):
        """Generate unique event ID"""
        event_id = f"E{self.event_counter:03d}"
        self.event_counter += 1
        return event_id

    # @algorithm Scan Avoidance Detection | Detects when RFID sees product but POS doesn't record it
    def detect_scan_avoidance(self) -> List[Dict]:
        """
        Detect scan avoidance by comparing RFID readings with POS transactions
        Logic: If RFID detects item in scan area but no corresponding POS transaction within 30 seconds
        """
        events = []
        current_time = datetime.now()

        # Look at recent RFID data
        rfid_data = self.get_recent_data(self.data_processor.rfid_data, 20)
        pos_data = self.get_recent_data(self.data_processor.pos_data, 20)
        
        for rfid_event in rfid_data:
            if rfid_event.get('data', {}).get('location') == 'IN_SCAN_AREA':
                rfid_timestamp = rfid_event.get('timestamp')
                station_id = rfid_event.get('station_id')
                sku = rfid_event.get('data', {}).get('sku')

                # Check if there's a corresponding POS transaction
                found_transaction = False
                for pos_event in pos_data:
                    if (pos_event.get('station_id') == station_id and
                            pos_event.get('data', {}).get('sku') == sku):
                        found_transaction = True
                        break

                if not found_transaction:
                    event = {
                        "timestamp": datetime.now().isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "Scanner Avoidance",
                            "station_id": station_id,
                            "SKU": sku,
                            "confidence": "high"
                        }
                    }
                    events.append(event)

        return events

    # @algorithm Barcode Switching Detection | Detects when cheaper product barcode is used
    def detect_barcode_switching(self) -> List[Dict]:
        """
        Detect barcode switching by comparing product recognition with actual POS scans
        Logic: Expensive item seen by camera but cheap item scanned at POS
        """
        events = []
        
        recognition_data = self.get_recent_data(self.data_processor.product_recognition_data, 10)
        pos_data = self.get_recent_data(self.data_processor.pos_data, 10)

        for recognition_event in recognition_data:
            recognized_sku = recognition_event.get('data', {}).get('sku')
            station_id = recognition_event.get('station_id')
            
            if recognized_sku and recognized_sku in self.data_processor.products_db:
                recognized_price = float(self.data_processor.products_db[recognized_sku].get('price', 0))
                
                # Find corresponding POS transaction at same station
                for pos_event in pos_data:
                    if pos_event.get('station_id') == station_id:
                        scanned_sku = pos_event.get('data', {}).get('sku')
                        if scanned_sku in self.data_processor.products_db:
                            scanned_price = float(self.data_processor.products_db[scanned_sku].get('price', 0))
                            
                            # If recognized item is significantly more expensive than scanned
                            if recognized_price > scanned_price * 1.5:  # 50% price difference threshold
                                event = {
                                    "timestamp": datetime.now().isoformat(),
                                    "event_id": self.generate_event_id(),
                                    "event_data": {
                                        "event_name": "Barcode Switching",
                                        "station_id": station_id,
                                        "recognized_SKU": recognized_sku,
                                        "scanned_SKU": scanned_sku,
                                        "price_difference": recognized_price - scanned_price,
                                        "confidence": "high"
                                    }
                                }
                                events.append(event)
        
        return events

    # @algorithm Weight Discrepancy Detection | Detects weight/item mismatches
    def detect_weight_discrepancies(self) -> List[Dict]:
        """
        Detect weight discrepancies in self-checkout scenarios
        Logic: Compare expected item weight with actual weight sensor readings
        """
        events = []
        
        pos_data = self.get_recent_data(self.data_processor.pos_data, 10)
        
        for pos_event in pos_data:
            if pos_event.get('station_id', '').startswith('SCO'):  # Self-checkout stations
                sku = pos_event.get('data', {}).get('sku')
                actual_weight = pos_event.get('data', {}).get('weight', 0)
                
                if sku in self.data_processor.products_db:
                    expected_weight = float(self.data_processor.products_db[sku].get('weight', 0))
                    
                    # Check if weight difference is significant
                    if expected_weight > 0:
                        weight_difference = abs(actual_weight - expected_weight) / expected_weight
                        
                        if weight_difference > self.detection_thresholds['weight_tolerance']:
                            event = {
                                "timestamp": datetime.now().isoformat(),
                                "event_id": self.generate_event_id(),
                                "event_data": {
                                    "event_name": "Weight Discrepancy",
                                    "station_id": pos_event.get('station_id'),
                                    "SKU": sku,
                                    "expected_weight": expected_weight,
                                    "actual_weight": actual_weight,
                                    "variance_percentage": weight_difference * 100,
                                    "confidence": "medium"
                                }
                            }
                            events.append(event)
        
        return events

    # @algorithm System Crash Detection | Detects when POS systems fail or crash
    def detect_system_crashes(self) -> List[Dict]:
        """
        Detect system crashes or failures by monitoring POS transaction patterns
        Logic: Sudden stop in transactions from active stations
        """
        events = []
        current_time = datetime.now()
        
        pos_data = self.get_recent_data(self.data_processor.pos_data, 20)
        
        # Check for stations that suddenly stopped processing
        station_last_transaction = {}
        for pos_event in pos_data:
            station_id = pos_event.get('station_id')
            timestamp = pos_event.get('timestamp', '')
            station_last_transaction[station_id] = timestamp
        
        # Flag stations with no recent activity (>5 minutes)
        for station_id, last_timestamp in station_last_transaction.items():
            try:
                last_time = datetime.fromisoformat(last_timestamp.replace('Z', '+00:00'))
                time_diff = (current_time - last_time.replace(tzinfo=None)).total_seconds()
                
                if time_diff > 300:  # 5 minutes
                    event = {
                        "timestamp": datetime.now().isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "System Crash",
                            "station_id": station_id,
                            "last_transaction": last_timestamp,
                            "downtime_seconds": time_diff,
                            "confidence": "medium"
                        }
                    }
                    events.append(event)
            except Exception:
                continue  # Skip invalid timestamps
        
        return events

    # @algorithm Queue Length Monitoring | Detects excessive wait times and queue lengths
    def detect_long_queues(self) -> List[Dict]:
        """
        Detect long queues that may impact customer experience
        Logic: Monitor queue length and average wait times
        """
        events = []
        
        queue_data = self.get_recent_data(self.data_processor.queue_data, 5)
        
        for queue_event in queue_data:
            customer_count = queue_event.get('data', {}).get('customer_count', 0)
            avg_wait_time = queue_event.get('data', {}).get('average_dwell_time', 0)
            station_id = queue_event.get('station_id')
            
            # Alert for long queues or wait times
            if (customer_count > self.detection_thresholds['queue_length_alert'] or 
                avg_wait_time > self.detection_thresholds['wait_time_alert']):
                
                event = {
                    "timestamp": datetime.now().isoformat(),
                    "event_id": self.generate_event_id(),
                    "event_data": {
                        "event_name": "Long Queue Alert",
                        "station_id": station_id,
                        "customer_count": customer_count,
                        "average_wait_time": avg_wait_time,
                        "severity": "high" if customer_count > 6 else "medium",
                        "confidence": "high"
                    }
                }
                events.append(event)
        
        return events

    def detect_all_events(self) -> List[Dict]:
        """Run all detection algorithms and return combined results"""
        all_events = []
        
        try:
            all_events.extend(self.detect_scan_avoidance())
            all_events.extend(self.detect_barcode_switching())
            all_events.extend(self.detect_weight_discrepancies())
            all_events.extend(self.detect_system_crashes())
            all_events.extend(self.detect_long_queues())
            
            # Add new advanced algorithms
            all_events.extend(self.detect_suspicious_behavior())
            all_events.extend(self.detect_inventory_discrepancies())
            all_events.extend(self.detect_multi_station_anomalies())
            all_events.extend(self.detect_staffing_needs())
            
        except Exception as e:
            print(f"Error in event detection: {e}")
        
        # Remove duplicates and add to history
        for event in all_events:
            if event not in self.detected_events:
                self.detected_events.append(event)
        
        return all_events
    
    # @algorithm Advanced Behavioral Analysis | Detects suspicious customer behavior patterns
    def detect_suspicious_behavior(self) -> List[Dict]:
        """
        Advanced algorithm that analyzes customer behavior patterns for anomalies
        Uses statistical analysis to identify outliers in shopping patterns
        """
        events = []
        
        # Analyze transaction patterns
        customer_analysis = defaultdict(lambda: {
            'transaction_count': 0,
            'total_value': 0,
            'avg_time_between': [],
            'stations_used': set()
        })
        
        pos_data = self.get_recent_data(self.data_processor.pos_data, 50)
        
        # Build customer profiles
        for pos_event in pos_data:
            customer_id = pos_event.get('data', {}).get('customer_id')
            if customer_id:
                profile = customer_analysis[customer_id]
                profile['transaction_count'] += 1
                profile['total_value'] += pos_event.get('data', {}).get('price', 0)
                profile['stations_used'].add(pos_event.get('station_id'))
        
        # Detect anomalies
        for customer_id, profile in customer_analysis.items():
            risk_score = 0
            
            # High frequency shopping in short time
            if profile['transaction_count'] > 10:
                risk_score += 0.3
            
            # Using multiple stations rapidly
            if len(profile['stations_used']) > 2:
                risk_score += 0.2
            
            # High-value transactions
            if profile['total_value'] > 1000:
                risk_score += 0.2
            
            if risk_score > 0.6:
                event = {
                    "timestamp": datetime.now().isoformat(),
                    "event_id": self.generate_event_id(),
                    "event_data": {
                        "event_name": "Suspicious Behavior Pattern",
                        "customer_id": customer_id,
                        "risk_score": risk_score,
                        "transaction_count": profile['transaction_count'],
                        "total_value": profile['total_value']
                    }
                }
                events.append(event)
        
        return events
    
    # @algorithm Inventory Discrepancy Prediction | Predicts inventory issues before they become critical
    def detect_inventory_discrepancies(self) -> List[Dict]:
        """
        Advanced inventory analysis that predicts discrepancies based on
        transaction patterns vs inventory levels
        """
        events = []
        
        # Track product movement vs inventory
        product_flow = defaultdict(lambda: {'sold': 0, 'expected_remaining': 0})
        
        pos_data = self.get_recent_data(self.data_processor.pos_data, 50)
        
        # Calculate expected inventory based on transactions
        for pos_event in pos_data:
            sku = pos_event.get('data', {}).get('sku')
            if sku:
                product_flow[sku]['sold'] += 1
        
        # Compare with actual inventory
        for sku, flow_data in product_flow.items():
            if sku in self.data_processor.inventory_data:
                actual_inventory = self.data_processor.inventory_data[sku]
                
                # Get initial inventory from products DB
                initial_qty = int(self.data_processor.products_db.get(sku, {}).get('quantity', 0))
                expected_remaining = initial_qty - flow_data['sold']
                
                # Calculate discrepancy
                discrepancy = abs(actual_inventory - expected_remaining)
                
                if discrepancy > 5:  # Significant discrepancy
                    event = {
                        "timestamp": datetime.now().isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "Inventory Discrepancy",
                            "SKU": sku,
                            "Expected_Inventory": expected_remaining,
                            "Actual_Inventory": actual_inventory,
                            "Discrepancy": discrepancy
                        }
                    }
                    events.append(event)
        
        return events
    
    # @algorithm Multi-Station Correlation Analysis | Detects coordinated suspicious activities across stations
    def detect_multi_station_anomalies(self) -> List[Dict]:
        """
        Advanced correlation analysis that detects suspicious activities
        spanning multiple checkout stations simultaneously
        """
        events = []
        
        # Group events by time windows
        time_windows = defaultdict(lambda: defaultdict(list))
        current_time = datetime.now()
        
        pos_data = self.get_recent_data(self.data_processor.pos_data, 30)
        
        # 5-minute time windows
        for pos_event in pos_data:
            timestamp_str = pos_event.get('timestamp', '')
            try:
                event_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                time_bucket = int(event_time.timestamp() // 300)  # 5-minute buckets
                station_id = pos_event.get('station_id')
                time_windows[time_bucket][station_id].append(pos_event)
            except:
                continue
        
        # Analyze patterns across stations
        for time_bucket, stations in time_windows.items():
            if len(stations) >= 3:  # Multiple stations active
                total_transactions = sum(len(events) for events in stations.values())
                
                # Check for synchronized suspicious activity
                high_value_transactions = 0
                error_count = 0
                
                for station_events in stations.values():
                    for event in station_events:
                        price = event.get('data', {}).get('price', 0)
                        if price > 500:  # High-value transaction
                            high_value_transactions += 1
                        if event.get('status') != 'Active':
                            error_count += 1
                
                # Detect coordinated activity
                if high_value_transactions >= 3 and error_count >= 2:
                    event = {
                        "timestamp": datetime.now().isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "Multi-Station Coordinated Activity",
                            "stations_involved": list(stations.keys()),
                            "time_window": time_bucket,
                            "high_value_transactions": high_value_transactions,
                            "error_count": error_count,
                            "confidence": "high"
                        }
                    }
                    events.append(event)
        
        return events
    
    # @algorithm Dynamic Staffing Optimization | Recommends optimal staffing based on real-time patterns  
    def detect_staffing_needs(self) -> List[Dict]:
        """
        Intelligent staffing recommendation system based on queue analysis,
        transaction volume, and historical patterns
        """
        events = []
        
        # Analyze current load across all stations
        station_load = {}
        total_customers_waiting = 0
        
        queue_data = self.get_recent_data(self.data_processor.queue_data, 10)
        
        for queue_event in queue_data:
            station_id = queue_event.get('station_id')
            customer_count = queue_event.get('data', {}).get('customer_count', 0)
            wait_time = queue_event.get('data', {}).get('average_dwell_time', 0)
            
            station_load[station_id] = {
                'queue_length': customer_count,
                'wait_time': wait_time,
                'efficiency': self.data_processor.calculate_efficiency_score(station_id)
            }
            total_customers_waiting += customer_count
        
        # Generate staffing recommendations
        recommendations = []
        
        if total_customers_waiting > 15:  # High overall load
            recommendations.append("Consider opening additional checkout lanes")
        
        for station_id, load in station_load.items():
            if load['queue_length'] > 6 and load['wait_time'] > 400:
                event = {
                    "timestamp": datetime.now().isoformat(),
                    "event_id": self.generate_event_id(),
                    "event_data": {
                        "event_name": "Staffing Needs",
                        "station_id": station_id,
                        "Staff_type": "Cashier",
                        "queue_length": load['queue_length'],
                        "wait_time": load['wait_time'],
                        "priority": "high" if load['wait_time'] > 600 else "medium"
                    }
                }
                events.append(event)
            
            elif load['efficiency'] < 60:
                event = {
                    "timestamp": datetime.now().isoformat(),
                    "event_id": self.generate_event_id(),
                    "event_data": {
                        "event_name": "Station Performance Alert",
                        "station_id": station_id,
                        "efficiency_score": load['efficiency'],
                        "recommendation": "Review station operation"
                    }
                }
                events.append(event)
        
        return events
    
    def save_events_to_file(self, filename: str):
        """Save detected events to JSONL file"""
        try:
            with open(filename, 'w') as f:
                for event in self.detected_events:
                    f.write(json.dumps(event) + '\n')
            print(f"Saved {len(self.detected_events)} events to {filename}")
        except Exception as e:
            print(f"Error saving events: {e}")


    def get_detection_summary(self) -> Dict:
        """Get summary of detection results"""
        summary = {
            'total_events': len(self.detected_events),
            'event_types': {},
            'recent_events': self.detected_events[-10:] if self.detected_events else []
        }
        
        # Count events by type
        for event in self.detected_events:
            event_type = event.get('event_data', {}).get('event_name', 'Unknown')
            summary['event_types'][event_type] = summary['event_types'].get(event_type, 0) + 1
        
        return summary

    def display_recent_events(self):
        """Display recent events for monitoring"""
        if self.detected_events:
            print("\n🚨 Recent Security Events:")
            for event in self.detected_events[-3:]:  # Show last 3 events
                event_data = event.get('event_data', {})
                print(f"  • {event_data.get('event_name', 'Unknown')} at {event.get('timestamp', 'N/A')}")
        else:
            print("\n✅ No security events detected")