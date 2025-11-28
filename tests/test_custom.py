"""
Custom Tests for Error Handling and Edge Cases

These tests focus on validating proper error handling, edge cases,
and robustness of the data processing pipeline.

Run with: pytest tests/test_custom.py -v
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing import ingest_data, detect_anomalies, summarize_metrics


class TestIngestDataErrors:
    """Tests for error handling in ingest_data()."""
    
    def test_empty_list_raises_valueerror(self):
        """Should raise ValueError when data_batches is empty."""
        with pytest.raises(ValueError, match="data_batches cannot be empty"):
            ingest_data([])
    
    def test_non_dataframe_batch_raises_valueerror(self):
        """Should raise ValueError when batch is not a DataFrame."""
        with pytest.raises(ValueError, match="All batches must be pandas DataFrames"):
            ingest_data([{"not": "a dataframe"}])
    
    def test_mixed_invalid_batches_raises_valueerror(self):
        """Should raise ValueError when mixing valid and invalid batches."""
        valid_df = pd.DataFrame({
            "timestamp": [datetime.now()],
            "sensor": ["temperature"],
            "value": [65.0],
            "unit": ["°C"],
            "quality": ["GOOD"],
        })
        with pytest.raises(ValueError, match="All batches must be pandas DataFrames"):
            ingest_data([valid_df, "not a dataframe", valid_df])
    
    def test_all_empty_batches_raises_valueerror(self):
        """Should raise ValueError when all batches are empty DataFrames."""
        empty1 = pd.DataFrame()
        empty2 = pd.DataFrame()
        with pytest.raises(ValueError, match="All data batches are empty"):
            ingest_data([empty1, empty2])
    
    def test_missing_required_columns_raises_valueerror(self):
        """Should raise ValueError when required columns are missing."""
        incomplete_df = pd.DataFrame({
            "timestamp": [datetime.now()],
            "sensor": ["temperature"],
            # Missing: value, unit, quality
        })
        with pytest.raises(ValueError, match="Missing required columns"):
            ingest_data([incomplete_df])
    
    def test_missing_multiple_columns_raises_valueerror(self):
        """Should raise ValueError listing all missing columns."""
        minimal_df = pd.DataFrame({
            "timestamp": [datetime.now()],
            # Missing: sensor, value, unit, quality
        })
        with pytest.raises(ValueError, match="Missing required columns"):
            ingest_data([minimal_df])


class TestDetectAnomaliesErrors:
    """Tests for error handling in detect_anomalies()."""
    
    @pytest.fixture
    def valid_data(self):
        """Create valid test data."""
        timestamps = [datetime.now() + timedelta(seconds=i) for i in range(10)]
        return pd.DataFrame({
            "timestamp": timestamps,
            "sensor": ["temperature"] * 10,
            "value": [65.0 + i * 0.5 for i in range(10)],
            "unit": ["°C"] * 10,
            "quality": ["GOOD"] * 10,
        })
    
    def test_nonexistent_sensor_raises_valueerror(self, valid_data):
        """Should raise ValueError when sensor doesn't exist."""
        with pytest.raises(ValueError, match="Sensor 'nonexistent' not found"):
            detect_anomalies(valid_data, "nonexistent")
    
    def test_invalid_method_raises_valueerror(self, valid_data):
        """Should raise ValueError for unsupported method."""
        with pytest.raises(ValueError, match="Method 'invalid' not supported"):
            detect_anomalies(valid_data, "temperature", method="invalid")
    
    def test_insufficient_data_raises_valueerror(self):
        """Should raise ValueError when insufficient valid data points."""
        minimal_df = pd.DataFrame({
            "timestamp": [datetime.now()],
            "sensor": ["temperature"],
            "value": [65.0],
            "unit": ["°C"],
            "quality": ["GOOD"],
        })
        with pytest.raises(ValueError, match="Insufficient data"):
            detect_anomalies(minimal_df, "temperature")
    
    def test_all_nan_values_raises_valueerror(self):
        """Should raise ValueError when all values are NaN."""
        nan_df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(5)],
            "sensor": ["temperature"] * 5,
            "value": [np.nan] * 5,
            "unit": ["°C"] * 5,
            "quality": ["BAD"] * 5,
        })
        with pytest.raises(ValueError, match="Insufficient data"):
            detect_anomalies(nan_df, "temperature")
    
    def test_rolling_method_insufficient_data_raises_valueerror(self):
        """Should raise ValueError when not enough data for rolling window."""
        small_df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(3)],
            "sensor": ["temperature"] * 3,
            "value": [65.0, 66.0, 67.0],
            "unit": ["°C"] * 3,
            "quality": ["GOOD"] * 3,
        })
        with pytest.raises(ValueError, match="Insufficient data for rolling method"):
            detect_anomalies(small_df, "temperature", method="rolling")


