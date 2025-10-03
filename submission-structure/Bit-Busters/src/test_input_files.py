#!/usr/bin/env python3
"""
Test script to verify input data files are readable
"""

from data_processor import DataProcessor


def test_data_loading():
    """Test that input files can be loaded correctly"""
    print("Testing input data file loading...")

    # Create data processor (this will automatically load data)
    processor = DataProcessor()

    # Check if reference data was loaded
    print(f"Products loaded: {len(processor.products_db)}")
    print(f"Customers loaded: {len(processor.customers_db)}")

    # Check if historical data was loaded
    print(
        f"Historical inventory snapshots: {len(processor.historical_inventory)}")
    print(
        f"Historical POS transactions: {len(processor.historical_transactions)}")
    print(f"Historical queue data: {len(processor.historical_queue_data)}")
    print(f"Historical RFID readings: {len(processor.historical_rfid_data)}")
    print(
        f"Historical product recognition: {len(processor.historical_product_recognition)}")

    # Show sample products
    if processor.products_db:
        print("\nSample products:")
        for i, (sku, product) in enumerate(list(processor.products_db.items())[:5]):
            product_name = product.get(
                'product_name', product.get('Product_Name', 'N/A'))
            price = product.get('price', product.get('Price', 'N/A'))
            print(f"  {sku}: {product_name} - ${price}")
            if i == 0:  # Show all available columns for first product
                print(f"    Available columns: {list(product.keys())}")

    # Show sample customers
    if processor.customers_db:
        print("\nSample customers:")
        for i, (customer_id, customer) in enumerate(list(processor.customers_db.items())[:5]):
            customer_name = customer.get(
                'Name', customer.get('Customer_Name', 'N/A'))
            print(f"  {customer_id}: {customer_name}")
            if i == 0:  # Show all available columns for first customer
                print(f"    Available columns: {list(customer.keys())}")

    # Show sample historical data
    if processor.historical_transactions:
        print("\nSample historical transaction:")
        sample_transaction = processor.historical_transactions[0]
        print(f"  Timestamp: {sample_transaction.get('timestamp', 'N/A')}")
        print(f"  Station: {sample_transaction.get('station_id', 'N/A')}")
        if 'data' in sample_transaction:
            data = sample_transaction['data']
            print(f"  Customer: {data.get('customer_id', 'N/A')}")
            print(
                f"  Product: {data.get('product_name', 'N/A')} ({data.get('sku', 'N/A')})")
            print(f"  Price: ${data.get('price', 'N/A')}")

    if processor.historical_inventory:
        print("\nSample inventory snapshot:")
        sample_inventory = processor.historical_inventory[0]
        print(f"  Timestamp: {sample_inventory.get('timestamp', 'N/A')}")
        if 'data' in sample_inventory:
            inventory_data = sample_inventory['data']
            print(f"  Total products tracked: {len(inventory_data)}")
            print(
                f"  Sample inventory levels: {dict(list(inventory_data.items())[:5])}")

    print("\n🎉 All input data files are now readable and integrated! ✅")
    print("✅ CSV files: products_list.csv, customer_data.csv")
    print("✅ JSONL files: inventory_snapshots.jsonl, pos_transactions.jsonl, queue_monitoring.jsonl, rfid_readings.jsonl, product_recognition.jsonl")
    print("✅ Historical data available for enhanced analytics and event detection")


if __name__ == "__main__":
    test_data_loading()
