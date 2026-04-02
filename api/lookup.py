"""
API integrations for phone number lookup
Supports multiple providers with automatic fallback
"""
import os
import requests
from typing import Optional, Dict
from enum import Enum


class APIProvider(Enum):
    NUMVERIFY = "numverify"
    ABSTRACT_API = "abstractapi"
    APILAYER = "apilayer"


class PhoneLookupAPI:
    def __init__(self):
        # Load API keys from environment variables
        self.numverify_key = os.getenv('NUMVERIFY_API_KEY')
        self.abstract_key = os.getenv('ABSTRACTAPI_KEY')
        self.apilayer_key = os.getenv('APILAYER_KEY')
    
    def lookup_numverify(self, phone_number: str) -> Optional[Dict]:
        """
        Lookup using Numverify API
        Free tier: 100 requests/month
        Sign up: https://numverify.com/
        """
        if not self.numverify_key:
            return None
        
        try:
            url = "http://apilayer.net/api/validate"
            params = {
                'access_key': self.numverify_key,
                'number': phone_number,
                'country_code': '',
                'format': 1
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if data.get('valid'):
                return {
                    'valid': data.get('valid', False),
                    'number': data.get('number'),
                    'local_format': data.get('local_format'),
                    'international_format': data.get('international_format'),
                    'country': data.get('country_name'),
                    'country_code': data.get('country_code'),
                    'location': data.get('location'),
                    'carrier': data.get('carrier'),
                    'line_type': data.get('line_type'),
                    'source': 'numverify'
                }
        except Exception as e:
            print(f"Numverify API error: {e}")
        
        return None
    
    def lookup_abstractapi(self, phone_number: str) -> Optional[Dict]:
        """
        Lookup using AbstractAPI
        Free tier: 250 requests/month
        Sign up: https://www.abstractapi.com/phone-validation-api
        """
        if not self.abstract_key:
            return None
        
        try:
            url = "https://phonevalidation.abstractapi.com/v1/"
            params = {
                'api_key': self.abstract_key,
                'phone': phone_number
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if data.get('valid'):
                return {
                    'valid': data.get('valid', False),
                    'number': data.get('phone'),
                    'local_format': data.get('local_format'),
                    'international_format': data.get('international_format'),
                    'country': data.get('country', {}).get('name'),
                    'country_code': data.get('country', {}).get('code'),
                    'location': data.get('location'),
                    'carrier': data.get('carrier'),
                    'line_type': data.get('type'),
                    'source': 'abstractapi'
                }
        except Exception as e:
            print(f"AbstractAPI error: {e}")
        
        return None
    
    def lookup_apilayer(self, phone_number: str) -> Optional[Dict]:
        """
        Lookup using APILayer (newer numverify)
        Free tier: 100 requests/month
        Sign up: https://apilayer.com/marketplace/number_verification-api
        """
        if not self.apilayer_key:
            return None
        
        try:
            url = f"https://api.apilayer.com/number_verification/validate"
            params = {'number': phone_number}
            headers = {'apikey': self.apilayer_key}
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            data = response.json()
            
            if data.get('valid'):
                return {
                    'valid': data.get('valid', False),
                    'number': data.get('number'),
                    'local_format': data.get('local_format'),
                    'international_format': data.get('international_format'),
                    'country': data.get('country_name'),
                    'country_code': data.get('country_code'),
                    'location': data.get('location'),
                    'carrier': data.get('carrier'),
                    'line_type': data.get('line_type'),
                    'source': 'apilayer'
                }
        except Exception as e:
            print(f"APILayer error: {e}")
        
        return None
    
    def lookup(self, phone_number: str, preferred_provider: Optional[APIProvider] = None) -> Optional[Dict]:
        """
        Lookup phone number using available APIs with fallback
        Tries preferred provider first, then falls back to others
        """
        providers = [
            self.lookup_numverify,
            self.lookup_abstractapi,
            self.lookup_apilayer
        ]
        
        # Try each provider until one succeeds
        for provider_func in providers:
            result = provider_func(phone_number)
            if result:
                return result
        
        return None
    
    def has_api_keys(self) -> bool:
        """Check if any API keys are configured"""
        return any([self.numverify_key, self.abstract_key, self.apilayer_key])
