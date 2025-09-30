#!/usr/bin/env python3
"""
Test different Zyte API approaches
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

ZYTE_API_KEY = os.getenv('ZYTE_API_KEY')

def test_zyte_api_extract():
    """Test Zyte API extract endpoint."""
    print("\n1. Testing Zyte API (Extract endpoint)...")
    print("-" * 60)
    
    api_url = "https://api.zyte.com/v1/extract"
    payload = {
        "url": "https://techcrunch.com/",
        "browserHtml": True,
    }
    
    try:
        response = requests.post(
            api_url,
            auth=(ZYTE_API_KEY, ''),
            json=payload,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            html = data.get('browserHtml', '')
            print(f"✓ Success! HTML length: {len(html)}")
        else:
            print(f"✗ Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")


def test_smart_proxy_manager():
    """Test Zyte Smart Proxy Manager (formerly Crawlera)."""
    print("\n2. Testing Smart Proxy Manager...")
    print("-" * 60)
    
    # Smart Proxy Manager uses proxy configuration
    proxy_url = f"http://{ZYTE_API_KEY}:@proxy.crawlera.com:8011"
    
    proxies = {
        'http': proxy_url,
        'https': proxy_url,
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(
            'https://techcrunch.com/',
            proxies=proxies,
            headers=headers,
            timeout=30,
            verify=False  # SPM handles SSL
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✓ Success! HTML length: {len(response.text)}")
        else:
            print(f"✗ Error: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")


def test_zyte_api_autoextract():
    """Test Zyte Automatic Extraction API."""
    print("\n3. Testing Zyte Automatic Extraction...")
    print("-" * 60)
    
    api_url = "https://autoextract.zyte.com/v1/extract"
    payload = {
        "url": "https://techcrunch.com/",
        "pageType": "article"
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            api_url,
            auth=(ZYTE_API_KEY, ''),
            json=[payload],  # Autoextract expects array
            headers=headers,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Response: {data}")
        else:
            print(f"✗ Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")


if __name__ == '__main__':
    print("=" * 60)
    print("TESTING ZYTE INTEGRATION")
    print("=" * 60)
    print(f"API Key: ***{ZYTE_API_KEY[-8:] if ZYTE_API_KEY else 'NOT SET'}")
    
    test_zyte_api_extract()
    test_smart_proxy_manager()
    test_zyte_api_autoextract()
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)
