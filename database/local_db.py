"""
Local database lookup for area codes and basic information
"""
import json
import os
from typing import Optional, Dict


class LocalDatabase:
    def __init__(self, db_path: str = None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, '..', 'database', 'area_codes.json')
        
        self.db_path = db_path
        self.data = self._load_database()
    
    def _load_database(self) -> dict:
        """Load the area code database"""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Database file not found at {self.db_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in database file")
            return {}
    
    def lookup(self, country_code: str, area_code: str) -> Optional[Dict[str, str]]:
        """
        Look up area code information in local database
        Returns dict with location and timezone info
        """
        if country_code not in self.data:
            return None
        
        country_data = self.data[country_code]
        area_codes = country_data.get('area_codes', {})
        
        if area_code not in area_codes:
            return None
        
        result = area_codes[area_code].copy()
        result['country'] = country_data.get('country', 'Unknown')
        result['source'] = 'local_database'
        
        return result
    
    def get_country_name(self, country_code: str) -> Optional[str]:
        """Get country name for a country code"""
        if country_code in self.data:
            return self.data[country_code].get('country')
        return None
