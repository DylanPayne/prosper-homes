import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any, Tuple
from config import (
    BUILDING_DEFAULTS,
    TEMPERATURE_DEFAULTS,
    get_equipment_spec,
    calculate_energy_cost,
    EquipmentSpec
)
from config.debug_config import DEBUG_CONFIG, debug_print, debug_json, DebugLevel

class HeatingSystem(Enum):
    GAS_FURNACE = "Furnace"
    ELECTRIC_RESISTANCE = "Electric Baseboard"

class CoolingSystem(Enum):
    CENTRAL_AC = "Central AC"
    NONE = "None"

@dataclass
class Building:
    square_footage: float
    num_floors: int = BUILDING_DEFAULTS["assumed_floors"]
    ceiling_height: float = BUILDING_DEFAULTS["ceiling_height_ft"]
    r_value: float = BUILDING_DEFAULTS["r_value"]
    ach: float = BUILDING_DEFAULTS["ach"]

    def __post_init__(self):
        debug_print(f"Created building: {self.square_footage} sq ft", DebugLevel.DEBUG, "energy")
        debug_json({
            "square_footage": self.square_footage,
            "num_floors": self.num_floors,
            "ceiling_height": self.ceiling_height,
            "r_value": self.r_value,
            "ach": self.ach
        }, DebugLevel.TRACE, "energy")

    @property
    def volume(self) -> float:
        """Calculate building volume in cubic feet"""
        return self.square_footage * self.ceiling_height * self.num_floors

    @property
    def surface_area(self) -> float:
        """Calculate total exterior surface area in square feet
        Simplified as a rectangular box"""
        floor_area_per_story = self.square_footage / self.num_floors
        length = math.sqrt(floor_area_per_story * BUILDING_DEFAULTS["width_to_length_ratio"])
        width = length / BUILDING_DEFAULTS["width_to_length_ratio"]
        height = self.ceiling_height * self.num_floors
        
        # Surface area = 2(lw + lh + wh)
        return 2 * (length * width + length * height + width * height)

def calculate_load(building: Building, indoor_temp: float, outdoor_temp: float) -> tuple[float, float]:
    """
    Calculate heating/cooling load in BTU/h
    
    Args:
        building: Building object with properties
        indoor_temp: Indoor temperature (°F)
        outdoor_temp: Outdoor temperature (°F)
        
    Returns:
        tuple of (conductive_load, infiltration_load) in BTU/h
    """
    debug_print(f"Calculating load for {indoor_temp}°F indoor, {outdoor_temp}°F outdoor", DebugLevel.DEBUG, "energy")
    
    # Conductive heat loss through surfaces
    delta_t = indoor_temp - outdoor_temp
    conductive_load = building.surface_area * delta_t / building.r_value
    
    # Infiltration load
    # Q = 1.08 * ACH * Volume * ΔT
    # 1.08 = specific heat * density of air * minutes per hour / 60
    infiltration_load = 1.08 * building.ach * building.volume * delta_t
    
    debug_json({
        "conductive_load_btuh": conductive_load,
        "infiltration_load_btuh": infiltration_load
    }, DebugLevel.DEBUG, "energy")
    
    return conductive_load, infiltration_load

def calculate_energy_consumption(
    building: Building,
    heating_system: Optional[HeatingSystem],
    cooling_system: Optional[CoolingSystem],
    indoor_temp_heat: float = TEMPERATURE_DEFAULTS["heating_setpoint_f"],
    indoor_temp_cool: float = TEMPERATURE_DEFAULTS["cooling_setpoint_f"],
    outdoor_temp: float = 0,
    mode: str = "heating"
) -> dict:
    """
    Calculate energy consumption for heating or cooling
    
    Args:
        building: Building object
        heating_system: Type of heating system
        cooling_system: Type of cooling system
        indoor_temp_heat: Indoor heating setpoint (°F)
        indoor_temp_cool: Indoor cooling setpoint (°F)
        outdoor_temp: Outdoor temperature (°F)
        mode: "heating" or "cooling"
        
    Returns:
        Dictionary with load and energy consumption details
    """
    debug_print(f"Calculating {mode} energy for {outdoor_temp}°F", DebugLevel.INFO, "energy")
    
    indoor_temp = indoor_temp_heat if mode == "heating" else indoor_temp_cool
    conductive_load, infiltration_load = calculate_load(building, indoor_temp, outdoor_temp)
    total_load = abs(conductive_load + infiltration_load)
    
    results = {
        "conductive_load_btuh": conductive_load,
        "infiltration_load_btuh": infiltration_load,
        "total_load_btuh": total_load,
        "energy_consumption_kwh": 0,
        "gas_consumption_therm": 0,
        "energy_cost": 0
    }
    
    if mode == "heating" and heating_system:
        equipment = get_equipment_spec(heating_system.value)
        if not equipment:
            raise ValueError(f"Unknown heating system: {heating_system}")
            
        if equipment.fuel_type == "gas":
            results["gas_consumption_therm"] = (total_load / equipment.efficiency) / 100000  # 100,000 BTU per therm
            results["energy_cost"] = calculate_energy_cost("gas", results["gas_consumption_therm"], "therm")
        else:  # electric
            results["energy_consumption_kwh"] = (total_load / equipment.efficiency) / 3412  # 3412 BTU per kWh
            results["energy_cost"] = calculate_energy_cost("electric", results["energy_consumption_kwh"], "kwh")
    
    elif mode == "cooling" and cooling_system and cooling_system != CoolingSystem.NONE:
        equipment = get_equipment_spec(cooling_system.value)
        if not equipment:
            raise ValueError(f"Unknown cooling system: {cooling_system}")
            
        eer = equipment.efficiency * 0.875  # Approximate EER from SEER
        results["energy_consumption_kwh"] = total_load / (eer * 3.412)  # Convert EER to BTU/Wh
        results["energy_cost"] = calculate_energy_cost("electric", results["energy_consumption_kwh"], "kwh")
    
    debug_json({
        "mode": mode,
        "outdoor_temp": outdoor_temp,
        "results": results
    }, DebugLevel.INFO, "energy")
    
    return results

def create_building_from_onboarding(
    square_footage: float,
    primary_heating: str,
    primary_cooling: str
) -> tuple[Building, Optional[HeatingSystem], Optional[CoolingSystem]]:
    """Create building and system objects from onboarding inputs"""
    building = Building(square_footage=square_footage)
    
    heating_system = None
    if primary_heating:
        try:
            heating_system = HeatingSystem(primary_heating)
        except ValueError:
            pass
            
    cooling_system = None
    if primary_cooling:
        try:
            cooling_system = CoolingSystem(primary_cooling)
        except ValueError:
            cooling_system = CoolingSystem.NONE
            
    return building, heating_system, cooling_system