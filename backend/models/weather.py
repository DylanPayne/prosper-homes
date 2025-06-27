import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests
import pandas as pd
import pgeocode
from config.debug_config import debug_print, DebugLevel

# Constants
WEATHER_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/weather_data.json")
OPEN_METEO_API = "https://archive-api.open-meteo.com/v1/archive"

def get_coordinates(zip_code: str) -> Optional[Dict[str, float]]:
    """
    Fetch latitude and longitude for a given ZIP code using pgeocode.
    
    Args:
        zip_code: US ZIP code
        
    Returns:
        Dictionary with latitude and longitude, or None if the lookup fails.
    """
    try:
        nomi = pgeocode.Nominatim("us")
        location = nomi.query_postal_code(zip_code)
        
        if location is not None and not location.empty:
            return {"latitude": location.latitude, "longitude": location.longitude}
        else:
            debug_print(f"Failed to find coordinates for ZIP {zip_code}", DebugLevel.ERROR, "weather")
            return None
    except Exception as e:
        debug_print(f"Error fetching coordinates: {str(e)}", DebugLevel.ERROR, "weather")
        return None

def fetch_weather_data(zip_code: str, year: int) -> Optional[Dict[str, Any]]:
    """
    Fetch weather data for a specific ZIP code and year.
    
    Args:
        zip_code: US ZIP code
        year: Year to fetch data for
        
    Returns:
        Dictionary containing weather data and metadata, or None if the fetch fails.
    """
    debug_print(f"Fetching weather data for ZIP {zip_code}, year {year}", DebugLevel.INFO, "weather")
    
    # Get coordinates for the ZIP code
    coordinates = get_coordinates(zip_code)
    if not coordinates:
        return None
    
    lat = coordinates["latitude"]
    lon = coordinates["longitude"]
    
    # Calculate date range for the specified year
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
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
        
        hourly_temps = data["hourly"]["temperature_2m"]
        hourly_data = []
        
        # Create hourly_data with datetime and temperature
        for i, temp in enumerate(hourly_temps):
            hour_datetime = data["hourly"]["time"][i]
            hourly_data.append({
                "datetime": hour_datetime,
                "temperature": temp
            })
        
        weather_data = {
            "metadata": {
                "latitude": lat,
                "longitude": lon,
                "fetched_at": datetime.now().isoformat(),
                "zip_code": zip_code,
                "year": year
            },
            "hourly_data": hourly_data
        }
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        debug_print(f"Error fetching weather data: {str(e)}", DebugLevel.ERROR, "weather")
        return None

def save_weather_to_csv(zip_code: str, year: int, output_dir: Optional[str] = None) -> str:
    """
    Fetch and save hourly weather data to a CSV file.
    
    Args:
        zip_code: US ZIP code
        year: Year to fetch data for
        output_dir: Optional directory to save the CSV file
        
    Returns:
        Path to the saved CSV file, or an empty string if saving fails.
    """
    debug_print(f"Saving weather data for ZIP {zip_code}, year {year} to CSV", DebugLevel.INFO, "weather")
    
    # Fetch the weather data
    weather_data = fetch_weather_data(zip_code, year)
    if not weather_data:
        debug_print("Failed to fetch weather data", DebugLevel.ERROR, "weather")
        return ""
    
    # Create output directory if needed
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename
    csv_filename = f"weather_{zip_code}_{year}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    try:
        # Convert to DataFrame and save
        df = pd.DataFrame(weather_data["hourly_data"])
        df.to_csv(csv_path, index=False)
        debug_print(f"Successfully saved weather data to {csv_path}", DebugLevel.INFO, "weather")
        return csv_path
    except Exception as e:
        debug_print(f"Error saving CSV file: {str(e)}", DebugLevel.ERROR, "weather")
        return ""