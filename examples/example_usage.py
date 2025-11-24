"""
Example usage of the FDSE Challenge data processing functions.

This script demonstrates how to use the simulator and the three core functions.
Candidates can use this as a reference for testing their implementations.

Run with: python examples/example_usage.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_simulator import IndustrialDataSimulator
from src.data_processing import ingest_data, detect_anomalies, summarize_metrics


def main():
    """Demonstrate complete pipeline usage."""
    
    print("=" * 60)
    print("FDSE Challenge - Example Usage")
    print("=" * 60)
    
    # Step 1: Create simulator
    print("\n1. Creating industrial data simulator...")
    sim = IndustrialDataSimulator(seed=42, dropout_rate=0.1)
    print("   ✓ Simulator initialized with 10% dropout rate")
    
    # Step 2: Collect data batches
    print("\n2. Collecting data batches (some may fail)...")
    batches = sim.get_batch_readings(num_batches=5, batch_duration=20)
    print(f"   ✓ Successfully collected {len(batches)} batches")
    
    if not batches:
        print("   ✗ All batches failed - try running again or reduce dropout_rate")
        return
    
    # Inspect first batch
    print(f"\n   Sample from first batch:")
    print(f"   - Shape: {batches[0].shape}")
    print(f"   - Columns: {list(batches[0].columns)}")
    print(f"   - Sensors: {batches[0]['sensor'].unique()}")
    
    # Step 3: Ingest and clean data
    print("\n3. Ingesting and cleaning data...")
    try:
        clean_data = ingest_data(batches, validate=True)
        print(f"   ✓ Ingested {len(clean_data)} total readings")
        print(f"   ✓ Data quality: {(clean_data['quality'] == 'GOOD').sum()}/{len(clean_data)} good readings")
    except NotImplementedError:
        print("   ⚠ ingest_data() not yet implemented")
        return
    except Exception as e:
        print(f"   ✗ Error in ingest_data(): {e}")
        return
    
    # Step 4: Detect anomalies
    print("\n4. Detecting anomalies in temperature data...")
    try:
        anomaly_data = detect_anomalies(
            clean_data, 
            sensor_name="temperature",
            method="zscore",
            threshold=3.0
        )
        temp_anomalies = anomaly_data[
            (anomaly_data['sensor'] == 'temperature') & 
            (anomaly_data['is_anomaly'] == True)
        ]
        print(f"   ✓ Detected {len(temp_anomalies)} temperature anomalies")
        
        if len(temp_anomalies) > 0:
            print(f"   ✓ Anomaly score range: {temp_anomalies['anomaly_score'].min():.2f} - {temp_anomalies['anomaly_score'].max():.2f}")
    except NotImplementedError:
        print("   ⚠ detect_anomalies() not yet implemented")
        anomaly_data = clean_data
    except Exception as e:
        print(f"   ✗ Error in detect_anomalies(): {e}")
        anomaly_data = clean_data
    
    # Step 5: Summarize metrics
    print("\n5. Generating summary metrics...")
    try:
        metrics = summarize_metrics(anomaly_data, group_by="sensor")
        
        print(f"   ✓ Generated metrics for {len(metrics)} sensors")
        print("\n   Sample metrics for temperature:")
        
        if "temperature" in metrics:
            temp_metrics = metrics["temperature"]
            for key, value in temp_metrics.items():
                if isinstance(value, float):
                    print(f"     - {key}: {value:.2f}")
                else:
                    print(f"     - {key}: {value}")
    except NotImplementedError:
        print("   ⚠ summarize_metrics() not yet implemented")
    except Exception as e:
        print(f"   ✗ Error in summarize_metrics(): {e}")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
