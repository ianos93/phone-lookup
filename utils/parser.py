"""
Phone number parsing and validation utilities
"""
import re
from typing import Optional, Dict


def clean_phone_number(phone: str) -> str:
    """Remove all non-numeric characters from phone number"""
    return re.sub(r'\D', '', phone)


def parse_phone_number(phone: str) -> Optional[Dict[str, str]]:
    """
    Parse phone number into components
    Returns dict with country_code, area_code, and local_number
    """
    cleaned = clean_phone_number(phone)
    
    if not cleaned:
        return None
    
    # Handle different formats
    if len(cleaned) == 10:  # Assume US/Canada without country code
        return {
            'country_code': '1',
            'area_code': cleaned[:3],
            'local_number': cleaned[3:]
        }
    elif len(cleaned) == 11 and cleaned[0] == '1':  # US/Canada with country code
        return {
            'country_code': '1',
            'area_code': cleaned[1:4],
            'local_number': cleaned[4:]
        }
    elif len(cleaned) >= 10:  # International format
        # Try to detect country code (1-3 digits)
        for cc_length in [1, 2, 3]:
            country_code = cleaned[:cc_length]
            remaining = cleaned[cc_length:]
            if len(remaining) >= 7:  # Minimum local number length
                # Extract area code (2-4 digits typically)
                area_code_length = min(4, len(remaining) - 6)
                area_code = remaining[:area_code_length]
                local_number = remaining[area_code_length:]
                
                return {
                    'country_code': country_code,
                    'area_code': area_code,
                    'local_number': local_number
                }
    
    return None


def format_phone_number(parsed: Dict[str, str]) -> str:
    """Format parsed phone number for display"""
    country = parsed.get('country_code', '')
    area = parsed.get('area_code', '')
    local = parsed.get('local_number', '')
    
    if country == '1' and len(local) == 7:
        # US/Canada format: +1 (XXX) XXX-XXXX
        return f"+{country} ({area}) {local[:3]}-{local[3:]}"
    else:
        # International format: +CC (AREA) LOCAL
        return f"+{country} ({area}) {local}"


def validate_phone_number(phone: str) -> bool:
    """Basic validation of phone number"""
    cleaned = clean_phone_number(phone)
    return len(cleaned) >= 10 and cleaned.isdigit()
