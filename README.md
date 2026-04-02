# 📞 Phone Number Lookup Tool

A Python-based phone number lookup tool that retrieves carrier information, location data, and line status. Features automatic fallback from API lookup to local database when API keys are unavailable.

## Features

- ✅ **Carrier Information**: Identify the phone carrier/operator
- 📍 **Location Data**: Get city, region, and country information
- 🔌 **Line Status**: Check if the number is active, disconnected, or invalid
- 🌐 **International Support**: Works with phone numbers from multiple countries
- 🔄 **Smart Fallback**: Automatically falls back to local database when API is unavailable
- 🆓 **Free Tier Support**: Works with free API tiers from multiple providers

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **(Optional) Configure API Keys**:

The tool works without API keys using the local database, but for full functionality (carrier info, line status), sign up for one of these free APIs:

### Recommended APIs (Choose One or More)

#### Option 1: Numverify (100 requests/month free)
- Sign up: https://numverify.com/
- Set environment variable:
```bash
export NUMVERIFY_API_KEY="your_api_key_here"
```

#### Option 2: AbstractAPI (250 requests/month free)
- Sign up: https://www.abstractapi.com/phone-validation-api
- Set environment variable:
```bash
export ABSTRACTAPI_KEY="your_api_key_here"
```

#### Option 3: APILayer (100 requests/month free)
- Sign up: https://apilayer.com/marketplace/number_verification-api
- Set environment variable:
```bash
export APILAYER_KEY="your_api_key_here"
```

## Usage

### Basic Usage

Run the example program:
```bash
python main.py
```

### Interactive Mode

Run the interactive CLI:
```bash
python cli.py
```

### Using as a Library

```python
from main import PhoneNumberLookup

# Initialize the lookup tool
lookup = PhoneNumberLookup()

# Search for a phone number
result = lookup.search("+1 (415) 555-0123")

# Display formatted results
print(lookup.format_result(result))

# Or access data programmatically
if result['success']:
    print(f"Carrier: {result.get('carrier')}")
    print(f"Location: {result.get('location')}")
    print(f"Is Active: {result.get('is_active')}")
```

### Supported Phone Number Formats

The tool accepts various formats:
- `+1 (415) 555-0123`
- `14155550123`
- `415-555-0123`
- `+54 11 1234 5678`
- Any format with country code

## Project Structure

```
phone-lookup/
├── api/
│   └── lookup.py           # API integrations (Numverify, AbstractAPI, etc.)
├── database/
│   ├── area_codes.json     # Local area code database
│   └── local_db.py         # Local database lookup module
├── utils/
│   └── parser.py           # Phone number parsing utilities
├── main.py                 # Main lookup module and CLI
├── cli.py                  # Interactive CLI
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## How It Works

1. **Validation**: Phone number is validated and parsed into components (country code, area code, local number)

2. **API Lookup**: If API keys are configured, the tool queries the API for:
   - Carrier/operator name
   - Line type (mobile, landline, VoIP)
   - Active status
   - Precise location data

3. **Local Fallback**: If no API keys are available or API fails:
   - Looks up area code in local database
   - Returns country and general location
   - Indicates that API key is needed for full details

4. **Results**: Returns comprehensive information in a structured format

## Data Sources

### With API (Full Information):
- ✅ Carrier name
- ✅ Line type (mobile/landline/VoIP)
- ✅ Active status verification
- ✅ Precise location
- ✅ Country information

### Local Database Only (Limited):
- ✅ Country information
- ✅ General location (city/region)
- ✅ Timezone
- ❌ Carrier name (requires API)
- ❌ Active status (requires API)
- ❌ Line type (requires API)

## Expanding the Local Database

To add more area codes to the local database, edit `database/area_codes.json`:

```json
{
  "1": {
    "country": "United States/Canada",
    "area_codes": {
      "415": {"location": "San Francisco, CA", "timezone": "PST"}
    }
  }
}
```

## Example Output

```
============================================================
📞 PHONE NUMBER LOOKUP RESULTS
============================================================
Number: +1 (415) 555-0123
Valid: True

📍 LOCATION INFORMATION
  Country: United States
  Location: San Francisco, CA
  Timezone: PST

📱 CARRIER INFORMATION
  Carrier: AT&T
  Line Type: mobile
  Is Active: True

ℹ️  METADATA
  Data Source: numverify
============================================================
```

## API Rate Limits

- **Numverify Free**: 100 requests/month
- **AbstractAPI Free**: 250 requests/month  
- **APILayer Free**: 100 requests/month

The tool automatically tries multiple APIs if one fails or reaches its limit.

## Privacy & Legal

- This tool is for legitimate lookup purposes only
- Respect privacy laws in your jurisdiction
- Do not use for harassment, spam, or unauthorized contact
- Some countries have restrictions on phone number lookup services

## Contributing

To add more area codes or improve the local database:
1. Edit `database/area_codes.json`
2. Follow the existing JSON structure
3. Include location and timezone information

## Troubleshooting

### "No API keys configured" warning
- This is normal if you haven't set up API keys
- The tool will still work with limited local database information
- Set at least one API key for full functionality

### API errors
- Check that your API key is valid
- Verify you haven't exceeded rate limits
- Try a different API provider

### Invalid phone number
- Ensure the number includes country code
- Check that the format is valid (at least 10 digits)
- Try different formatting: `+1234567890` or `(123) 456-7890`

## License

MIT License - Feel free to use and modify as needed.

## Credits

- Uses free tier APIs from Numverify, AbstractAPI, and APILayer
- Local database compiled from public area code information
