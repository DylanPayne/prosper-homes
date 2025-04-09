import os
import sys

# Add the parent directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.energy_model import Building, HeatingSystem, CoolingSystem, calculate_energy_consumption
from config.debug_config import DEBUG_CONFIG, DebugLevel

def main():
    # Create a test building
    building = Building(
        square_footage=2000,
        num_floors=2,
        ceiling_height=8.0,
        r_value=13.0,
        ach=1.0
    )
    
    # Calculate heating energy at 30°F
    results = calculate_energy_consumption(
        building=building,
        heating_system=HeatingSystem.GAS_FURNACE,
        cooling_system=None,
        outdoor_temp=30,
        mode="heating"
    )
    
    # Calculate cooling energy at 90°F
    results = calculate_energy_consumption(
        building=building,
        heating_system=None,
        cooling_system=CoolingSystem.CENTRAL_AC,
        outdoor_temp=90,
        mode="cooling"
    )

if __name__ == "__main__":
    main()
