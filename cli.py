#!/usr/bin/env python3
"""
Interactive CLI for phone number lookup
"""
from main import PhoneNumberLookup


def main():
    lookup = PhoneNumberLookup()
    
    print("=" * 60)
    print("📞 Phone Number Lookup Tool - Interactive Mode")
    print("=" * 60)
    print()
    
    if not lookup.api.has_api_keys():
        print("⚠️  No API keys configured.")
        print("   Results will be limited to location data from local database.")
        print("   See README.md for API setup instructions.")
        print()
    
    print("Enter phone numbers to lookup (or 'quit' to exit)")
    print("Examples: +1 (415) 555-0123, 2125551234, +54 11 1234 5678")
    print()
    
    while True:
        try:
            phone_number = input("📞 Enter phone number: ").strip()
            
            if phone_number.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            if not phone_number:
                continue
            
            print()
            result = lookup.search(phone_number)
            print(lookup.format_result(result))
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
