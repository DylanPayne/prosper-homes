from dataclasses import dataclass
from typing import Dict, Any

# Building defaults
BUILDING_DEFAULTS = {
    "assumed_floors": 1,
    "ceiling_height_ft": 8.0,
    "r_value": 13.0,
    "ach": 1.0,  # Air changes per hour
    "width_to_length_ratio": 1.0  # Square footprint by default
}

# Temperature defaults
TEMPERATURE_DEFAULTS = {
    "heating_setpoint_f": 68,  # °F
    "cooling_setpoint_f": 75,  # °F
    "balance_point_f": 65  # °F
}

# Energy rates
ELECTRICITY_RATE_PER_KWH = 0.12  # $/kWh
GAS_RATE_PER_THERM = 1.20  # $/therm

@dataclass
class EquipmentSpec:
    efficiency: float
    fuel_type: str

def get_equipment_spec(system_type: str) -> EquipmentSpec:
    """Get efficiency and fuel type for a given system type"""
    if system_type == "Furnace":
        return EquipmentSpec(0.95, "gas")  # 95% efficient gas furnace
    elif system_type == "Electric Baseboard":
        return EquipmentSpec(1.0, "electric")  # 100% efficient electric heat
    elif system_type == "Central AC":
        return EquipmentSpec(13.0, "electric")  # SEER 13 AC
    else:
        raise ValueError(f"Unknown system type: {system_type}")

def calculate_energy_cost(fuel_type: str, consumption: float, unit: str) -> float:
    """Calculate energy cost based on fuel type and consumption"""
    if fuel_type == "electric" and unit == "kwh":
        return consumption * ELECTRICITY_RATE_PER_KWH
    elif fuel_type == "gas" and unit == "therm":
        return consumption * GAS_RATE_PER_THERM
    else:
        raise ValueError(f"Invalid fuel type ({fuel_type}) or unit ({unit})")
