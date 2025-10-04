#!/usr/bin/env python3
"""
API Server for Project Sentinel
Provides REST API endpoints for React dashboard to get real-time data
"""

import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socketserver
from datetime import datetime


class SentinelAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Enable CORS for React development server
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        try:
            if path == '/api/status':
                self.handle_status()
            elif path == '/api/events':
                self.handle_events()
            elif path == '/api/dashboard':
                self.handle_dashboard_data()
            elif path == '/api/stations':
                self.handle_stations()
            elif path == '/api/analytics':
                self.handle_analytics()
            elif path == '/api/sales':
                self.handle_sales_data()
            elif path == '/api/inventory':
                self.handle_inventory_insights()
            elif path == '/api/customer-behavior':
                self.handle_customer_behavior()
            else:
                self.send_error_response(404, "Endpoint not found")
        except Exception as e:
            self.send_error_response(500, str(e))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def handle_status(self):
        """Return system status"""
        if hasattr(self.server, 'data_processor') and hasattr(self.server, 'event_detector'):
            status = self.server.data_processor.get_current_status()
            total_events = len(self.server.event_detector.detected_events)

            response = {
                'status': 'running',
                'timestamp': datetime.now().isoformat(),
                'rfid_events': status.get('rfid_events', 0),
                'pos_events': status.get('pos_events', 0),
                'queue_events': status.get('queue_events', 0),
                'recognition_events': status.get('recognition_events', 0),
                'total_alerts': total_events,
                'is_connected': True
            }
        else:
            response = {
                'status': 'disconnected',
                'timestamp': datetime.now().isoformat(),
                'is_connected': False
            }

        self.wfile.write(json.dumps(response).encode())

    def handle_events(self):
        """Return recent events"""
        if hasattr(self.server, 'event_detector'):
            events = self.server.event_detector.detected_events
            recent_events = events[-20:] if len(events) > 20 else events

            # Convert to API format
            formatted_events = []
            for i, event in enumerate(reversed(recent_events)):
                formatted_events.append({
                    'id': f'E{len(events) - i:03d}',
                    'type': event['event_data']['event_name'],
                    'timestamp': event.get('timestamp', datetime.now().isoformat()),
                    'station_id': event['event_data'].get('station_id', 'Unknown'),
                    'severity': event['event_data'].get('severity', 'medium'),
                    'details': event['event_data'].get('details', '')
                })

            response = {
                'events': formatted_events,
                'total_count': len(events),
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {
                'events': [],
                'total_count': 0,
                'timestamp': datetime.now().isoformat()
            }

        self.wfile.write(json.dumps(response).encode())

    def handle_dashboard_data(self):
        """Return complete dashboard data"""
        if hasattr(self.server, 'data_processor') and hasattr(self.server, 'event_detector'):
            # Get real data from the system
            status = self.server.data_processor.get_current_status()
            events = self.server.event_detector.detected_events

            # Calculate event type distribution
            event_types = {}
            for event in events:
                event_name = event['event_data']['event_name']
                event_types[event_name] = event_types.get(event_name, 0) + 1

            # Format event types for frontend
            total_events = len(events)
            formatted_event_types = []
            for event_type, count in event_types.items():
                percentage = (count / total_events *
                              100) if total_events > 0 else 0
                formatted_event_types.append({
                    'name': event_type,
                    'count': count,
                    'percentage': round(percentage, 1)
                })

            # Station data (based on real data)
            stations = [
                {
                    'id': 'SCC1',
                    'efficiency': 95.0 + (status.get('pos_events', 0) * 0.5),
                    'isActive': status.get('pos_events', 0) > 0
                },
                {
                    'id': 'SC-02',
                    'efficiency': 92.0 + (status.get('rfid_events', 0) * 0.3),
                    'isActive': status.get('rfid_events', 0) > 0
                },
                {
                    'id': 'SC-03',
                    'efficiency': 98.0 + (status.get('queue_events', 0) * 0.2),
                    'isActive': status.get('queue_events', 0) > 0
                }
            ]

            # Recent events
            recent_events = events[-10:] if len(events) > 10 else events
            formatted_recent_events = []
            for i, event in enumerate(reversed(recent_events)):
                formatted_recent_events.append({
                    'id': f'E{len(events) - i:03d}',
                    'type': event['event_data']['event_name'],
                    'timestamp': event.get('timestamp', datetime.now().isoformat()),
                    'station_id': event['event_data'].get('station_id', 'Unknown')
                })

            # Calculate active stations
            active_stations = sum(
                1 for station in stations if station['isActive'])
            avg_efficiency = sum(station['efficiency']
                                 for station in stations) / len(stations)

            response = {
                'totalEvents': total_events,
                'activeStations': active_stations,
                'averageEfficiency': round(avg_efficiency, 1),
                'eventTypes': formatted_event_types,
                'stations': stations,
                'recentEvents': formatted_recent_events,
                'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'systemStatus': {
                    'rfid_events': status.get('rfid_events', 0),
                    'pos_events': status.get('pos_events', 0),
                    'queue_events': status.get('queue_events', 0),
                    'recognition_events': status.get('recognition_events', 0)
                }
            }
        else:
            # Fallback dummy data when system not connected
            response = {
                'totalEvents': 0,
                'activeStations': 0,
                'averageEfficiency': 0,
                'eventTypes': [],
                'stations': [],
                'recentEvents': [],
                'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'systemStatus': {
                    'rfid_events': 0,
                    'pos_events': 0,
                    'queue_events': 0,
                    'recognition_events': 0
                },
                'error': 'System not connected'
            }

        self.wfile.write(json.dumps(response).encode())

    def handle_stations(self):
        """Return station-specific data"""
        if hasattr(self.server, 'data_processor'):
            status = self.server.data_processor.get_current_status()

            stations = [
                {
                    'id': 'SCC1',
                    'name': 'Self-Checkout 1',
                    'status': 'active' if status.get('pos_events', 0) > 0 else 'idle',
                    'efficiency': 95.0,
                    'transactions': status.get('pos_events', 0),
                    'last_activity': datetime.now().isoformat()
                },
                {
                    'id': 'SC-02',
                    'name': 'Station 2',
                    'status': 'active' if status.get('rfid_events', 0) > 0 else 'idle',
                    'efficiency': 92.0,
                    'transactions': status.get('rfid_events', 0),
                    'last_activity': datetime.now().isoformat()
                },
                {
                    'id': 'SC-03',
                    'name': 'Station 3',
                    'status': 'active' if status.get('queue_events', 0) > 0 else 'idle',
                    'efficiency': 98.0,
                    'transactions': status.get('queue_events', 0),
                    'last_activity': datetime.now().isoformat()
                }
            ]

            response = {
                'stations': stations,
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {
                'stations': [],
                'timestamp': datetime.now().isoformat(),
                'error': 'System not connected'
            }

        self.wfile.write(json.dumps(response).encode())

    def send_error_response(self, code, message):
        """Send error response"""
        response = {
            'error': message,
            'timestamp': datetime.now().isoformat()
        }
        self.wfile.write(json.dumps(response).encode())

    def handle_analytics(self):
        """Return comprehensive business analytics"""
        if hasattr(self.server, 'data_processor'):
            # Get POS transaction data for analysis
            pos_data = list(self.server.data_processor.pos_data)

            # Sales metrics
            total_revenue = 0
            product_sales = {}
            hourly_sales = {}
            customer_transactions = {}

            for transaction in pos_data:
                if 'data' in transaction and 'price' in transaction['data']:
                    price = transaction['data']['price']
                    total_revenue += price

                    # Track product sales
                    product_name = transaction['data'].get(
                        'product_name', 'Unknown')
                    if product_name in product_sales:
                        product_sales[product_name]['count'] += 1
                        product_sales[product_name]['revenue'] += price
                    else:
                        product_sales[product_name] = {
                            'count': 1, 'revenue': price}

                    # Track hourly sales
                    timestamp = transaction.get('timestamp', '')
                    if timestamp:
                        hour = timestamp[11:13] if len(
                            timestamp) > 13 else '16'
                        hourly_sales[hour] = hourly_sales.get(hour, 0) + price

                    # Track customer behavior
                    customer_id = transaction['data'].get(
                        'customer_id', 'Unknown')
                    if customer_id in customer_transactions:
                        customer_transactions[customer_id]['count'] += 1
                        customer_transactions[customer_id]['total'] += price
                    else:
                        customer_transactions[customer_id] = {
                            'count': 1, 'total': price}

            # Top selling products
            top_products = sorted(product_sales.items(),
                                  key=lambda x: x[1]['revenue'], reverse=True)[:5]

            # Sales trends (hourly)
            sales_trend = [{'hour': f"{hour}:00", 'revenue': revenue}
                           for hour, revenue in sorted(hourly_sales.items())]

            # Customer insights
            avg_transaction_value = total_revenue / \
                len(pos_data) if pos_data else 0
            unique_customers = len(customer_transactions)

            response = {
                'total_revenue': round(total_revenue, 2),
                'total_transactions': len(pos_data),
                'avg_transaction_value': round(avg_transaction_value, 2),
                'unique_customers': unique_customers,
                'top_products': [
                    {
                        'name': name,
                        'sales_count': data['count'],
                        'revenue': round(data['revenue'], 2)
                    } for name, data in top_products
                ],
                'hourly_sales': sales_trend,
                'customer_metrics': {
                    'repeat_customers': sum(1 for c in customer_transactions.values() if c['count'] > 1),
                    'avg_customer_spending': round(sum(c['total'] for c in customer_transactions.values()) / unique_customers if unique_customers > 0 else 0, 2)
                },
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {
                'error': 'Data processor not available',
                'timestamp': datetime.now().isoformat()
            }

        self.wfile.write(json.dumps(response).encode())

    def handle_sales_data(self):
        """Return detailed sales data"""
        if hasattr(self.server, 'data_processor'):
            pos_data = list(self.server.data_processor.pos_data)

            # Recent transactions (last 10)
            recent_sales = []
            for transaction in pos_data[-10:]:
                if 'data' in transaction:
                    recent_sales.append({
                        'timestamp': transaction.get('timestamp', ''),
                        'customer_id': transaction['data'].get('customer_id', 'Unknown'),
                        'product_name': transaction['data'].get('product_name', 'Unknown'),
                        'price': transaction['data'].get('price', 0),
                        'station_id': transaction.get('station_id', 'SCC1')
                    })

            # Category analysis
            category_sales = {}
            for transaction in pos_data:
                if 'data' in transaction and 'sku' in transaction['data']:
                    sku = transaction['data']['sku']
                    category = sku.split('_')[1] if '_' in sku else 'Unknown'
                    price = transaction['data'].get('price', 0)

                    if category in category_sales:
                        category_sales[category]['count'] += 1
                        category_sales[category]['revenue'] += price
                    else:
                        category_sales[category] = {
                            'count': 1, 'revenue': price}

            # Format category data
            category_data = [
                {
                    'category': cat,
                    'sales_count': data['count'],
                    'revenue': round(data['revenue'], 2),
                    'avg_price': round(data['revenue'] / data['count'], 2)
                } for cat, data in category_sales.items()
            ]

            response = {
                'recent_transactions': recent_sales,
                'category_performance': sorted(category_data, key=lambda x: x['revenue'], reverse=True),
                'total_sales_today': len(pos_data),
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {
                'error': 'Data processor not available',
                'timestamp': datetime.now().isoformat()
            }

        self.wfile.write(json.dumps(response).encode())

    def handle_inventory_insights(self):
        """Return inventory analysis and insights"""
        if hasattr(self.server, 'data_processor'):
            inventory_data = self.server.data_processor.inventory_data
            pos_data = list(self.server.data_processor.pos_data)

            # Calculate stock movement
            stock_alerts = []
            fast_moving = []

            for sku, current_stock in inventory_data.items():
                # Simulate initial stock (would be from historical data)
                initial_stock = current_stock + 10  # Approximate

                if current_stock < 50:  # Low stock threshold
                    stock_alerts.append({
                        'sku': sku,
                        'current_stock': current_stock,
                        'status': 'low' if current_stock < 30 else 'medium',
                        'recommended_reorder': 100
                    })

                # Calculate movement
                movement = initial_stock - current_stock
                if movement > 5:
                    fast_moving.append({
                        'sku': sku,
                        'current_stock': current_stock,
                        'units_sold': movement,
                        'velocity': 'high' if movement > 10 else 'medium'
                    })

            # Product performance from sales
            product_performance = {}
            for transaction in pos_data:
                if 'data' in transaction:
                    sku = transaction['data'].get('sku', '')
                    if sku in product_performance:
                        product_performance[sku] += 1
                    else:
                        product_performance[sku] = 1

            response = {
                'stock_alerts': sorted(stock_alerts, key=lambda x: x['current_stock']),
                'fast_moving_items': sorted(fast_moving, key=lambda x: x['units_sold'], reverse=True)[:10],
                'total_skus': len(inventory_data),
                'low_stock_count': len([item for item in stock_alerts if item['status'] == 'low']),
                'out_of_stock_count': len([sku for sku, stock in inventory_data.items() if stock == 0]),
                'product_performance': [
                    {'sku': sku, 'sales_count': count}
                    for sku, count in sorted(product_performance.items(), key=lambda x: x[1], reverse=True)[:10]
                ],
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {
                'error': 'Data processor not available',
                'timestamp': datetime.now().isoformat()
            }

        self.wfile.write(json.dumps(response).encode())

    def handle_customer_behavior(self):
        """Return customer behavior analytics"""
        if hasattr(self.server, 'data_processor'):
            pos_data = list(self.server.data_processor.pos_data)
            queue_data = list(self.server.data_processor.queue_data)

            # Customer transaction patterns
            customer_analysis = {}
            for transaction in pos_data:
                if 'data' in transaction:
                    customer_id = transaction['data'].get(
                        'customer_id', 'Unknown')
                    price = transaction['data'].get('price', 0)
                    timestamp = transaction.get('timestamp', '')

                    if customer_id not in customer_analysis:
                        customer_analysis[customer_id] = {
                            'transaction_count': 0,
                            'total_spent': 0,
                            'last_visit': timestamp,
                            'products': []
                        }

                    customer_analysis[customer_id]['transaction_count'] += 1
                    customer_analysis[customer_id]['total_spent'] += price
                    customer_analysis[customer_id]['products'].append(
                        transaction['data'].get('product_name', 'Unknown')
                    )

            # Queue efficiency analysis
            queue_stats = {
                'total_queue_events': len(queue_data),
                'avg_queue_time': 2.5,  # Simulated
                'peak_hours': ['16:00', '17:00', '18:00']
            }

            # Top customers
            top_customers = sorted(
                [(cid, data) for cid, data in customer_analysis.items()],
                key=lambda x: x[1]['total_spent'], reverse=True
            )[:5]

            response = {
                'total_unique_customers': len(customer_analysis),
                'avg_transactions_per_customer': round(sum(data['transaction_count'] for data in customer_analysis.values()) / len(customer_analysis) if customer_analysis else 0, 2),
                'avg_spending_per_customer': round(sum(data['total_spent'] for data in customer_analysis.values()) / len(customer_analysis) if customer_analysis else 0, 2),
                'top_customers': [
                    {
                        'customer_id': cid,
                        'transaction_count': data['transaction_count'],
                        'total_spent': round(data['total_spent'], 2),
                        'avg_order_value': round(data['total_spent'] / data['transaction_count'], 2)
                    } for cid, data in top_customers
                ],
                'queue_analytics': queue_stats,
                'shopping_patterns': {
                    'peak_shopping_hours': ['16:00-17:00', '17:00-18:00'],
                    'most_bought_together': ['Rice & Curry Powder', 'Milk & Tea', 'Soap & Shampoo']
                },
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {
                'error': 'Data processor not available',
                'timestamp': datetime.now().isoformat()
            }

        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        pass


class SentinelAPIServer:
    def __init__(self, port=3001):
        self.port = port
        self.server = None
        self.server_thread = None
        self.data_processor = None
        self.event_detector = None

    def set_system_components(self, data_processor, event_detector):
        """Set references to the main system components"""
        self.data_processor = data_processor
        self.event_detector = event_detector

        if self.server:
            self.server.data_processor = data_processor
            self.server.event_detector = event_detector

    def start_server(self):
        """Start the API server"""
        try:
            self.server = HTTPServer(
                ('localhost', self.port), SentinelAPIHandler)
            self.server.data_processor = self.data_processor
            self.server.event_detector = self.event_detector

            self.server_thread = threading.Thread(
                target=self.server.serve_forever, daemon=True)
            self.server_thread.start()

            print(f"✅ API Server started on http://localhost:{self.port}")
            print(
                f"   • Dashboard data: http://localhost:{self.port}/api/dashboard")
            print(f"   • Events: http://localhost:{self.port}/api/events")
            print(f"   • Status: http://localhost:{self.port}/api/status")
            return True

        except Exception as e:
            print(f"❌ Failed to start API server: {e}")
            return False

    def stop_server(self):
        """Stop the API server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("🛑 API Server stopped")


if __name__ == "__main__":
    # Test the API server standalone
    api_server = SentinelAPIServer(3001)

    try:
        if api_server.start_server():
            print("API Server running... Press Ctrl+C to stop")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        api_server.stop_server()
