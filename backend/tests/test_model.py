from ..models.energy_model import create_building_from_onboarding, calculate_energy_consumption
from ..config.config import DESIGN_TEMPERATURES

def main():
    # Test with sample onboarding inputs
    square_footage = 2000
    primary_heating = "Furnace"
    primary_cooling = "Central AC"
    
    # Create building and systems from onboarding inputs
    building, heating_system, cooling_system = create_building_from_onboarding(
        square_footage=square_footage,
        primary_heating=primary_heating,
        primary_cooling=primary_cooling
    )
    
    # Calculate peak heating load
    heating_results = calculate_energy_consumption(
        building=building,
        heating_system=heating_system,
        cooling_system=cooling_system,
        outdoor_temp=DESIGN_TEMPERATURES["heating_design_temp_f"],
        mode="heating"
    )
    
    # Calculate peak cooling load
    cooling_results = calculate_energy_consumption(
        building=building,
        heating_system=heating_system,
        cooling_system=cooling_system,
        outdoor_temp=DESIGN_TEMPERATURES["cooling_design_temp_f"],
        mode="cooling"
    )
    
    # Print results
    print("\nBuilding Specifications:")
    print(f"Square Footage: {building.square_footage:,} sq ft")
    print(f"Number of Floors: {building.num_floors}")
    print(f"Ceiling Height: {building.ceiling_height} ft")
    print(f"R-Value: {building.r_value}")
    print(f"Air Changes per Hour: {building.ach}")
    
    print(f"\nHeating Load Test ({DESIGN_TEMPERATURES['heating_design_temp_f']}°F outdoor):")
    print(f"Conductive Load: {heating_results['conductive_load_btuh']:,.0f} BTU/h")
    print(f"Infiltration Load: {heating_results['infiltration_load_btuh']:,.0f} BTU/h")
    print(f"Total Load: {heating_results['total_load_btuh']:,.0f} BTU/h")
    print(f"Gas Consumption: {heating_results['gas_consumption_therm']:.2f} therms/h")
    print(f"Energy Cost: ${heating_results['energy_cost']:.2f}/h")
    
    print(f"\nCooling Load Test ({DESIGN_TEMPERATURES['cooling_design_temp_f']}°F outdoor):")
    print(f"Conductive Load: {cooling_results['conductive_load_btuh']:,.0f} BTU/h")
    print(f"Infiltration Load: {cooling_results['infiltration_load_btuh']:,.0f} BTU/h")
    print(f"Total Load: {cooling_results['total_load_btuh']:,.0f} BTU/h")
    print(f"Electricity Consumption: {cooling_results['energy_consumption_kwh']:.2f} kWh/h")
    print(f"Energy Cost: ${cooling_results['energy_cost']:.2f}/h")

if __name__ == "__main__":
    main()
