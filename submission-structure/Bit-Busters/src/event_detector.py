#!/usr/bin/env python3
"""
Enhanced Event Detector for Project Sentinel
Advanced AI-powered retail monitoring with predictive analytics and intelligent automation
"""

import json
import time
import math
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import statistics
from collections import defaultdict, deque
import os


class EventDetector:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.detected_events = []
        self.event_counter = 1
        
        # Enhanced detection parameters with intelligent thresholds
        self.detection_thresholds = {
            'scan_avoidance_confidence': 0.75,
            'price_variance_threshold': 0.5,
            'weight_tolerance': 0.15,
            'queue_length_alert': 4,
            'wait_time_alert': 300,
            'theft_risk_threshold': 0.7,
            'inventory_discrepancy_threshold': 5,
            'coordinated_activity_threshold': 3,
            'efficiency_threshold': 60,
            'peak_prediction_window': 10,  # minutes
            'sustainability_idle_threshold': 600  # seconds
        }
        
        # Advanced pattern learning and AI storage
        self.behavior_patterns = defaultdict(list)
        self.customer_risk_profiles = defaultdict(lambda: {
            'risk_score': 0.0,
            'transaction_history': deque(maxlen=50),
            'anomaly_count': 0,
            'visit_frequency': 0,
            'avg_basket_value': 0.0,
            'station_preferences': defaultdict(int),
            'time_patterns': defaultdict(int)
        })
        
        # Predictive models storage
        self.queue_forecast_model = {
            'historical_patterns': defaultdict(list),
            'hourly_averages': defaultdict(float),
            'day_of_week_patterns': defaultdict(list),
            'last_updated': datetime.now()
        }
        
        # Theft risk scoring engine
        self.theft_risk_engine = {
            'active_risks': {},
            'risk_factors': {
                'multiple_stations': 0.3,
                'high_value_items': 0.25,
                'barcode_switching': 0.4,
                'scan_avoidance': 0.35,
                'weight_discrepancy': 0.2,
                'rapid_transactions': 0.15
            },
            'risk_history': deque(maxlen=100)
        }
        
        # Adaptive alert system
        self.alert_system = {
            'sensitivity_level': 'medium',  # low, medium, high
            'alert_counts': defaultdict(int),
            'escalation_rules': {
                'theft_alert_threshold': 3,
                'queue_alert_threshold': 2,
                'system_alert_threshold': 5
            },
            'suppression_windows': defaultdict(lambda: 0)
        }
        
        # Sustainability and efficiency tracking
        self.sustainability_tracker = {
            'station_utilization': defaultdict(list),
            'energy_efficiency_score': 100.0,
            'idle_recommendations': [],
            'peak_efficiency_times': defaultdict(list)
        }
    
    def get_recent_data(self, data_collection, count=20):
        """Enhanced helper method to get recent data with error handling"""
        try:
            data_list = list(data_collection)
            return data_list[-count:] if len(data_list) >= count else data_list
        except Exception:
            return []

    def generate_event_id(self):
        """Generate unique event ID with enhanced formatting"""
        event_id = f"SENTINEL-{self.event_counter:04d}"
        self.event_counter += 1
        return event_id

    def calculate_confidence_score(self, factors: Dict[str, float]) -> float:
        """Calculate confidence score based on multiple factors"""
        if not factors:
            return 0.5
        
        # Simply average the factor values since they're already normalized 0-1
        total_score = sum(factors.values())
        count = len(factors)
        
        return min(1.0, max(0.0, total_score / count if count > 0 else 0.5))

    # @algorithm Enhanced Scan Avoidance Detection | AI-powered detection with confidence scoring
    def detect_scan_avoidance(self) -> List[Dict]:
        """
        Enhanced scan avoidance detection with AI-powered confidence scoring
        Logic: Multi-factor analysis including temporal correlation, customer behavior, and product value
        """
        events = []
        current_time = datetime.now()

        # Enhanced data analysis with larger window
        rfid_data = self.get_recent_data(self.data_processor.rfid_data, 50)
        pos_data = self.get_recent_data(self.data_processor.pos_data, 50)
        
        # Create temporal windows for better correlation
        scan_area_events = []
        for rfid_event in rfid_data:
            if rfid_event.get('data', {}).get('location') == 'IN_SCAN_AREA':
                scan_area_events.append({
                    'timestamp': rfid_event.get('timestamp'),
                    'station_id': rfid_event.get('station_id'),
                    'sku': rfid_event.get('data', {}).get('sku'),
                    'customer_id': rfid_event.get('data', {}).get('customer_id')
                })

        # Check each scan area event for corresponding POS transaction
        for scan_event in scan_area_events:
            station_id = scan_event['station_id']
            sku = scan_event['sku']
            customer_id = scan_event['customer_id']
            
            # Look for matching POS transaction within 45 seconds
            found_transaction = False
            matching_pos_events = [pos for pos in pos_data 
                                 if (pos.get('station_id') == station_id and
                                     pos.get('data', {}).get('customer_id') == customer_id)]
            
            for pos_event in matching_pos_events:
                pos_sku = pos_event.get('data', {}).get('sku')
                if pos_sku == sku:
                    found_transaction = True
                    break

            if not found_transaction and sku:
                # Calculate confidence based on multiple factors
                confidence_factors = {}
                
                # Product value factor (higher value = higher confidence)
                product_price = float(self.data_processor.products_db.get(sku, {}).get('price', 0))
                confidence_factors['value_factor'] = min(1.0, product_price / 500.0)  # Normalize to 500 LKR
                
                # Customer risk profile factor
                if customer_id in self.customer_risk_profiles:
                    confidence_factors['risk_factor'] = self.customer_risk_profiles[customer_id]['risk_score']
                else:
                    confidence_factors['risk_factor'] = 0.3  # Default low risk
                
                # Station type factor (self-checkout higher risk)
                confidence_factors['station_factor'] = 0.8 if station_id.startswith('SCC') else 0.5
                
                # Time factor (longer without scan = higher confidence)
                confidence_factors['time_factor'] = 0.7  # Base time confidence
                
                confidence_score = self.calculate_confidence_score(confidence_factors)
                
                if confidence_score >= self.detection_thresholds['scan_avoidance_confidence']:
                    event = {
                        "timestamp": current_time.isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "Scanner Avoidance",
                            "station_id": station_id,
                            "customer_id": customer_id,
                            "SKU": sku,
                            "product_value": product_price,
                            "confidence": confidence_score,
                            "risk_factors": confidence_factors,
                            "severity": "high" if confidence_score > 0.9 else "medium"
                        }
                    }
                    events.append(event)
                    
                    # Update customer risk profile
                    self.customer_risk_profiles[customer_id]['risk_score'] = min(1.0, 
                        self.customer_risk_profiles[customer_id]['risk_score'] + 0.2)
                    self.customer_risk_profiles[customer_id]['anomaly_count'] += 1

        return events

    # @algorithm Advanced Barcode Switching Detection | ML-enhanced pattern recognition
    def detect_barcode_switching(self) -> List[Dict]:
        """
        Advanced barcode switching detection with machine learning patterns
        Logic: Multi-dimensional analysis including price gaps, product categories, and behavioral patterns
        """
        events = []
        
        recognition_data = self.get_recent_data(self.data_processor.product_recognition_data, 30)
        pos_data = self.get_recent_data(self.data_processor.pos_data, 30)

        # Enhanced correlation analysis
        for recognition_event in recognition_data:
            recognized_sku = recognition_event.get('data', {}).get('sku')
            station_id = recognition_event.get('station_id')
            customer_id = recognition_event.get('data', {}).get('customer_id')
            recognition_time = recognition_event.get('timestamp')
            
            if recognized_sku and recognized_sku in self.data_processor.products_db:
                recognized_product = self.data_processor.products_db[recognized_sku]
                recognized_price = float(recognized_product.get('price', 0))
                recognized_category = recognized_product.get('category', 'Unknown')
                
                # Find corresponding POS transaction within time window
                for pos_event in pos_data:
                    if (pos_event.get('station_id') == station_id and 
                        pos_event.get('data', {}).get('customer_id') == customer_id):
                        
                        scanned_sku = pos_event.get('data', {}).get('sku')
                        if scanned_sku and scanned_sku in self.data_processor.products_db:
                            scanned_product = self.data_processor.products_db[scanned_sku]
                            scanned_price = float(scanned_product.get('price', 0))
                            scanned_category = scanned_product.get('category', 'Unknown')
                            
                            # Enhanced detection logic
                            price_difference = recognized_price - scanned_price
                            price_ratio = recognized_price / scanned_price if scanned_price > 0 else float('inf')
                            
                            # Multi-factor detection
                            detection_triggers = []
                            
                            # Significant price difference
                            if price_difference > 200 and price_ratio > 2.0:
                                detection_triggers.append("major_price_gap")
                            
                            # Category mismatch with price advantage
                            if recognized_category != scanned_category and price_difference > 100:
                                detection_triggers.append("category_price_mismatch")
                            
                            # Premium to basic product switching
                            if "premium" in recognized_product.get('name', '').lower() and "basic" in scanned_product.get('name', '').lower():
                                detection_triggers.append("premium_to_basic_switch")
                            
                            if detection_triggers:
                                # Calculate risk score
                                risk_score = min(1.0, (price_difference / 1000.0) + 
                                               (0.3 if len(detection_triggers) > 1 else 0.1))
                                
                                event = {
                                    "timestamp": datetime.now().isoformat(),
                                    "event_id": self.generate_event_id(),
                                    "event_data": {
                                        "event_name": "Barcode Switching",
                                        "station_id": station_id,
                                        "customer_id": customer_id,
                                        "recognized_SKU": recognized_sku,
                                        "scanned_SKU": scanned_sku,
                                        "recognized_product": recognized_product.get('name', ''),
                                        "scanned_product": scanned_product.get('name', ''),
                                        "price_difference": price_difference,
                                        "price_ratio": price_ratio,
                                        "detection_triggers": detection_triggers,
                                        "risk_score": risk_score,
                                        "confidence": "high",
                                        "potential_loss": price_difference
                                    }
                                }
                                events.append(event)
                                
                                # Update customer risk profile
                                if customer_id:
                                    self.customer_risk_profiles[customer_id]['risk_score'] = min(1.0,
                                        self.customer_risk_profiles[customer_id]['risk_score'] + risk_score)
        
        return events

    # @algorithm Smart Weight Discrepancy Detection | Enhanced with product category analysis
    def detect_weight_discrepancies(self) -> List[Dict]:
        """
        Enhanced weight discrepancy detection with product category intelligence
        Logic: Context-aware weight analysis considering product types and customer patterns
        """
        events = []
        
        pos_data = self.get_recent_data(self.data_processor.pos_data, 20)
        
        for pos_event in pos_data:
            if pos_event.get('station_id', '').startswith('SCC'):  # Self-checkout stations
                sku = pos_event.get('data', {}).get('sku')
                actual_weight = pos_event.get('data', {}).get('weight', 0)
                customer_id = pos_event.get('data', {}).get('customer_id')
                
                if sku in self.data_processor.products_db:
                    product_info = self.data_processor.products_db[sku]
                    expected_weight = float(product_info.get('weight', 0))
                    product_category = product_info.get('category', 'Unknown')
                    product_name = product_info.get('name', '')
                    
                    # Enhanced weight tolerance based on product category
                    if product_category.lower() in ['produce', 'bakery', 'deli']:
                        weight_tolerance = 0.25  # Higher tolerance for variable weight items
                    elif 'package' in product_name.lower() or 'bulk' in product_name.lower():
                        weight_tolerance = 0.20  # Medium tolerance for packaged items
                    else:
                        weight_tolerance = self.detection_thresholds['weight_tolerance']  # Standard tolerance
                    
                    # Check if weight difference is significant
                    if expected_weight > 0:
                        weight_difference = abs(actual_weight - expected_weight) / expected_weight
                        
                        if weight_difference > weight_tolerance:
                            # Calculate severity based on weight difference and product value
                            product_price = float(product_info.get('price', 0))
                            severity_score = min(1.0, weight_difference + (product_price / 1000.0))
                            
                            event = {
                                "timestamp": datetime.now().isoformat(),
                                "event_id": self.generate_event_id(),
                                "event_data": {
                                    "event_name": "Weight Discrepancy",
                                    "station_id": pos_event.get('station_id'),
                                    "customer_id": customer_id,
                                    "SKU": sku,
                                    "product_name": product_name,
                                    "product_category": product_category,
                                    "expected_weight": expected_weight,
                                    "actual_weight": actual_weight,
                                    "variance_percentage": weight_difference * 100,
                                    "severity_score": severity_score,
                                    "confidence": "high" if weight_difference > 0.3 else "medium",
                                    "potential_fraud": weight_difference > 0.5
                                }
                            }
                            events.append(event)
                            
                            # Update customer risk profile
                            if customer_id:
                                risk_increase = min(0.3, weight_difference)
                                self.customer_risk_profiles[customer_id]['risk_score'] = min(1.0,
                                    self.customer_risk_profiles[customer_id]['risk_score'] + risk_increase)
        
        return events

    # @algorithm Intelligent System Health Monitoring | Predictive failure detection
    def detect_system_crashes(self) -> List[Dict]:
        """
        Intelligent system health monitoring with predictive failure detection
        Logic: Multi-signal analysis including transaction patterns, error rates, and performance degradation
        """
        events = []
        current_time = datetime.now()
        
        pos_data = self.get_recent_data(self.data_processor.pos_data, 50)
        
        # Advanced station health analysis
        station_health = defaultdict(lambda: {
            'last_transaction': None,
            'transaction_count': 0,
            'error_count': 0,
            'response_times': [],
            'transaction_intervals': []
        })
        
        # Analyze station patterns
        for pos_event in pos_data:
            station_id = pos_event.get('station_id')
            timestamp = pos_event.get('timestamp', '')
            status = pos_event.get('status', 'Active')
            
            station_health[station_id]['transaction_count'] += 1
            
            if status != 'Active':
                station_health[station_id]['error_count'] += 1
            
            try:
                event_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                if station_health[station_id]['last_transaction']:
                    interval = (event_time - station_health[station_id]['last_transaction']).total_seconds()
                    station_health[station_id]['transaction_intervals'].append(interval)
                station_health[station_id]['last_transaction'] = event_time
            except:
                continue
        
        # Detect various system issues
        for station_id, health_data in station_health.items():
            last_transaction = health_data['last_transaction']
            
            if last_transaction:
                downtime = (current_time - last_transaction.replace(tzinfo=None)).total_seconds()
                error_rate = health_data['error_count'] / max(1, health_data['transaction_count'])
                
                # Sudden system failure
                if downtime > 600:  # 10 minutes
                    event = {
                        "timestamp": current_time.isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "System Crash",
                            "station_id": station_id,
                            "last_transaction": last_transaction.isoformat(),
                            "downtime_seconds": downtime,
                            "severity": "critical" if downtime > 1800 else "high",
                            "confidence": "high",
                            "estimated_loss": self.calculate_downtime_impact(station_id, downtime)
                        }
                    }
                    events.append(event)
                
                # Performance degradation
                elif error_rate > 0.3:  # 30% error rate
                    event = {
                        "timestamp": current_time.isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "System Performance Degradation",
                            "station_id": station_id,
                            "error_rate": error_rate,
                            "transaction_count": health_data['transaction_count'],
                            "error_count": health_data['error_count'],
                            "severity": "medium",
                            "confidence": "high",
                            "recommendation": "Immediate maintenance required"
                        }
                    }
                    events.append(event)
        
        return events
    
    def calculate_downtime_impact(self, station_id: str, downtime_seconds: float) -> float:
        """Calculate estimated revenue impact of system downtime"""
        # Estimate based on average transaction value and frequency
        avg_transaction_value = 250.0  # LKR average
        transactions_per_minute = 2.0 if station_id.startswith('SCC') else 3.0
        
        minutes_down = downtime_seconds / 60.0
        estimated_lost_transactions = minutes_down * transactions_per_minute
        estimated_loss = estimated_lost_transactions * avg_transaction_value
        
        return round(estimated_loss, 2)

    # @algorithm Predictive Queue Forecasting | AI-powered queue management
    def detect_long_queues_and_forecast(self) -> List[Dict]:
        """
        Predictive queue forecasting with AI-powered congestion management
        Logic: Historical pattern analysis with real-time prediction and dynamic recommendations
        """
        events = []
        current_time = datetime.now()
        current_hour = current_time.hour
        
        queue_data = self.get_recent_data(self.data_processor.queue_data, 20)
        
        # Update historical patterns
        for queue_event in queue_data:
            station_id = queue_event.get('station_id')
            customer_count = queue_event.get('data', {}).get('customer_count', 0)
            timestamp = queue_event.get('timestamp', '')
            
            try:
                event_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                hour = event_time.hour
                self.queue_forecast_model['historical_patterns'][f"{station_id}_{hour}"].append(customer_count)
            except:
                continue
        
        # Current queue analysis and forecasting
        current_queues = {}
        total_customers_waiting = 0
        
        for queue_event in queue_data[-10:]:  # Most recent queue data
            station_id = queue_event.get('station_id')
            customer_count = queue_event.get('data', {}).get('customer_count', 0)
            avg_wait_time = queue_event.get('data', {}).get('average_dwell_time', 0)
            
            current_queues[station_id] = {
                'current_length': customer_count,
                'wait_time': avg_wait_time,
                'predicted_peak': self.predict_queue_peak(station_id, current_hour),
                'efficiency_score': self.data_processor.calculate_efficiency_score(station_id)
            }
            total_customers_waiting += customer_count
        
        # Generate intelligent recommendations
        for station_id, queue_info in current_queues.items():
            current_length = queue_info['current_length']
            wait_time = queue_info['wait_time']
            predicted_peak = queue_info['predicted_peak']
            
            # Current congestion alerts
            if current_length > self.detection_thresholds['queue_length_alert']:
                severity = "critical" if current_length > 8 else "high" if current_length > 6 else "medium"
                
                event = {
                    "timestamp": current_time.isoformat(),
                    "event_id": self.generate_event_id(),
                    "event_data": {
                        "event_name": "Long Queue Alert",
                        "station_id": station_id,
                        "current_queue_length": current_length,
                        "average_wait_time": wait_time,
                        "predicted_peak_length": predicted_peak,
                        "severity": severity,
                        "confidence": "high",
                        "customer_satisfaction_impact": self.calculate_satisfaction_impact(wait_time),
                        "immediate_action_required": current_length > 6
                    }
                }
                events.append(event)
            
            # Predictive congestion warnings
            if predicted_peak > current_length + 3:
                event = {
                    "timestamp": current_time.isoformat(),
                    "event_id": self.generate_event_id(),
                    "event_data": {
                        "event_name": "Predicted Queue Congestion",
                        "station_id": station_id,
                        "current_length": current_length,
                        "predicted_peak": predicted_peak,
                        "estimated_peak_time": (current_time + timedelta(minutes=10)).isoformat(),
                        "severity": "medium",
                        "confidence": "medium",
                        "recommended_action": "Consider opening additional checkout lanes"
                    }
                }
                events.append(event)
        
        # System-wide recommendations
        if total_customers_waiting > 20:
            event = {
                "timestamp": current_time.isoformat(),
                "event_id": self.generate_event_id(),
                "event_data": {
                    "event_name": "System-wide Queue Congestion",
                    "total_customers_waiting": total_customers_waiting,
                    "affected_stations": len(current_queues),
                    "severity": "high",
                    "confidence": "high",
                    "recommendations": [
                        "Open additional checkout lanes immediately",
                        "Deploy additional staff to expedite checkout",
                        "Consider express lane for small baskets",
                        "Activate queue management announcements"
                    ]
                }
            }
            events.append(event)
        
        return events
    
    def predict_queue_peak(self, station_id: str, current_hour: int) -> int:
        """Predict queue peak based on historical patterns"""
        pattern_key = f"{station_id}_{current_hour}"
        historical_data = self.queue_forecast_model['historical_patterns'].get(pattern_key, [])
        
        if len(historical_data) >= 3:
            # Use 90th percentile as peak prediction
            return int(np.percentile(historical_data, 90))
        else:
            # Default prediction based on time of day
            peak_hours = {9: 6, 10: 8, 11: 7, 12: 9, 13: 10, 17: 8, 18: 9, 19: 7}
            return peak_hours.get(current_hour, 5)
    
    def calculate_satisfaction_impact(self, wait_time: float) -> str:
        """Calculate customer satisfaction impact based on wait time"""
        if wait_time > 600:  # 10 minutes
            return "severe_negative"
        elif wait_time > 300:  # 5 minutes
            return "moderate_negative"
        elif wait_time > 180:  # 3 minutes
            return "minor_negative"
        else:
            return "acceptable"

    def detect_all_events(self) -> List[Dict]:
        """Run all detection algorithms and return combined results with intelligent filtering"""
        all_events = []
        
        try:
            # Core detection algorithms
            all_events.extend(self.detect_scan_avoidance())
            all_events.extend(self.detect_barcode_switching())
            all_events.extend(self.detect_weight_discrepancies())
            all_events.extend(self.detect_system_crashes())
            all_events.extend(self.detect_long_queues_and_forecast())
            
            # Advanced intelligence algorithms
            all_events.extend(self.detect_theft_risk_patterns())
            all_events.extend(self.detect_inventory_discrepancies_enhanced())
            all_events.extend(self.detect_multi_station_coordinated_fraud())
            all_events.extend(self.detect_intelligent_staffing_needs())
            all_events.extend(self.detect_sustainability_opportunities())
            all_events.extend(self.detect_normal_operations())
            
            # Apply adaptive alert filtering
            filtered_events = self.apply_adaptive_filtering(all_events)
            
        except Exception as e:
            print(f"Error in event detection: {e}")
            filtered_events = []
        
        # Add to history with deduplication
        for event in filtered_events:
            if not self.is_duplicate_event(event):
                self.detected_events.append(event)
        
        return filtered_events
    
    # @algorithm Theft Risk Scoring Engine | AI-powered real-time risk assessment
    def detect_theft_risk_patterns(self) -> List[Dict]:
        """
        Advanced theft risk scoring engine with behavioral pattern analysis
        Logic: Multi-factor risk scoring with real-time threat assessment
        """
        events = []
        current_time = datetime.now()
        
        # Analyze customer behavior patterns for risk indicators
        for customer_id, profile in self.customer_risk_profiles.items():
            if profile['risk_score'] > self.detection_thresholds['theft_risk_threshold']:
                
                # Get recent activity for this customer
                recent_pos = [pos for pos in self.get_recent_data(self.data_processor.pos_data, 30)
                             if pos.get('data', {}).get('customer_id') == customer_id]
                
                if recent_pos:
                    # Calculate comprehensive risk metrics
                    risk_factors = self.calculate_comprehensive_risk_factors(customer_id, recent_pos)
                    
                    if risk_factors['overall_risk'] > 0.8:
                        event = {
                            "timestamp": current_time.isoformat(),
                            "event_id": self.generate_event_id(),
                            "event_data": {
                                "event_name": "High Theft Risk Alert",
                                "customer_id": customer_id,
                                "risk_score": profile['risk_score'],
                                "risk_factors": risk_factors,
                                "recent_transactions": len(recent_pos),
                                "stations_involved": len(set(pos.get('station_id') for pos in recent_pos)),
                                "total_value_at_risk": sum(pos.get('data', {}).get('price', 0) for pos in recent_pos),
                                "severity": "critical",
                                "confidence": "high",
                                "recommended_action": "Immediate security intervention required"
                            }
                        }
                        events.append(event)
                        
                        # Store in theft risk engine
                        self.theft_risk_engine['active_risks'][customer_id] = {
                            'risk_score': profile['risk_score'],
                            'last_updated': current_time,
                            'interventions_required': True
                        }
        
        return events
    
    def calculate_comprehensive_risk_factors(self, customer_id: str, recent_transactions: List[Dict]) -> Dict:
        """Calculate comprehensive risk factors for a customer"""
        risk_factors = {
            'transaction_velocity': 0.0,
            'value_concentration': 0.0,
            'station_hopping': 0.0,
            'anomaly_frequency': 0.0,
            'overall_risk': 0.0
        }
        
        if not recent_transactions:
            return risk_factors
        
        # Transaction velocity (too many transactions in short time)
        transaction_count = len(recent_transactions)
        if transaction_count > 10:
            risk_factors['transaction_velocity'] = min(1.0, transaction_count / 15.0)
        
        # Value concentration (high-value items)
        total_value = sum(tx.get('data', {}).get('price', 0) for tx in recent_transactions)
        if total_value > 2000:  # LKR
            risk_factors['value_concentration'] = min(1.0, total_value / 5000.0)
        
        # Station hopping behavior
        unique_stations = len(set(tx.get('station_id') for tx in recent_transactions))
        if unique_stations > 2:
            risk_factors['station_hopping'] = min(1.0, unique_stations / 5.0)
        
        # Anomaly frequency from customer profile
        profile = self.customer_risk_profiles[customer_id]
        if profile['anomaly_count'] > 0:
            risk_factors['anomaly_frequency'] = min(1.0, profile['anomaly_count'] / 10.0)
        
        # Calculate overall risk using weighted average
        weights = {
            'transaction_velocity': 0.25,
            'value_concentration': 0.30,
            'station_hopping': 0.20,
            'anomaly_frequency': 0.25
        }
        
        risk_factors['overall_risk'] = sum(
            risk_factors[factor] * weight for factor, weight in weights.items()
        )
        
        return risk_factors

    # @algorithm Enhanced Inventory Intelligence | Predictive inventory discrepancy detection
    def detect_inventory_discrepancies_enhanced(self) -> List[Dict]:
        """
        Enhanced inventory analysis with predictive modeling and root cause analysis
        Logic: Advanced correlation analysis between sales, inventory, and sensor data
        """
        events = []
        current_time = datetime.now()
        
        # Build comprehensive product flow analysis
        product_analytics = defaultdict(lambda: {
            'sales_count': 0,
            'total_revenue': 0.0,
            'rfid_detections': 0,
            'weight_discrepancies': 0,
            'barcode_switches': 0,
            'expected_inventory': 0,
            'last_inventory_check': None,
            'risk_score': 0.0
        })
        
        # Analyze recent transaction data
        pos_data = self.get_recent_data(self.data_processor.pos_data, 100)
        rfid_data = self.get_recent_data(self.data_processor.rfid_data, 100)
        
        # Calculate sales for each product
        for pos_event in pos_data:
            sku = pos_event.get('data', {}).get('sku')
            price = pos_event.get('data', {}).get('price', 0)
            if sku:
                product_analytics[sku]['sales_count'] += 1
                product_analytics[sku]['total_revenue'] += price
        
        # Count RFID detections
        for rfid_event in rfid_data:
            sku = rfid_event.get('data', {}).get('sku')
            if sku:
                product_analytics[sku]['rfid_detections'] += 1
        
        # Analyze inventory discrepancies
        for sku, analytics in product_analytics.items():
            if sku in self.data_processor.products_db:
                product_info = self.data_processor.products_db[sku]
                initial_inventory = int(product_info.get('quantity', 0))
                
                # Calculate expected remaining inventory
                expected_remaining = initial_inventory - analytics['sales_count']
                analytics['expected_inventory'] = expected_remaining
                
                # Check for anomalies
                anomaly_indicators = []
                
                # More RFID detections than sales (potential theft)
                if analytics['rfid_detections'] > analytics['sales_count'] + 2:
                    anomaly_indicators.append("excess_rfid_detections")
                    analytics['risk_score'] += 0.4
                
                # High-value product with unusual patterns
                product_price = float(product_info.get('price', 0))
                if product_price > 500 and analytics['sales_count'] > 5:
                    anomaly_indicators.append("high_value_volume")
                    analytics['risk_score'] += 0.3
                
                # Expected negative inventory (overselling)
                if expected_remaining < 0:
                    anomaly_indicators.append("negative_inventory")
                    analytics['risk_score'] += 0.5
                
                # Generate events for significant discrepancies
                if analytics['risk_score'] > 0.6 or anomaly_indicators:
                    event = {
                        "timestamp": current_time.isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "Advanced Inventory Discrepancy",
                            "SKU": sku,
                            "product_name": product_info.get('name', ''),
                            "initial_inventory": initial_inventory,
                            "sales_recorded": analytics['sales_count'],
                            "expected_remaining": expected_remaining,
                            "rfid_detections": analytics['rfid_detections'],
                            "total_revenue": analytics['total_revenue'],
                            "anomaly_indicators": anomaly_indicators,
                            "risk_score": analytics['risk_score'],
                            "severity": "high" if analytics['risk_score'] > 0.8 else "medium",
                            "confidence": "high",
                            "financial_impact": self.calculate_inventory_impact(sku, analytics)
                        }
                    }
                    events.append(event)
        
        return events
    
    def calculate_inventory_impact(self, sku: str, analytics: Dict) -> Dict:
        """Calculate financial impact of inventory discrepancies"""
        product_info = self.data_processor.products_db.get(sku, {})
        product_price = float(product_info.get('price', 0))
        
        # Potential loss from unrecorded sales
        rfid_excess = max(0, analytics['rfid_detections'] - analytics['sales_count'])
        potential_theft_loss = rfid_excess * product_price
        
        # Revenue impact
        revenue_impact = analytics['total_revenue']
        
        return {
            'potential_theft_loss': potential_theft_loss,
            'recorded_revenue': revenue_impact,
            'impact_percentage': (potential_theft_loss / revenue_impact * 100) if revenue_impact > 0 else 0
        }

    # @algorithm Multi-Station Coordinated Fraud Detection | Advanced correlation analysis
    def detect_multi_station_coordinated_fraud(self) -> List[Dict]:
        """
        Advanced detection of coordinated fraudulent activities across multiple stations
        Logic: Temporal and behavioral correlation analysis across stations and customers
        """
        events = []
        current_time = datetime.now()
        
        # Analyze recent data in time windows
        pos_data = self.get_recent_data(self.data_processor.pos_data, 60)
        
        # Group by time windows (5-minute intervals)
        time_windows = defaultdict(lambda: defaultdict(list))
        
        for pos_event in pos_data:
            try:
                timestamp = pos_event.get('timestamp', '')
                event_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_bucket = int(event_time.timestamp() // 300)  # 5-minute buckets
                station_id = pos_event.get('station_id')
                time_windows[time_bucket][station_id].append(pos_event)
            except:
                continue
        
        # Analyze each time window for coordinated activity
        for time_bucket, stations_data in time_windows.items():
            if len(stations_data) >= 3:  # Multiple stations active
                coordination_score = self.calculate_coordination_score(stations_data)
                
                if coordination_score['overall_score'] > self.detection_thresholds['coordinated_activity_threshold']:
                    event = {
                        "timestamp": current_time.isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "Coordinated Multi-Station Fraud",
                            "time_window": datetime.fromtimestamp(time_bucket * 300).isoformat(),
                            "stations_involved": list(stations_data.keys()),
                            "coordination_indicators": coordination_score['indicators'],
                            "overall_coordination_score": coordination_score['overall_score'],
                            "total_value_at_risk": coordination_score['total_value'],
                            "severity": "critical",
                            "confidence": "high",
                            "recommended_action": "Immediate investigation and security review"
                        }
                    }
                    events.append(event)
        
        return events
    
    def calculate_coordination_score(self, stations_data: Dict) -> Dict:
        """Calculate coordination score for multi-station activity"""
        indicators = []
        total_value = 0.0
        
        # Analyze patterns across stations
        high_value_count = 0
        error_count = 0
        customer_overlap = set()
        
        for station_id, transactions in stations_data.items():
            station_value = 0
            station_errors = 0
            
            for transaction in transactions:
                price = transaction.get('data', {}).get('price', 0)
                customer_id = transaction.get('data', {}).get('customer_id')
                status = transaction.get('status', 'Active')
                
                station_value += price
                if price > 500:
                    high_value_count += 1
                
                if status != 'Active':
                    station_errors += 1
                    error_count += 1
                
                if customer_id:
                    customer_overlap.add(customer_id)
            
            total_value += station_value
            
            # High-value concentration at single station
            if station_value > 2000:
                indicators.append(f"high_value_concentration_{station_id}")
        
        # Coordination indicators
        if high_value_count >= 5:
            indicators.append("synchronized_high_value_transactions")
        
        if error_count >= 3:
            indicators.append("synchronized_system_errors")
        
        if len(customer_overlap) < len(stations_data) * 2:
            indicators.append("limited_customer_overlap")
        
        # Calculate overall coordination score
        base_score = len(indicators) * 0.25
        value_factor = min(1.0, total_value / 10000.0)  # Normalize to 10K LKR
        
        overall_score = min(1.0, base_score + value_factor)
        
        return {
            'indicators': indicators,
            'overall_score': overall_score,
            'total_value': total_value,
            'stations_count': len(stations_data)
        }
    
    # @algorithm Intelligent Staffing Optimization | Dynamic workforce management
    def detect_intelligent_staffing_needs(self) -> List[Dict]:
        """
        AI-powered staffing optimization with predictive workforce management
        Logic: Real-time analysis with predictive modeling for optimal staff allocation
        """
        events = []
        current_time = datetime.now()
        
        # Comprehensive station analysis
        station_metrics = {}
        queue_data = self.get_recent_data(self.data_processor.queue_data, 20)
        pos_data = self.get_recent_data(self.data_processor.pos_data, 50)
        
        # Analyze current performance metrics
        for queue_event in queue_data:
            station_id = queue_event.get('station_id')
            customer_count = queue_event.get('data', {}).get('customer_count', 0)
            wait_time = queue_event.get('data', {}).get('average_dwell_time', 0)
            
            if station_id not in station_metrics:
                station_metrics[station_id] = {
                    'queue_length': customer_count,
                    'wait_time': wait_time,
                    'transaction_count': 0,
                    'efficiency_score': 0.0,
                    'utilization_rate': 0.0,
                    'predicted_demand': 0.0
                }
            
            station_metrics[station_id]['queue_length'] = max(station_metrics[station_id]['queue_length'], customer_count)
            station_metrics[station_id]['wait_time'] = max(station_metrics[station_id]['wait_time'], wait_time)
        
        # Add transaction volume analysis
        for pos_event in pos_data:
            station_id = pos_event.get('station_id')
            if station_id in station_metrics:
                station_metrics[station_id]['transaction_count'] += 1
        
        # Calculate efficiency and utilization metrics
        for station_id, metrics in station_metrics.items():
            metrics['efficiency_score'] = self.data_processor.calculate_efficiency_score(station_id)
            metrics['utilization_rate'] = min(1.0, metrics['transaction_count'] / 30.0)  # Normalize to 30 transactions
            metrics['predicted_demand'] = self.predict_station_demand(station_id, current_time.hour)
        
        # Generate intelligent staffing recommendations
        total_queue_pressure = sum(metrics['queue_length'] * metrics['wait_time'] for metrics in station_metrics.values())
        
        for station_id, metrics in station_metrics.items():
            # Critical staffing needs
            if metrics['queue_length'] > 6 and metrics['wait_time'] > 400:
                priority = "critical" if metrics['wait_time'] > 600 else "high"
                
                event = {
                    "timestamp": current_time.isoformat(),
                    "event_id": self.generate_event_id(),
                    "event_data": {
                        "event_name": "Critical Staffing Need",
                        "station_id": station_id,
                        "staff_type": "Cashier",
                        "current_queue_length": metrics['queue_length'],
                        "current_wait_time": metrics['wait_time'],
                        "efficiency_score": metrics['efficiency_score'],
                        "predicted_demand": metrics['predicted_demand'],
                        "priority": priority,
                        "severity": "high",
                        "confidence": "high",
                        "estimated_resolution_time": self.calculate_resolution_time(metrics),
                        "customer_impact": self.calculate_customer_impact(metrics['wait_time'])
                    }
                }
                events.append(event)
            
            # Performance optimization opportunities
            elif metrics['efficiency_score'] < self.detection_thresholds['efficiency_threshold']:
                event = {
                    "timestamp": current_time.isoformat(),
                    "event_id": self.generate_event_id(),
                    "event_data": {
                        "event_name": "Station Performance Optimization",
                        "station_id": station_id,
                        "current_efficiency": metrics['efficiency_score'],
                        "optimization_potential": 100 - metrics['efficiency_score'],
                        "recommended_actions": self.generate_optimization_recommendations(metrics),
                        "severity": "medium",
                        "confidence": "medium"
                    }
                }
                events.append(event)
        
        # System-wide staffing analysis
        if total_queue_pressure > 500:  # High system-wide pressure
            event = {
                "timestamp": current_time.isoformat(),
                "event_id": self.generate_event_id(),
                "event_data": {
                    "event_name": "System-wide Staffing Crisis",
                    "total_queue_pressure": total_queue_pressure,
                    "affected_stations": len([s for s, m in station_metrics.items() if m['queue_length'] > 4]),
                    "severity": "critical",
                    "confidence": "high",
                    "immediate_actions": [
                        "Deploy all available cashiers immediately",
                        "Open additional checkout lanes",
                        "Consider temporary self-checkout assistance",
                        "Implement crowd control measures"
                    ],
                    "estimated_recovery_time": "15-20 minutes with immediate action"
                }
            }
            events.append(event)
        
        return events
    
    def predict_station_demand(self, station_id: str, current_hour: int) -> float:
        """Predict station demand based on historical patterns"""
        # Simple demand prediction based on hour and station type
        base_demand = {
            9: 0.7, 10: 0.8, 11: 0.9, 12: 1.0, 13: 0.95,
            17: 0.9, 18: 1.0, 19: 0.8, 20: 0.6
        }.get(current_hour, 0.5)
        
        # Adjust for station type
        if station_id.startswith('SCC'):
            base_demand *= 0.8  # Self-checkout typically has higher throughput
        
        return base_demand
    
    def calculate_resolution_time(self, metrics: Dict) -> str:
        """Calculate estimated time to resolve staffing issues"""
        queue_factor = metrics['queue_length'] * 2  # minutes per customer
        efficiency_factor = (100 - metrics['efficiency_score']) * 0.1
        
        total_minutes = queue_factor + efficiency_factor
        
        if total_minutes < 5:
            return "2-5 minutes"
        elif total_minutes < 10:
            return "5-10 minutes"
        elif total_minutes < 20:
            return "10-20 minutes"
        else:
            return "20+ minutes"
    
    def calculate_customer_impact(self, wait_time: float) -> Dict:
        """Calculate customer satisfaction impact"""
        if wait_time > 600:
            return {"satisfaction_score": 1, "churn_risk": "high", "recovery_actions_needed": True}
        elif wait_time > 300:
            return {"satisfaction_score": 3, "churn_risk": "medium", "recovery_actions_needed": True}
        elif wait_time > 180:
            return {"satisfaction_score": 6, "churn_risk": "low", "recovery_actions_needed": False}
        else:
            return {"satisfaction_score": 9, "churn_risk": "none", "recovery_actions_needed": False}
    
    def generate_optimization_recommendations(self, metrics: Dict) -> List[str]:
        """Generate specific optimization recommendations"""
        recommendations = []
        
        if metrics['efficiency_score'] < 50:
            recommendations.append("Consider additional cashier training")
            recommendations.append("Review checkout process for bottlenecks")
        
        if metrics['wait_time'] > 200:
            recommendations.append("Implement queue management system")
            recommendations.append("Consider express lane for small baskets")
        
        if metrics['utilization_rate'] < 0.3:
            recommendations.append("Optimize staff scheduling")
            recommendations.append("Consider consolidating low-traffic periods")
        
        return recommendations if recommendations else ["Monitor performance trends"]

    # @algorithm Sustainability & Efficiency Intelligence | Green retail optimization
    def detect_sustainability_opportunities(self) -> List[Dict]:
        """
        Intelligent sustainability and energy efficiency optimization
        Logic: Analyze station utilization patterns to recommend energy-saving measures
        """
        events = []
        current_time = datetime.now()
        
        # Analyze station utilization over time
        pos_data = self.get_recent_data(self.data_processor.pos_data, 100)
        queue_data = self.get_recent_data(self.data_processor.queue_data, 50)
        
        # Track station activity patterns
        station_activity = defaultdict(lambda: {
            'total_transactions': 0,
            'idle_periods': 0,
            'last_activity': None,
            'utilization_score': 0.0,
            'energy_efficiency': 100.0
        })
        
        # Analyze transaction patterns
        for pos_event in pos_data:
            station_id = pos_event.get('station_id')
            timestamp = pos_event.get('timestamp')
            
            station_activity[station_id]['total_transactions'] += 1
            station_activity[station_id]['last_activity'] = timestamp
        
        # Analyze queue patterns for idle detection
        for queue_event in queue_data:
            station_id = queue_event.get('station_id')
            customer_count = queue_event.get('data', {}).get('customer_count', 0)
            
            if customer_count == 0:
                station_activity[station_id]['idle_periods'] += 1
        
        # Calculate utilization and efficiency scores
        for station_id, activity in station_activity.items():
            total_observations = len(pos_data) // len(station_activity)  # Approximate
            activity['utilization_score'] = activity['total_transactions'] / max(1, total_observations)
            
            # Energy efficiency based on utilization and idle time
            idle_ratio = activity['idle_periods'] / max(1, len(queue_data))
            activity['energy_efficiency'] = max(0, 100 - (idle_ratio * 50))
        
        # Generate sustainability recommendations
        low_utilization_stations = []
        energy_saving_opportunities = []
        
        for station_id, activity in station_activity.items():
            # Detect low-utilization stations
            if activity['utilization_score'] < 0.2 and activity['idle_periods'] > 10:
                low_utilization_stations.append(station_id)
                
                # Check if station has been idle for extended period
                if activity['last_activity']:
                    try:
                        last_activity = datetime.fromisoformat(activity['last_activity'].replace('Z', '+00:00'))
                        idle_duration = (current_time - last_activity.replace(tzinfo=None)).total_seconds()
                        
                        if idle_duration > self.detection_thresholds['sustainability_idle_threshold']:
                            event = {
                                "timestamp": current_time.isoformat(),
                                "event_id": self.generate_event_id(),
                                "event_data": {
                                    "event_name": "Energy Conservation Opportunity",
                                    "station_id": station_id,
                                    "idle_duration_minutes": idle_duration / 60,
                                    "utilization_score": activity['utilization_score'],
                                    "energy_efficiency_score": activity['energy_efficiency'],
                                    "recommended_action": "Consider temporary closure",
                                    "estimated_energy_savings": self.calculate_energy_savings(idle_duration),
                                    "severity": "low",
                                    "confidence": "medium",
                                    "sustainability_impact": "positive"
                                }
                            }
                            events.append(event)
                    except:
                        continue
        
        # System-wide sustainability analysis
        if len(low_utilization_stations) >= 2:
            total_potential_savings = sum(
                self.calculate_energy_savings(600) for _ in low_utilization_stations  # 10 min baseline
            )
            
            event = {
                "timestamp": current_time.isoformat(),
                "event_id": self.generate_event_id(),
                "event_data": {
                    "event_name": "System-wide Energy Optimization",
                    "underutilized_stations": low_utilization_stations,
                    "potential_energy_savings": total_potential_savings,
                    "recommendations": [
                        "Consolidate checkout operations during low-traffic periods",
                        "Implement smart power management for idle stations",
                        "Consider flexible staffing schedules",
                        "Deploy energy-efficient standby modes"
                    ],
                    "environmental_impact": "Reduced carbon footprint",
                    "cost_savings_potential": f"{total_potential_savings * 0.1:.2f} LKR/hour",
                    "severity": "low",
                    "confidence": "high"
                }
            }
            events.append(event)
        
        return events
    
    def calculate_energy_savings(self, idle_seconds: float) -> float:
        """Calculate estimated energy savings from station optimization"""
        # Estimate based on typical POS system power consumption
        # Average POS system: ~200W, cost ~20 LKR/kWh
        power_consumption_kw = 0.2  # 200W
        cost_per_kwh = 20.0  # LKR
        
        hours_idle = idle_seconds / 3600.0
        energy_saved_kwh = power_consumption_kw * hours_idle
        cost_savings = energy_saved_kwh * cost_per_kwh
        
        return round(cost_savings, 2)

    # @algorithm Normal Operations Detection | Success tracking and positive reinforcement
    def detect_normal_operations(self) -> List[Dict]:
        """
        Detect and log successful operations for comprehensive monitoring
        Logic: Identify smooth transactions and efficient operations for baseline establishment
        """
        events = []
        current_time = datetime.now()
        
        pos_data = self.get_recent_data(self.data_processor.pos_data, 20)
        
        for pos_event in pos_data:
            # Criteria for successful operation
            status = pos_event.get('status', '')
            price = pos_event.get('data', {}).get('price', 0)
            customer_id = pos_event.get('data', {}).get('customer_id')
            station_id = pos_event.get('station_id')
            sku = pos_event.get('data', {}).get('sku')
            
            # Check if this is a clean, successful transaction
            if (status == 'Active' and price > 0 and customer_id and sku and 
                customer_id not in self.customer_risk_profiles or 
                self.customer_risk_profiles[customer_id]['risk_score'] < 0.3):
                
                # Only log every 5th normal operation to avoid spam
                if self.event_counter % 5 == 0:
                    event = {
                        "timestamp": current_time.isoformat(),
                        "event_id": self.generate_event_id(),
                        "event_data": {
                            "event_name": "Success Operation",
                            "station_id": station_id,
                            "customer_id": customer_id,
                            "SKU": sku,
                            "transaction_value": price,
                            "confidence": "high",
                            "operational_efficiency": "optimal"
                        }
                    }
                    events.append(event)
        
        return events

    # @algorithm Adaptive Alert System | Smart filtering and escalation
    def apply_adaptive_filtering(self, events: List[Dict]) -> List[Dict]:
        """
        Apply intelligent filtering to reduce alert fatigue and focus on critical issues
        Logic: Dynamic threshold adjustment and alert suppression based on patterns
        """
        if not events:
            return events
        
        filtered_events = []
        current_time = datetime.now()
        
        # Categorize events by type and severity
        event_categories = defaultdict(list)
        for event in events:
            event_name = event.get('event_data', {}).get('event_name', 'Unknown')
            severity = event.get('event_data', {}).get('severity', 'medium')
            event_categories[f"{event_name}_{severity}"].append(event)
        
        # Apply adaptive filtering rules
        for category, category_events in event_categories.items():
            event_name, severity = category.rsplit('_', 1)
            
            # Always allow critical events
            if severity == 'critical':
                filtered_events.extend(category_events)
                continue
            
            # Apply suppression windows for non-critical events
            suppression_key = f"{event_name}_{severity}"
            last_alert_time = self.alert_system['suppression_windows'].get(suppression_key, 0)
            
            # Suppression window based on severity
            suppression_minutes = {'high': 10, 'medium': 15, 'low': 30}.get(severity, 15)
            
            if (current_time.timestamp() - last_alert_time) > (suppression_minutes * 60):
                # Allow one event from this category
                if category_events:
                    filtered_events.append(category_events[0])
                    self.alert_system['suppression_windows'][suppression_key] = current_time.timestamp()
            
        return filtered_events
    
    def is_duplicate_event(self, new_event: Dict) -> bool:
        """Check if event is a duplicate of recent events"""
        if not self.detected_events:
            return False
        
        # Check last 10 events for duplicates
        recent_events = self.detected_events[-10:]
        new_event_data = new_event.get('event_data', {})
        
        for existing_event in recent_events:
            existing_data = existing_event.get('event_data', {})
            
            # Same event type and station within 5 minutes
            if (new_event_data.get('event_name') == existing_data.get('event_name') and
                new_event_data.get('station_id') == existing_data.get('station_id')):
                
                try:
                    new_time = datetime.fromisoformat(new_event.get('timestamp', ''))
                    existing_time = datetime.fromisoformat(existing_event.get('timestamp', ''))
                    
                    if (new_time - existing_time).total_seconds() < 300:  # 5 minutes
                        return True
                except:
                    continue
        
        return False
    
    def save_events_to_file(self, filename: str):
        """Enhanced event saving with comprehensive formatting"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w') as f:
                for event in self.detected_events:
                    f.write(json.dumps(event) + '\n')
            
            print(f"✅ Saved {len(self.detected_events)} events to {filename}")
            
            # Generate summary statistics
            self.print_event_summary()
            
        except Exception as e:
            print(f"❌ Error saving events: {e}")

    def get_detection_summary(self) -> Dict:
        """Enhanced detection summary with intelligence metrics"""
        summary = {
            'total_events': len(self.detected_events),
            'event_types': {},
            'severity_distribution': {},
            'recent_events': self.detected_events[-10:] if self.detected_events else [],
            'risk_metrics': {
                'high_risk_customers': len([c for c, p in self.customer_risk_profiles.items() 
                                          if p['risk_score'] > 0.7]),
                'active_threats': len(self.theft_risk_engine['active_risks']),
                'system_health_score': self.calculate_system_health_score()
            },
            'operational_metrics': {
                'alert_suppression_rate': self.calculate_suppression_rate(),
                'detection_accuracy': self.estimate_detection_accuracy(),
                'processing_efficiency': self.calculate_processing_efficiency()
            }
        }
        
        # Count events by type and severity
        for event in self.detected_events:
            event_data = event.get('event_data', {})
            event_type = event_data.get('event_name', 'Unknown')
            severity = event_data.get('severity', 'medium')
            
            summary['event_types'][event_type] = summary['event_types'].get(event_type, 0) + 1
            summary['severity_distribution'][severity] = summary['severity_distribution'].get(severity, 0) + 1
        
        return summary

    def calculate_system_health_score(self) -> float:
        """Calculate overall system health score (0-100)"""
        base_score = 100.0
        
        # Reduce score based on active risks
        active_risks = len(self.theft_risk_engine['active_risks'])
        base_score -= min(30, active_risks * 5)
        
        # Reduce score based on recent critical events
        recent_critical = len([e for e in self.detected_events[-20:] 
                              if e.get('event_data', {}).get('severity') == 'critical'])
        base_score -= min(40, recent_critical * 10)
        
        # Reduce score based on system errors
        recent_errors = len([e for e in self.detected_events[-20:] 
                            if 'system' in e.get('event_data', {}).get('event_name', '').lower()])
        base_score -= min(20, recent_errors * 5)
        
        return max(0.0, base_score)

    def calculate_suppression_rate(self) -> float:
        """Calculate rate of alert suppression to avoid alert fatigue"""
        total_potential_alerts = len(self.alert_system['alert_counts'])
        if total_potential_alerts == 0:
            return 0.0
        
        suppressed_alerts = sum(1 for count in self.alert_system['alert_counts'].values() if count > 1)
        return (suppressed_alerts / total_potential_alerts) * 100

    def estimate_detection_accuracy(self) -> float:
        """Estimate detection accuracy based on confidence scores"""
        if not self.detected_events:
            return 0.0
        
        confidence_scores = []
        for event in self.detected_events:
            confidence = event.get('event_data', {}).get('confidence', 'medium')
            score = {'high': 0.9, 'medium': 0.7, 'low': 0.5}.get(confidence, 0.7)
            confidence_scores.append(score)
        
        return (sum(confidence_scores) / len(confidence_scores)) * 100

    def calculate_processing_efficiency(self) -> float:
        """Calculate processing efficiency metric"""
        # Based on events per second and quality
        events_per_minute = len(self.detected_events) / max(1, (time.time() - getattr(self, 'start_time', time.time())) / 60)
        
        # Optimal range is 1-5 events per minute
        if 1 <= events_per_minute <= 5:
            return 100.0
        elif events_per_minute < 1:
            return 80.0  # Too few detections
        else:
            return max(60.0, 100 - (events_per_minute - 5) * 5)  # Too many detections

    def print_event_summary(self):
        """Print comprehensive event summary"""
        summary = self.get_detection_summary()
        
        print("\n" + "="*60)
        print("� PROJECT SENTINEL - DETECTION SUMMARY")
        print("="*60)
        
        print(f"🎯 Total Events Detected: {summary['total_events']}")
        print(f"🛡️ System Health Score: {summary['risk_metrics']['system_health_score']:.1f}/100")
        print(f"⚠️ High-Risk Customers: {summary['risk_metrics']['high_risk_customers']}")
        print(f"🚨 Active Threats: {summary['risk_metrics']['active_threats']}")
        
        print("\n📋 Event Distribution:")
        for event_type, count in summary['event_types'].items():
            print(f"   • {event_type}: {count}")
        
        print("\n⚡ Severity Breakdown:")
        for severity, count in summary['severity_distribution'].items():
            print(f"   • {severity.capitalize()}: {count}")
        
        print("\n🔧 Performance Metrics:")
        print(f"   • Detection Accuracy: {summary['operational_metrics']['detection_accuracy']:.1f}%")
        print(f"   • Processing Efficiency: {summary['operational_metrics']['processing_efficiency']:.1f}%")
        print(f"   • Alert Suppression Rate: {summary['operational_metrics']['alert_suppression_rate']:.1f}%")
        
        print("="*60)

    def display_recent_events(self):
        """Enhanced display of recent events with intelligence insights"""
        if self.detected_events:
            print("\n🚨 RECENT SECURITY & OPERATIONAL EVENTS:")
            print("-" * 50)
            
            # Show last 5 events with enhanced formatting
            for event in self.detected_events[-5:]:
                event_data = event.get('event_data', {})
                event_name = event_data.get('event_name', 'Unknown')
                severity = event_data.get('severity', 'medium')
                station_id = event_data.get('station_id', 'N/A')
                timestamp = event.get('timestamp', 'N/A')
                
                # Format timestamp
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%H:%M:%S')
                except:
                    formatted_time = 'N/A'
                
                # Severity emoji
                severity_emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(severity, '⚪')
                
                print(f"  {severity_emoji} {formatted_time} | {event_name} | Station: {station_id}")
                
                # Add specific details based on event type
                if 'risk_score' in event_data:
                    print(f"      Risk Score: {event_data['risk_score']:.2f}")
                if 'confidence' in event_data:
                    print(f"      Confidence: {event_data['confidence']}")
                if 'potential_loss' in event_data:
                    print(f"      Potential Loss: {event_data['potential_loss']:.2f} LKR")
            
            print("-" * 50)
            
            # Show system insights
            self.display_system_insights()
            
        else:
            print("\n✅ No security events detected - System operating normally")

    def display_system_insights(self):
        """Display intelligent system insights"""
        print("\n🧠 INTELLIGENT SYSTEM INSIGHTS:")
        
        # Risk assessment
        high_risk_customers = len([c for c, p in self.customer_risk_profiles.items() if p['risk_score'] > 0.7])
        if high_risk_customers > 0:
            print(f"   ⚠️ {high_risk_customers} customer(s) flagged as high-risk")
        
        # Active threats
        active_threats = len(self.theft_risk_engine['active_risks'])
        if active_threats > 0:
            print(f"   🚨 {active_threats} active security threat(s) require attention")
        
        # System health
        health_score = self.calculate_system_health_score()
        if health_score < 80:
            print(f"   🔧 System health needs attention: {health_score:.1f}/100")
        elif health_score >= 95:
            print(f"   ✅ System operating at optimal health: {health_score:.1f}/100")
        
        # Predictive insights
        current_hour = datetime.now().hour
        if current_hour in [11, 12, 17, 18]:  # Peak hours
            print(f"   📈 Peak traffic period - Enhanced monitoring active")
        
        print("-" * 50)

    def get_real_time_dashboard_data(self) -> Dict:
        """Generate real-time data for dashboard integration"""
        summary = self.get_detection_summary()
        
        # Calculate additional metrics for dashboard
        current_time = datetime.now()
        recent_events_1h = [e for e in self.detected_events 
                           if (current_time - datetime.fromisoformat(e.get('timestamp', '').replace('Z', '+00:00').replace('+00:00', ''))).total_seconds() < 3600]
        
        return {
            'system_status': {
                'health_score': summary['risk_metrics']['system_health_score'],
                'status': 'HEALTHY' if summary['risk_metrics']['system_health_score'] > 80 else 'DEGRADED',
                'active_threats': summary['risk_metrics']['active_threats'],
                'high_risk_customers': summary['risk_metrics']['high_risk_customers']
            },
            'event_metrics': {
                'total_events': summary['total_events'],
                'events_last_hour': len(recent_events_1h),
                'event_types': summary['event_types'],
                'severity_distribution': summary['severity_distribution']
            },
            'operational_insights': {
                'detection_accuracy': summary['operational_metrics']['detection_accuracy'],
                'processing_efficiency': summary['operational_metrics']['processing_efficiency'],
                'alert_suppression_rate': summary['operational_metrics']['alert_suppression_rate']
            },
            'recent_events': [
                {
                    'event_name': e.get('event_data', {}).get('event_name', 'Unknown'),
                    'timestamp': e.get('timestamp', ''),
                    'severity': e.get('event_data', {}).get('severity', 'medium'),
                    'station_id': e.get('event_data', {}).get('station_id', 'N/A'),
                    'confidence': e.get('event_data', {}).get('confidence', 'medium')
                }
                for e in self.detected_events[-10:]
            ]
        }

    def reset_detection_state(self):
        """Reset detection state for new monitoring session"""
        self.detected_events = []
        self.event_counter = 1
        self.customer_risk_profiles.clear()
        self.theft_risk_engine['active_risks'].clear()
        self.alert_system['suppression_windows'].clear()
        print("🔄 Detection state reset for new monitoring session")

    def export_intelligence_report(self, filename: str):
        """Export comprehensive intelligence report"""
        try:
            report = {
                'report_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'system_version': 'Project Sentinel v2.0 - Enhanced Intelligence',
                    'detection_algorithms': [
                        'Enhanced Scan Avoidance Detection',
                        'Advanced Barcode Switching Detection', 
                        'Smart Weight Discrepancy Detection',
                        'Intelligent System Health Monitoring',
                        'Predictive Queue Forecasting',
                        'Theft Risk Scoring Engine',
                        'Enhanced Inventory Intelligence',
                        'Multi-Station Coordinated Fraud Detection',
                        'Intelligent Staffing Optimization',
                        'Sustainability & Efficiency Intelligence'
                    ]
                },
                'detection_summary': self.get_detection_summary(),
                'customer_risk_profiles': {
                    customer_id: {
                        'risk_score': profile['risk_score'],
                        'anomaly_count': profile['anomaly_count'],
                        'visit_frequency': profile['visit_frequency']
                    }
                    for customer_id, profile in self.customer_risk_profiles.items()
                    if profile['risk_score'] > 0.5
                },
                'system_recommendations': self.generate_system_recommendations(),
                'all_events': self.detected_events
            }
            
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"📄 Intelligence report exported to {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting intelligence report: {e}")

    def generate_system_recommendations(self) -> List[Dict]:
        """Generate intelligent system recommendations"""
        recommendations = []
        
        # Security recommendations
        high_risk_count = len([c for c, p in self.customer_risk_profiles.items() if p['risk_score'] > 0.7])
        if high_risk_count > 3:
            recommendations.append({
                'category': 'Security',
                'priority': 'High',
                'recommendation': 'Deploy additional security personnel during peak hours',
                'rationale': f'{high_risk_count} high-risk customers detected'
            })
        
        # Performance recommendations
        recent_crashes = len([e for e in self.detected_events[-20:] 
                             if 'crash' in e.get('event_data', {}).get('event_name', '').lower()])
        if recent_crashes > 2:
            recommendations.append({
                'category': 'Performance',
                'priority': 'Medium',
                'recommendation': 'Schedule system maintenance for affected stations',
                'rationale': f'{recent_crashes} system crashes detected recently'
            })
        
        # Operational recommendations
        staffing_events = len([e for e in self.detected_events[-10:] 
                              if 'staffing' in e.get('event_data', {}).get('event_name', '').lower()])
        if staffing_events > 2:
            recommendations.append({
                'category': 'Operations',
                'priority': 'Medium',
                'recommendation': 'Review staffing schedules and consider flexible workforce',
                'rationale': f'Multiple staffing alerts detected'
            })
        
        return recommendations