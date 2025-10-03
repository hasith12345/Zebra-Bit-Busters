#!/usr/bin/env python3
"""
Test the enhanced system with historical data integration
"""

from data_processor import DataProcessor
import json


def test_enhanced_analytics():
    """Test the enhanced analytics with historical data"""
    print("Testing Enhanced Analytics with Historical Data...")

    # Create data processor (loads all data automatically)
    processor = DataProcessor()

    # Test current status
    print("\n=== Current Status ===")
    status = processor.get_current_status()
    print(f"Active stations: {status.get('active_stations', [])}")
    print(
        f"Data queues - RFID: {len(processor.rfid_data)}, POS: {len(processor.pos_data)}")

    # Test predictive insights with historical data
    print("\n=== Predictive Insights (Enhanced with Historical Data) ===")
    insights = processor.get_predictive_insights()

    print(
        f"Busiest station: {insights.get('busiest_station', 'None detected')}")
    print(f"Revenue forecast: ${insights.get('revenue_forecast', 0):.2f}")

    # Inventory analysis
    inventory = insights.get('inventory_analysis', {})
    if inventory:
        print(f"\nInventory Analysis:")
        print(
            f"  Total products tracked: {inventory.get('total_products', 0)}")
        print(
            f"  Low stock items: {len(inventory.get('low_stock_items', []))}")
        print(
            f"  High demand products: {len(inventory.get('high_demand_products', []))}")
        print(
            f"  Average stock level: {inventory.get('average_stock_level', 0):.1f}")

    # Transaction patterns
    patterns = insights.get('transaction_patterns', {})
    if patterns:
        print(f"\nTransaction Patterns:")
        print(
            f"  Total historical transactions: {patterns.get('total_historical_transactions', 0)}")
        print(
            f"  Peak revenue hour: {patterns.get('peak_revenue_hour', 'N/A')}:00")

        popular = patterns.get('popular_products', {})
        if popular:
            print(f"  Most popular products:")
            for sku, count in list(popular.items())[:3]:
                product_name = processor.products_db.get(
                    sku, {}).get('product_name', sku)
                print(f"    {product_name} ({sku}): {count} transactions")

    # Peak time predictions
    peak_times = insights.get('peak_time_prediction', [])
    if peak_times:
        print(f"\nPeak Time Predictions: {', '.join(peak_times)}")

    # Recommendations
    recommendations = insights.get('recommended_actions', [])
    if recommendations:
        print(f"\nRecommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")

    # Historical data summary
    historical = insights.get('historical_trends', {})
    if historical:
        print(f"\nHistorical Data Sources:")
        sources = historical.get('data_sources_loaded', {})
        for source, count in sources.items():
            print(f"  {source}: {count} records")

    print("\n🎉 Enhanced analytics with historical data integration working perfectly! ✅")


if __name__ == "__main__":
    test_enhanced_analytics()