class TestSummarizeMetricsErrors:
    """Tests for error handling in summarize_metrics()."""
    
    def test_empty_dataframe_raises_valueerror(self):
        """Should raise ValueError for empty DataFrame."""
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError, match="Data cannot be empty"):
            summarize_metrics(empty_df)
    
    def test_none_data_raises_valueerror(self):
        """Should raise ValueError when data is None."""
        with pytest.raises(ValueError, match="Data cannot be empty"):
            summarize_metrics(None)
    
    def test_invalid_group_by_column_raises_valueerror(self):
        """Should raise ValueError for non-existent group_by column."""
        valid_df = pd.DataFrame({
            "timestamp": [datetime.now()],
            "sensor": ["temperature"],
            "value": [65.0],
            "unit": ["°C"],
            "quality": ["GOOD"],
        })
        with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
            summarize_metrics(valid_df, group_by="nonexistent")
    
    def test_time_window_without_timestamp_raises_valueerror(self):
        """Should raise ValueError when time_window specified but no timestamp column."""
        no_timestamp_df = pd.DataFrame({
            "sensor": ["temperature"],
            "value": [65.0],
            "unit": ["°C"],
            "quality": ["GOOD"],
        })
        with pytest.raises(ValueError, match="must contain 'timestamp' column"):
            summarize_metrics(no_timestamp_df, time_window="1h")


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_single_valid_value_with_nans(self):
        """Should handle data with only one valid value among NaNs."""
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(5)],
            "sensor": ["temperature"] * 5,
            "value": [np.nan, np.nan, 65.0, np.nan, np.nan],
            "unit": ["°C"] * 5,
            "quality": ["BAD", "BAD", "GOOD", "BAD", "BAD"],
        })
        clean_data = ingest_data([df])
        # Should not crash, but anomaly detection should fail with insufficient data
        with pytest.raises(ValueError, match="Insufficient data"):
            detect_anomalies(clean_data, "temperature")
    
    def test_zero_variance_data_zscore(self):
        """Should handle constant values (zero variance) with z-score method."""
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(10)],
            "sensor": ["temperature"] * 10,
            "value": [65.0] * 10,  # All same value
            "unit": ["°C"] * 10,
            "quality": ["GOOD"] * 10,
        })
        clean_data = ingest_data([df])
        result = detect_anomalies(clean_data, "temperature", method="zscore")
        
        # No anomalies should be detected (all scores should be 0)
        assert result["is_anomaly"].sum() == 0
        assert (result["anomaly_score"] == 0.0).all()
    
    def test_zero_variance_data_iqr(self):
        """Should handle constant values (zero variance) with IQR method."""
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(10)],
            "sensor": ["temperature"] * 10,
            "value": [65.0] * 10,  # All same value
            "unit": ["°C"] * 10,
            "quality": ["GOOD"] * 10,
        })
        clean_data = ingest_data([df])
        result = detect_anomalies(clean_data, "temperature", method="iqr")
        
        # No anomalies should be detected
        assert result["is_anomaly"].sum() == 0
    
    def test_mixed_quality_flags(self):
        """Should handle data with mixed quality flags."""
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(6)],
            "sensor": ["temperature"] * 6,
            "value": [65.0, 66.0, 67.0, 68.0, 69.0, 70.0],
            "unit": ["°C"] * 6,
            "quality": ["GOOD", "BAD", "UNCERTAIN", "GOOD", "BAD", "GOOD"],
        })
        clean_data = ingest_data([df])
        metrics = summarize_metrics(clean_data, group_by="sensor")
        
        # Should have quality percentages
        temp_metrics = metrics["temperature"]
        assert "good_quality_pct" in temp_metrics
        assert "bad_quality_pct" in temp_metrics
        assert "uncertain_quality_pct" in temp_metrics
        assert temp_metrics["good_quality_pct"] == 50.0  # 3 out of 6
    
    def test_all_null_values_in_group(self):
        """Should handle groups where all values are null."""
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(4)],
            "sensor": ["temperature", "temperature", "pressure", "pressure"],
            "value": [np.nan, np.nan, 101.0, 102.0],
            "unit": ["°C", "°C", "kPa", "kPa"],
            "quality": ["BAD", "BAD", "GOOD", "GOOD"],
        })
        clean_data = ingest_data([df])
        metrics = summarize_metrics(clean_data, group_by="sensor")
        
        # Temperature group should have zero statistics
        temp_metrics = metrics["temperature"]
        assert temp_metrics["null_count"] == 2
        assert temp_metrics["mean"] == 0.0
        assert temp_metrics["std"] == 0.0
    
    def test_extreme_outlier_detection(self):
        """Should detect obvious outliers with z-score method."""
        # Use more realistic data with variance to test outlier detection
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(15)],
            "sensor": ["temperature"] * 15,
            "value": [65.0, 66.0, 64.5, 65.5, 66.5, 65.0, 150.0, 66.0, 65.5, 64.0, 66.0, 65.0, 65.5, 66.5, 64.5],
            "unit": ["°C"] * 15,
            "quality": ["GOOD"] * 15,
        })
        clean_data = ingest_data([df])
        
        # Z-score should detect the 150.0 outlier
        result = detect_anomalies(clean_data, "temperature", method="zscore", threshold=2.0)
        assert result["is_anomaly"].sum() >= 1, "Z-score should detect outlier"
        
        # Verify the outlier is actually the high value
        outliers = result[result["is_anomaly"] == True]
        assert any(outliers["value"] > 100), "Should flag the 150.0 value as anomaly"
    
    def test_multiple_sensors_anomaly_detection(self):
        """Should only add anomaly columns for specified sensor."""
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(10)],
            "sensor": ["temperature"] * 5 + ["pressure"] * 5,
            "value": [65.0 + i for i in range(5)] + [101.0 + i for i in range(5)],
            "unit": ["°C"] * 5 + ["kPa"] * 5,
            "quality": ["GOOD"] * 10,
        })
        clean_data = ingest_data([df])
        result = detect_anomalies(clean_data, "temperature", method="zscore")
        
        # Temperature rows should have detection_method set
        temp_rows = result[result["sensor"] == "temperature"]
        assert all(temp_rows["detection_method"] == "zscore")
        
        # Pressure rows should have empty detection_method
        pressure_rows = result[result["sensor"] == "pressure"]
        assert all(pressure_rows["detection_method"] == "")
    
    def test_time_window_aggregation(self):
        """Should properly aggregate metrics by time window."""
        timestamps = [datetime(2025, 1, 1, 0, i, 0) for i in range(10)]
        df = pd.DataFrame({
            "timestamp": timestamps,
            "sensor": ["temperature"] * 10,
            "value": [65.0 + i for i in range(10)],
            "unit": ["°C"] * 10,
            "quality": ["GOOD"] * 10,
        })
        clean_data = ingest_data([df])
        metrics = summarize_metrics(clean_data, group_by="sensor", time_window="5min")
        
        # Should have time-indexed groups
        assert isinstance(metrics, dict)
        assert len(metrics) > 0
        
        # Each time key should have sensor groups
        for time_key, sensor_groups in metrics.items():
            assert "temperature" in sensor_groups


