import pandas as pd
import pgeocode
import time
from typing import List
import sys
import os

# Add the parent directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.weather import get_weather_data

def get_utah_zip_codes() -> List[str]:
    """Get all ZIP codes for Utah"""
    # Utah ZIP code ranges (approximate)
    utah_ranges = [
        (84001, 84799),  # Main Utah ZIP range
        (85000, 85099),  # Additional Utah ZIP range
        (86001, 86099)   # Additional Utah ZIP range
    ]
    
    nomi = pgeocode.Nominatim('us')
    utah_zips = []
    
    # Test each ZIP in the ranges
    for start, end in utah_ranges:
        for zip_code in range(start, end + 1):
            zip_str = str(zip_code).zfill(5)
            location = nomi.query_postal_code(zip_str)
            if not pd.isna(location.state_code) and location.state_code == 'UT':
                utah_zips.append(zip_str)
                print(f"Found valid Utah ZIP: {zip_str}")
    
    return utah_zips

def main():
    print("Fetching Utah ZIP codes...")
    zip_codes = get_utah_zip_codes()
    print(f"Found {len(zip_codes)} ZIP codes in Utah")
    
    success_count = 0
    error_count = 0
    
    for i, zip_code in enumerate(zip_codes, 1):
        print(f"\nProcessing {i}/{len(zip_codes)}: {zip_code}")
        
        try:
            result = get_weather_data(zip_code)
            if result:
                success_count += 1
                print(f"✓ Successfully fetched data for {zip_code}")
                print(f"  Location: {result['metadata']['latitude']:.4f}°N, {result['metadata']['longitude']:.4f}°W")
                print(f"  Temperature range: {min(result['hourly_temperatures']):.1f}°F to {max(result['hourly_temperatures']):.1f}°F")
            else:
                error_count += 1
                print(f"✗ Failed to fetch data for {zip_code}")
            
            # Sleep briefly between requests to be nice to the API
            time.sleep(1)
            
        except Exception as e:
            error_count += 1
            print(f"✗ Error processing {zip_code}: {str(e)}")
    
    print(f"\nComplete! Successfully fetched {success_count} ZIP codes, {error_count} errors")

if __name__ == "__main__":
    main()
