# OBJECTIVE: Ship a minimal CSV export feature for user data within 48 hours
# TERRAIN:
#   - Constraints: Python 3.8+, no external libs, single-file deployment
#   - Environment: Legacy monolith with no test coverage for data layer
#   - Codebase: 12-year-old codebase with circular imports in core modules
# FORCES:
#   - Tools: Git, pytest, standard library csv module
#   - Time: 48 hours total (8h dev, 8h review, 24h buffer)
#   - Resources: 1 senior dev, 1 junior dev (50% capacity)
# ENEMY:
#   - Legacy data model breaks on datetime fields
#   - Circular imports prevent direct data access
# PLAN:
#   Phase 1 (0-8h): Recon - create isolated data extractor module
#   Phase 2 (8-16h): Secure - implement CSV writer with fallback to JSON
#   Phase 3 (16-24h): Validate - run against production dataset snapshot
# RESERVE:
#   Fallback position: Export to JSON if CSV fails due to legacy constraints
#   Flanking path: Use database dump as raw data source if ORM fails

import csv
import json
from datetime import datetime
from typing import List, Dict, Any

class DataExtractor:
    """Isolated data extraction to avoid circular imports"""
    def __init__(self):
        self._data = []

    def fetch_user_data(self) -> List[Dict[str, Any]]:
        """Mock data fetch that simulates legacy system constraints"""
        # Simulate legacy datetime serialization issue
        return [
            {"id": 1, "name": "Alice", "created": datetime(2020, 1, 1)},
            {"id": 2, "name": "Bob", "created": datetime(2021, 5, 15)}
        ]

class CSVExporter:
    """Primary export strategy with datetime handling"""
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def export(self, path: str) -> bool:
        try:
            with open(path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
                writer.writeheader()
                for row in self.data:
                    # Handle datetime serialization
                    clean_row = {k: v.isoformat() if isinstance(v, datetime) else v
                                for k, v in row.items()}
                    writer.writerow(clean_row)
            return True
        except Exception as e:
            print(f"CSV export failed: {e}")
            return False

class JSONExporter:
    """Fallback export strategy"""
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def export(self, path: str) -> bool:
        try:
            with open(path, 'w') as f:
                json.dump(self.data, f, default=str)
            return True
        except Exception as e:
            print(f"JSON export failed: {e}")
            return False

def campaign_plan():
    # Phase 1: Recon - establish data pipeline
    extractor = DataExtractor()
    raw_data = extractor.fetch_user_data()

    # Phase 2: Secure - attempt primary export
    csv_exporter = CSVExporter(raw_data)
    csv_success = csv_exporter.export('user_data.csv')

    if csv_success:
        print("Primary CSV export successful")
        return True

    # Phase 3: Validate - fallback to JSON if CSV fails
    json_exporter = JSONExporter(raw_data)
    json_success = json_exporter.export('user_data.json')

    if json_success:
        print("Fallback JSON export successful")
        return True

    print("Both export strategies failed")
    return False

if __name__ == "__main__":
    success = campaign_plan()
    print(f"Campaign {'SUCCEEDED' if success else 'FAILED'}")