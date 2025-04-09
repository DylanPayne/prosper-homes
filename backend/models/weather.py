import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any

import requests

from config.debug_config import debug_print, debug_json, DebugLevel

# Constants
WEATHER_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/weather_data.json")
OPEN_METEO_API = "https://archive-api.open-meteo.com/v1/archive"
PARK_CITY_LAT = 40.6461
PARK_CITY_LON = -111.4980

# Use 2024 as our reference year
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"

def fetch_park_city_weather() -> Dict[str, Any]:
    """
    Fetch weather data for Park City, Utah and use it as default data
    """
    debug_print("Fetching Park City weather data", DebugLevel.INFO, "weather")
    
    params = {
        "latitude": PARK_CITY_LAT,
        "longitude": PARK_CITY_LON,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hourly": "temperature_2m",
        "temperature_unit": "fahrenheit",
        "timezone": "America/Denver"
    }
    
    try:
        response = requests.get(OPEN_METEO_API, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'hourly' not in data or 'temperature_2m' not in data['hourly']:
            debug_print("Error: Unexpected API response format", DebugLevel.ERROR, "weather")
            return None
        
        weather_data = {
            "metadata": {
                "latitude": PARK_CITY_LAT,
                "longitude": PARK_CITY_LON,
                "fetched_at": datetime.now().isoformat()
            },
            "hourly_temperatures": data["hourly"]["temperature_2m"]
        }
        
        # Save to file
        with open(WEATHER_DATA_FILE, 'w') as f:
            json.dump({"84060": weather_data}, f, indent=2)
            
        debug_print(f"Successfully saved Park City weather data ({len(weather_data['hourly_temperatures'])} readings)", 
                   DebugLevel.INFO, "weather")
        return weather_data
        
    except Exception as e:
        debug_print(f"Error fetching weather data: {str(e)}", DebugLevel.ERROR, "weather")
        return None

def get_weather_data(zip_code: str = "84060") -> Dict[str, Any]:
    """
    Get weather data - currently returns Park City data for all ZIP codes
    
    Args:
        zip_code: US ZIP code (currently ignored - always returns Park City data)
        
    Returns:
        Dictionary containing Park City weather data and metadata
    """
    try:
        # Try to load existing data
        if os.path.exists(WEATHER_DATA_FILE):
            with open(WEATHER_DATA_FILE, 'r') as f:
                data = json.load(f)
                park_city_data = data.get("84060")
                
                # Check if data exists and is not too old (24 hours)
                if park_city_data:
                    fetched_at = datetime.fromisoformat(park_city_data["metadata"]["fetched_at"])
                    age_hours = (datetime.now() - fetched_at).total_seconds() / 3600
                    
                    if age_hours < 24:
                        debug_print("Using cached Park City weather data", DebugLevel.DEBUG, "weather")
                        return park_city_data
        
        # If we get here, either file doesn't exist, data is missing, or too old
        return fetch_park_city_weather()
        
    except Exception as e:
        debug_print(f"Error getting weather data: {str(e)}", DebugLevel.ERROR, "weather")
        return None

if __name__ == '__main__':
    # Example usage
    result = get_weather_data()
    if result:
        temps = result['hourly_temperatures']
        print(f"Successfully loaded weather data with {len(temps)} temperature readings")
        print(f"Temperature range: {min(temps):.1f}°F to {max(temps):.1f}°F")
        print(f"First 24 hours: {temps[:24]}")
    else:
        print("Failed to load weather data")
