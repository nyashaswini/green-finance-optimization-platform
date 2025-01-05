from data_collectors.free_data_collector import FreeDataCollector
from data_collectors.data_processor import DataProcessor

def test_data_collection():
    print("Testing Free Data Collection...")
    
    # Initialize collectors
    collector = FreeDataCollector()
    processor = DataProcessor()
    
    # Test individual data sources
    print("\n1. Testing UN SDG Data Collection:")
    sdg_data = collector.get_un_sdg_data()
    print(f"SDG Data Retrieved: {'Success' if sdg_data else 'Failed'}")
    
    print("\n2. Testing World Bank Data Collection:")
    wb_data = collector.get_world_bank_data()
    print(f"World Bank Data Retrieved: {'Success' if wb_data is not None else 'Failed'}")
    
    print("\n3. Testing NOAA Climate Data Collection:")
    climate_data = collector.get_noaa_climate_data()
    print(f"Climate Data Retrieved: {'Success' if climate_data else 'Failed'}")
    
    print("\n4. Testing NASA Earth Data Collection:")
    nasa_data = collector.get_nasa_earth_data()
    print(f"NASA Data Retrieved: {'Success' if nasa_data else 'Failed'}")
    
    print("\n5. Testing IEA Energy Data Collection:")
    iea_data = collector.get_iea_data()
    print(f"IEA Data Retrieved: {'Success' if iea_data else 'Failed'}")
    
    print("\n6. Testing EEA Reports Collection:")
    eea_data = collector.get_eea_reports()
    print(f"EEA Reports Retrieved: {'Success' if eea_data else 'Failed'}")
    
    # Collect all data
    print("\nCollecting all data...")
    all_data = collector.collect_all_data()
    
    # Process collected data
    print("\nProcessing collected data...")
    processor.process_environmental_data(all_data)
    processor.process_social_data(all_data)
    processor.process_governance_data(all_data)
    
    # Export processed data
    print("\nExporting processed data...")
    export_success = processor.export_processed_data('data/processed_data.json')
    print(f"Data Export: {'Success' if export_success else 'Failed'}")

if __name__ == "__main__":
    test_data_collection()
