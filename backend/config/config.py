from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class EquipmentSpec:
    name: str
    fuel_type: Literal["gas", "electric"]
    efficiency: float  # AFUE for heating, SEER for cooling
    modes: list[Literal["heating", "cooling"]]
    min_capacity_btuh: Optional[float] = None
    max_capacity_btuh: Optional[float] = None
    cop: Optional[float] = None  # For heat pumps

# Building defaults
BUILDING_DEFAULTS = {
    "ceiling_height_ft": 8.0,
    "r_value": 10.0,
    "ach": 1.0,
    "assumed_floors": 2,  # Default assumption for sq footage to geometry conversion
    "width_to_length_ratio": 1.0,  # Square footprint by default
}

# Utility rates (example rates, should be updated per region)
UTILITY_RATES = {
    "electricity_cost_per_kwh": 0.12,
    "gas_cost_per_therm": 1.50,
}

# Equipment specifications
EQUIPMENT_SPECS = {
    "Furnace": EquipmentSpec(
        name="High-Efficiency Gas Furnace",
        fuel_type="gas",
        efficiency=0.95,  # 95% AFUE
        modes=["heating"],
        min_capacity_btuh=40000,
        max_capacity_btuh=120000
    ),
    "Electric Baseboard": EquipmentSpec(
        name="Electric Resistance Heating",
        fuel_type="electric",
        efficiency=1.0,  # 100% efficient
        modes=["heating"],
        min_capacity_btuh=2000,
        max_capacity_btuh=50000
    ),
    "Central AC": EquipmentSpec(
        name="Central Air Conditioner",
        fuel_type="electric",
        efficiency=16.0,  # SEER
        modes=["cooling"],
        min_capacity_btuh=18000,
        max_capacity_btuh=60000
    ),
}

# Temperature setpoints
TEMPERATURE_DEFAULTS = {
    "heating_setpoint_f": 68,
    "cooling_setpoint_f": 72,
}

# Design temperatures (example values, should be updated per region)
DESIGN_TEMPERATURES = {
    "heating_design_temp_f": -5,
    "cooling_design_temp_f": 86,
}

def get_equipment_spec(equipment_name: str) -> Optional[EquipmentSpec]:
    """Get equipment specifications by name"""
    return EQUIPMENT_SPECS.get(equipment_name)

def calculate_energy_cost(
    energy_type: Literal["gas", "electric"],
    amount: float,
    unit: Literal["kwh", "therm"]
) -> float:
    """Calculate energy cost based on type and amount"""
    if energy_type == "electric" and unit == "kwh":
        return amount * UTILITY_RATES["electricity_cost_per_kwh"]
    elif energy_type == "gas" and unit == "therm":
        return amount * UTILITY_RATES["gas_cost_per_therm"]
    else:
        raise ValueError(f"Invalid energy type ({energy_type}) and unit ({unit}) combination")