class TestDataIntegrity:
    """Tests for data integrity and consistency."""
    
    def test_ingest_preserves_valid_data(self):
        """Should preserve all valid data after ingestion."""
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(5)],
            "sensor": ["temperature"] * 5,
            "value": [65.0, 66.0, 67.0, 68.0, 69.0],
            "unit": ["°C"] * 5,
            "quality": ["GOOD"] * 5,
        })
        result = ingest_data([df])
        assert len(result) == 5
        assert all(result["sensor"] == "temperature")
    
    def test_anomaly_detection_preserves_data_length(self):
        """Should return same number of rows as input."""
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(10)],
            "sensor": ["temperature"] * 5 + ["pressure"] * 5,
            "value": [65.0 + i for i in range(5)] + [101.0 + i for i in range(5)],
            "unit": ["°C"] * 5 + ["kPa"] * 5,
            "quality": ["GOOD"] * 10,
        })
        clean_data = ingest_data([df])
        result = detect_anomalies(clean_data, "temperature")
        
        assert len(result) == len(clean_data)
    
    def test_metrics_accuracy(self):
        """Should compute accurate statistics."""
        df = pd.DataFrame({
            "timestamp": [datetime.now() + timedelta(seconds=i) for i in range(5)],
            "sensor": ["temperature"] * 5,
            "value": [10.0, 20.0, 30.0, 40.0, 50.0],
            "unit": ["°C"] * 5,
            "quality": ["GOOD"] * 5,
        })
        clean_data = ingest_data([df])
        metrics = summarize_metrics(clean_data, group_by="sensor")
        
        temp_metrics = metrics["temperature"]
        assert temp_metrics["count"] == 5
        assert temp_metrics["mean"] == 30.0
        assert temp_metrics["min"] == 10.0
        assert temp_metrics["max"] == 50.0
        assert temp_metrics["median"] == 30.0
        assert temp_metrics["null_count"] == 0
        assert temp_metrics["good_quality_pct"] == 100.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
