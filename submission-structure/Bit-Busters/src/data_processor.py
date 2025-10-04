#!/usr/bin/env python3
"""
Data Processor for Project Sentinel
Connects to the streaming server and processes real-time data from all sensors
"""

import json
import socket
import threading
import time
import os
from typing import Dict, List, Optional
from collections import defaultdict, deque
from datetime import datetime, timedelta
import statistics


class DataProcessor:
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self.is_running = False

        # Enhanced data storage with time-based windows
        self.rfid_data = deque(maxlen=200)
        self.pos_data = deque(maxlen=200)
        self.product_recognition_data = deque(maxlen=200)
        self.queue_data = deque(maxlen=200)
        self.inventory_data = {}

        # Load reference data
        self.products_db = {}
        self.customers_db = {}
        self.historical_inventory = []
        self.historical_transactions = []
        self.historical_queue_data = []
        self.historical_rfid_data = []
        self.historical_product_recognition = []

        # For tracking events
        self.detected_events = []

        # Advanced analytics storage
        self.station_analytics = defaultdict(lambda: {
            'transaction_count': 0,
            'total_revenue': 0.0,
            'customer_flow': deque(maxlen=50),
            'error_count': 0,
            'avg_transaction_time': 0.0,
            'peak_times': []
        })

        # Behavioral patterns
        self.customer_patterns = defaultdict(lambda: {
            'visit_frequency': 0,
            'avg_basket_size': 0.0,
            'preferred_stations': [],
            'risk_score': 0.0
        })

        # Real-time metrics
        self.performance_metrics = {
            'events_per_second': 0,
            'processing_latency': 0.0,
            'data_quality_score': 100.0,
            'system_health': 'HEALTHY'
        }

        # Load reference and historical data on initialization
        self.load_reference_data()
        self.load_historical_data()

    def load_reference_data(self):
        """Load product and customer reference data"""
        try:
            # Load products
            import csv
            # Use absolute path to find the data directory in the zebra root
            current_dir = os.path.abspath(__file__)
            # Navigate up to zebra directory: src -> Bit-Busters -> submission-structure -> zebra
            zebra_dir = os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.dirname(current_dir))))
            products_file = os.path.join(
                zebra_dir, "data", "input", "products_list.csv")

            if os.path.exists(products_file):
                with open(products_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Use the correct column name from the CSV
                        sku = row.get('SKU', row.get('sku', ''))
                        if sku:
                            self.products_db[sku] = row

            # Load customers
            customers_file = os.path.join(
                zebra_dir, "data", "input", "customer_data.csv")
            if os.path.exists(customers_file):
                with open(customers_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Use the correct column name from the CSV
                        customer_id = row.get(
                            'Customer_ID', row.get('customer_id', ''))
                        if customer_id:
                            self.customers_db[customer_id] = row

            print(
                f"Loaded {len(self.products_db)} products and {len(self.customers_db)} customers")

        except Exception as e:
            print(f"Warning: Could not load reference data: {e}")

    def load_historical_data(self):
        """Load historical data from JSONL files for better analytics"""
        try:
            # Get the zebra directory path
            current_dir = os.path.abspath(__file__)
            zebra_dir = os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.dirname(current_dir))))
            input_dir = os.path.join(zebra_dir, "data", "input")

            # Load historical inventory snapshots
            inventory_file = os.path.join(
                input_dir, "inventory_snapshots.jsonl")
            if os.path.exists(inventory_file):
                with open(inventory_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            self.historical_inventory.append(data)

            # Load historical POS transactions
            pos_file = os.path.join(input_dir, "pos_transactions.jsonl")
            if os.path.exists(pos_file):
                with open(pos_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            self.historical_transactions.append(data)

            # Load historical queue monitoring data
            queue_file = os.path.join(input_dir, "queue_monitoring.jsonl")
            if os.path.exists(queue_file):
                with open(queue_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            self.historical_queue_data.append(data)

            # Load historical RFID readings
            rfid_file = os.path.join(input_dir, "rfid_readings.jsonl")
            if os.path.exists(rfid_file):
                with open(rfid_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            self.historical_rfid_data.append(data)

            # Load historical product recognition data
            product_rec_file = os.path.join(
                input_dir, "product_recognition.jsonl")
            if os.path.exists(product_rec_file):
                with open(product_rec_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            self.historical_product_recognition.append(data)

            print(f"Loaded historical data: {len(self.historical_inventory)} inventory snapshots, "
                  f"{len(self.historical_transactions)} transactions, {len(self.historical_queue_data)} queue records, "
                  f"{len(self.historical_rfid_data)} RFID readings, {len(self.historical_product_recognition)} product recognition records")

        except Exception as e:
            print(f"Warning: Could not load historical data: {e}")

    def connect_to_stream(self):
        """Connect to the data streaming server"""
        try:
            with socket.create_connection((self.host, self.port)) as conn:
                print(f"Connected to stream server at {self.host}:{self.port}")

                with conn.makefile("r", encoding="utf-8") as stream:
                    for line in stream:
                        if not self.is_running:
                            break

                        if not line.strip():
                            continue

                        try:
                            event = json.loads(line)
                            self.process_event(event)
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON: {e}")

        except ConnectionError as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def process_event(self, event):
        """Process incoming event and store in appropriate data structure"""
        dataset = event.get('dataset', '')
        event_data = event.get('event', {})

        # Store recent events (keep last 100 for analysis)
        max_events = 100

        if 'RFID' in dataset or 'rfid' in dataset.lower():
            self.rfid_data.append(event_data)
            if len(self.rfid_data) > max_events:
                self.rfid_data.popleft()

        elif 'POS' in dataset or 'pos' in dataset.lower() or 'transaction' in dataset.lower():
            self.pos_data.append(event_data)
            if len(self.pos_data) > max_events:
                self.pos_data.popleft()

        elif 'Product_recognition' in dataset or 'recognition' in dataset.lower():
            self.product_recognition_data.append(event_data)
            if len(self.product_recognition_data) > max_events:
                self.product_recognition_data.popleft()

        elif 'Queue' in dataset or 'queue' in dataset.lower():
            self.queue_data.append(event_data)
            if len(self.queue_data) > max_events:
                self.queue_data.popleft()

        elif 'inventory' in dataset.lower():
            # Inventory is a snapshot, so just update the current state
            if 'data' in event_data:
                self.inventory_data.update(event_data['data'])

        # Print for debugging (remove in production)
        print(f"[{dataset}] {event_data.get('timestamp', 'No timestamp')}")

        # Update analytics in real-time
        self.update_analytics(dataset, event_data)

    def start_processing(self):
        """Start the data processing in a separate thread"""
        self.is_running = True
        self.load_reference_data()

        # Start processing in background thread
        processing_thread = threading.Thread(target=self.connect_to_stream)
        processing_thread.daemon = True
        processing_thread.start()

        print("Data processor started. Processing events...")
        return processing_thread

    def stop_processing(self):
        """Stop the data processing"""
        self.is_running = False
        print("Data processor stopped.")

    def get_current_status(self):
        """Get current status summary with enhanced metrics"""
        return {
            'rfid_events': len(self.rfid_data),
            'pos_events': len(self.pos_data),
            'recognition_events': len(self.product_recognition_data),
            'queue_events': len(self.queue_data),
            'inventory_items': len(self.inventory_data),
            'products_loaded': len(self.products_db),
            'customers_loaded': len(self.customers_db),
            'system_health': self.performance_metrics['system_health'],
            'data_quality_score': self.performance_metrics['data_quality_score'],
            'total_revenue': sum(station['total_revenue'] for station in self.station_analytics.values())
        }

    def update_analytics(self, dataset: str, event_data: dict):
        """Update real-time analytics based on incoming data"""
        try:
            station_id = event_data.get('station_id')

            if 'POS' in dataset and station_id:
                # Update station analytics
                station = self.station_analytics[station_id]
                station['transaction_count'] += 1

                if 'data' in event_data and 'price' in event_data['data']:
                    station['total_revenue'] += float(
                        event_data['data']['price'])

                # Track customer patterns
                customer_id = event_data.get('data', {}).get('customer_id')
                if customer_id:
                    self.customer_patterns[customer_id]['visit_frequency'] += 1

            elif 'Queue' in dataset and station_id:
                # Update customer flow metrics
                customer_count = event_data.get(
                    'data', {}).get('customer_count', 0)
                self.station_analytics[station_id]['customer_flow'].append(
                    customer_count)

            # Update system health based on error rates
            if event_data.get('status') in ['Read Error', 'System Crash']:
                if station_id:
                    self.station_analytics[station_id]['error_count'] += 1
                self.performance_metrics['data_quality_score'] = max(0,
                                                                     self.performance_metrics['data_quality_score'] - 1)

        except Exception as e:
            print(f"Analytics update error: {e}")

    def get_station_insights(self, station_id: str) -> dict:
        """Get detailed insights for a specific station"""
        station = self.station_analytics.get(station_id, {})
        customer_flow = list(station.get('customer_flow', []))

        return {
            'station_id': station_id,
            'transactions_today': station.get('transaction_count', 0),
            'revenue_today': station.get('total_revenue', 0),
            'avg_queue_length': statistics.mean(customer_flow) if customer_flow else 0,
            'peak_queue_length': max(customer_flow) if customer_flow else 0,
            'error_rate': station.get('error_count', 0) / max(1, station.get('transaction_count', 1)),
            'efficiency_score': self.calculate_efficiency_score(station_id)
        }

    def calculate_efficiency_score(self, station_id: str) -> float:
        """Calculate efficiency score for a station (0-100)"""
        station = self.station_analytics.get(station_id, {})

        # Base score
        score = 100.0

        # Reduce score for errors
        error_rate = station.get('error_count', 0) / \
            max(1, station.get('transaction_count', 1))
        score -= (error_rate * 30)

        # Reduce score for long queues
        customer_flow = list(station.get('customer_flow', []))
        if customer_flow:
            avg_queue = statistics.mean(customer_flow)
            if avg_queue > 4:
                score -= ((avg_queue - 4) * 10)

        return max(0, min(100, score))

    def get_predictive_insights(self) -> dict:
        """Generate predictive insights based on current trends and historical data"""
        insights = {
            'busiest_station': None,
            'peak_time_prediction': None,
            'revenue_forecast': 0.0,
            'high_risk_customers': [],
            'recommended_actions': [],
            'inventory_analysis': {},
            'transaction_patterns': {},
            'historical_trends': {}
        }

        # Find busiest station from real-time data
        max_transactions = 0
        for station_id, data in self.station_analytics.items():
            if data['transaction_count'] > max_transactions:
                max_transactions = data['transaction_count']
                insights['busiest_station'] = station_id

        # Analyze historical data for better insights
        if self.historical_inventory:
            latest_inventory = self.historical_inventory[-1].get('data', {})
            insights['inventory_analysis'] = {
                'total_products': len(latest_inventory),
                'low_stock_items': [sku for sku, qty in latest_inventory.items() if qty < 50],
                'high_demand_products': [sku for sku, qty in latest_inventory.items() if qty < 80],
                'average_stock_level': sum(latest_inventory.values()) / len(latest_inventory) if latest_inventory else 0
            }

        # Analyze transaction patterns from historical data
        if self.historical_transactions:
            transaction_hours = []
            product_sales = defaultdict(int)
            revenue_by_hour = defaultdict(float)

            for transaction in self.historical_transactions:
                timestamp = transaction.get('timestamp', '')
                if timestamp and 'T' in timestamp:
                    hour = int(timestamp.split('T')[1].split(':')[0])
                    transaction_hours.append(hour)

                data = transaction.get('data', {})
                sku = data.get('sku', '')
                price = data.get('price', 0)

                if sku:
                    product_sales[sku] += 1
                if price and timestamp:
                    hour = int(timestamp.split('T')[1].split(':')[0])
                    revenue_by_hour[hour] += price

            # Predict peak hours based on historical data
            if transaction_hours:
                from collections import Counter
                hour_counts = Counter(transaction_hours)
                peak_hours = hour_counts.most_common(3)
                insights['peak_time_prediction'] = [
                    f"{hour}:00" for hour, count in peak_hours]

            # Revenue forecast based on historical patterns
            if revenue_by_hour:
                avg_hourly_revenue = sum(
                    revenue_by_hour.values()) / len(revenue_by_hour)
                insights['revenue_forecast'] = avg_hourly_revenue * \
                    24  # Daily forecast

            insights['transaction_patterns'] = {
                'popular_products': dict(sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]),
                'peak_revenue_hour': max(revenue_by_hour.items(), key=lambda x: x[1])[0] if revenue_by_hour else None,
                'total_historical_transactions': len(self.historical_transactions)
            }

        # Identify high-risk customers (simplified model)
        for customer_id, pattern in self.customer_patterns.items():
            if pattern['visit_frequency'] > 5 and pattern['risk_score'] > 0.7:
                insights['high_risk_customers'].append(customer_id)

        # Generate enhanced recommendations
        recommendations = []

        # Station-based recommendations
        for station_id, data in self.station_analytics.items():
            customer_flow = list(data.get('customer_flow', []))
            if customer_flow and statistics.mean(customer_flow) > 4:
                recommendations.append(
                    f"Open additional checkout at {station_id} - high queue detected"
                )

        # Inventory-based recommendations
        if insights['inventory_analysis'].get('low_stock_items'):
            low_stock_count = len(
                insights['inventory_analysis']['low_stock_items'])
            recommendations.append(
                f"Urgent: Restock {low_stock_count} items with low inventory")

        # Peak time recommendations
        if insights.get('peak_time_prediction'):
            peak_time = insights['peak_time_prediction'][0]
            recommendations.append(
                f"Schedule additional staff for peak time at {peak_time}")

        insights['recommended_actions'] = recommendations
        insights['historical_trends'] = {
            'data_sources_loaded': {
                'inventory_snapshots': len(self.historical_inventory),
                'transactions': len(self.historical_transactions),
                'queue_data': len(self.historical_queue_data),
                'rfid_readings': len(self.historical_rfid_data),
                'product_recognition': len(self.historical_product_recognition)
            }
        }

        return insights


# Test the data processor
if __name__ == "__main__":
    processor = DataProcessor()

    try:
        thread = processor.start_processing()

        # Let it run for 30 seconds to collect data
        for i in range(30):
            time.sleep(1)
            if i % 5 == 0:  # Print status every 5 seconds
                status = processor.get_current_status()
                print(f"Status: {status}")

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        processor.stop_processing()
