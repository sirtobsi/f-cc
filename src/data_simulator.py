"""
Industrial Data Simulator with Intentional Flakiness

This module simulates data from industrial protocols (OPC UA/Modbus) with
realistic issues like connection dropouts, missing values, and timing jitter.

DO NOT MODIFY THIS FILE - It simulates real-world industrial data conditions.
"""

import random
import time
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class IndustrialDataSimulator:
    """
    Simulates industrial sensor data with realistic flakiness.
    
    Intentional issues:
    - Random connection dropouts (5-10% of reads)
    - Missing/null values (2-5% of data points)
    - Timestamp jitter and out-of-order records
    - Duplicate readings
    - Sudden sensor spikes/anomalies
    - Variable latency
    """
    
    def __init__(self, seed: Optional[int] = None, dropout_rate: float = 0.07):
        """
        Initialize the simulator.
        
        Args:
            seed: Random seed for reproducibility (None for random)
            dropout_rate: Probability of connection dropout (0.0-1.0)
        """
        self.seed = seed
        self.dropout_rate = dropout_rate
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        self.sensors = {
            "temperature": {"baseline": 65.0, "variance": 2.5, "unit": "°C"},
            "pressure": {"baseline": 101.3, "variance": 1.2, "unit": "kPa"},
            "vibration": {"baseline": 0.5, "variance": 0.15, "unit": "mm/s"},
            "flow_rate": {"baseline": 15.2, "variance": 0.8, "unit": "L/min"},
        }
        
        self.start_time = datetime.now()
        self.read_count = 0
    
    def read_sensors(
        self, 
        duration_seconds: int = 60, 
        interval_seconds: float = 1.0
    ) -> pd.DataFrame:
        """
        Simulate reading sensor data over a time period.
        
        Args:
            duration_seconds: How long to simulate data collection
            interval_seconds: Time between readings
        
        Returns:
            DataFrame with columns: timestamp, sensor, value, unit, quality
            
        Raises:
            ConnectionError: Randomly raised to simulate connection issues
        """
        # Simulate random connection dropout
        if random.random() < self.dropout_rate:
            raise ConnectionError(
                f"Simulated connection dropout at read #{self.read_count}"
            )
        
        records = []
        num_readings = int(duration_seconds / interval_seconds)
        
        for i in range(num_readings):
            base_timestamp = self.start_time + timedelta(seconds=i * interval_seconds)
            
            # Add timestamp jitter (±10% of interval)
            jitter = random.uniform(-interval_seconds * 0.1, interval_seconds * 0.1)
            timestamp = base_timestamp + timedelta(seconds=jitter)
            
            for sensor_name, config in self.sensors.items():
                # Simulate missing values (2-5% of readings)
                if random.random() < 0.03:
                    value = np.nan
                    quality = "BAD"
                # Simulate anomalies/spikes (1% of readings)
                elif random.random() < 0.01:
                    value = config["baseline"] + random.choice([-1, 1]) * config["variance"] * 10
                    quality = "UNCERTAIN"
                else:
                    # Normal reading with gaussian noise
                    value = config["baseline"] + np.random.normal(0, config["variance"])
                    quality = "GOOD"
                
                records.append({
                    "timestamp": timestamp,
                    "sensor": sensor_name,
                    "value": value,
                    "unit": config["unit"],
                    "quality": quality
                })
                
                # Occasionally duplicate a reading (0.5% chance)
                if random.random() < 0.005:
                    records.append(records[-1].copy())
        
        self.read_count += 1
        
        # Shuffle some records to simulate out-of-order arrival
        if len(records) > 10:
            num_shuffle = random.randint(1, min(5, len(records) // 10))
            indices = random.sample(range(len(records)), num_shuffle)
            for i in range(0, len(indices) - 1, 2):
                if i + 1 < len(indices):
                    idx1, idx2 = indices[i], indices[i + 1]
                    records[idx1], records[idx2] = records[idx2], records[idx1]
        
        # Add simulated latency
        time.sleep(random.uniform(0.01, 0.05))
        
        return pd.DataFrame(records)
    
    def get_batch_readings(
        self, 
        num_batches: int = 5, 
        batch_duration: int = 30,
        batch_interval: float = 1.0
    ) -> List[pd.DataFrame]:
        """
        Simulate multiple batches of sensor readings with potential failures.
        
        Args:
            num_batches: Number of batches to attempt
            batch_duration: Duration of each batch in seconds
            batch_interval: Interval between readings in each batch
        
        Returns:
            List of DataFrames (may be fewer than num_batches due to dropouts)
        """
        batches = []
        for i in range(num_batches):
            try:
                batch = self.read_sensors(batch_duration, batch_interval)
                batches.append(batch)
            except ConnectionError as e:
                # In real systems, connection errors happen - candidates must handle this
                print(f"Batch {i+1}/{num_batches} failed: {e}")
                continue
        
        return batches
