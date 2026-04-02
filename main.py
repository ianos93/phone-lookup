"""
Main phone lookup module with API and local database fallback
"""
from typing import Dict, Optional
from utils.parser import parse_phone_number, format_phone_number, validate_phone_number
from database.local_db import LocalDatabase
from api.lookup import PhoneLookupAPI


class PhoneNumberLookup:
    def __init__(self):
        self.api = PhoneLookupAPI()
        self.local_db = LocalDatabase()
    
    def search(self, phone_number: str) -> Dict:
        """
        Search for phone number information
        Tries API first, falls back to local database
        """
        # Validate phone number
        if not validate_phone_number(phone_number):
            return {
                'success': False,
                'error': 'Invalid phone number format',
                'phone_number': phone_number
            }
        
        # Parse phone number
        parsed = parse_phone_number(phone_number)
        if not parsed:
            return {
                'success': False,
                'error': 'Could not parse phone number',
                'phone_number': phone_number
            }
        
        formatted = format_phone_number(parsed)
        
        # Try API lookup first
        api_result = None
        if self.api.has_api_keys():
            api_result = self.api.lookup(phone_number)
        
        if api_result:
            return {
                'success': True,
                'phone_number': formatted,
                'valid': api_result.get('valid', True),
                'country': api_result.get('country'),
                'country_code': api_result.get('country_code'),
                'location': api_result.get('location'),
                'carrier': api_result.get('carrier'),
                'line_type': api_result.get('line_type'),
                'local_format': api_result.get('local_format'),
                'international_format': api_result.get('international_format'),
                'is_active': api_result.get('valid', False),
                'data_source': api_result.get('source')
            }
        
        # Fallback to local database
        local_result = self.local_db.lookup(
            parsed['country_code'],
            parsed['area_code']
        )
        
        if local_result:
            return {
                'success': True,
                'phone_number': formatted,
                'valid': True,  # We can't verify without API
                'country': local_result.get('country'),
                'country_code': parsed['country_code'],
                'location': local_result.get('location'),
                'timezone': local_result.get('timezone'),
                'carrier': 'Unknown (API key required)',
                'line_type': 'Unknown (API key required)',
                'is_active': 'Unknown (API key required)',
                'data_source': 'local_database',
                'note': 'Limited information - configure API key for full details'
            }
        
        # No data found
        country_name = self.local_db.get_country_name(parsed['country_code'])
        return {
            'success': True,
            'phone_number': formatted,
            'valid': 'Unknown',
            'country': country_name or f"Country code +{parsed['country_code']}",
            'country_code': parsed['country_code'],
            'location': 'Unknown',
            'carrier': 'Unknown (API key required)',
            'line_type': 'Unknown',
            'is_active': 'Unknown (API key required)',
            'data_source': 'limited',
            'note': 'Area code not in local database - configure API key for details'
        }
    
    def format_result(self, result: Dict) -> str:
        """Format lookup result for display"""
        if not result.get('success'):
            return f"❌ Error: {result.get('error')}\n"
        
        output = []
        output.append("=" * 60)
        output.append("📞 PHONE NUMBER LOOKUP RESULTS")
        output.append("=" * 60)
        output.append(f"Number: {result.get('phone_number')}")
        output.append(f"Valid: {result.get('valid')}")
        output.append("")
        
        output.append("📍 LOCATION INFORMATION")
        output.append(f"  Country: {result.get('country', 'Unknown')}")
        output.append(f"  Location: {result.get('location', 'Unknown')}")
        if result.get('timezone'):
            output.append(f"  Timezone: {result.get('timezone')}")
        output.append("")
        
        output.append("📱 CARRIER INFORMATION")
        output.append(f"  Carrier: {result.get('carrier', 'Unknown')}")
        output.append(f"  Line Type: {result.get('line_type', 'Unknown')}")
        output.append(f"  Is Active: {result.get('is_active', 'Unknown')}")
        output.append("")
        
        output.append("ℹ️  METADATA")
        output.append(f"  Data Source: {result.get('data_source', 'unknown')}")
        if result.get('note'):
            output.append(f"  Note: {result.get('note')}")
        
        output.append("=" * 60)
        
        return "\n".join(output)


def main():
    """Example usage"""
    lookup = PhoneNumberLookup()
    
    # Example phone numbers to test
    test_numbers = [
        "+1 (415) 555-0123",  # San Francisco
        "2125551234",          # New York
        "+54 11 1234 5678",    # Buenos Aires, Argentina
    ]
    
    print("\n🔍 Phone Number Lookup Tool\n")
    
    # Check if API keys are configured
    if not lookup.api.has_api_keys():
        print("⚠️  No API keys configured. Results will be limited to local database.")
        print("   Set environment variables: NUMVERIFY_API_KEY, ABSTRACTAPI_KEY, or APILAYER_KEY")
        print("   See README.md for API signup links.\n")
    
    for number in test_numbers:
        result = lookup.search(number)
        print(lookup.format_result(result))
        print()


if __name__ == "__main__":
    main()
