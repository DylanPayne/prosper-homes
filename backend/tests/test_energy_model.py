import unittest
from ..models.energy_model import Building, HeatingSystem, CoolingSystem, calculate_load, calculate_energy_consumption
from ..config.config import DESIGN_TEMPERATURES

class TestEnergyModel(unittest.TestCase):
    def setUp(self):
        # Create a simple test building: 1000 sq ft, single story
        self.building = Building(
            square_footage=1000,
            num_floors=1,
            ceiling_height=8.0,
            r_value=10.0,
            ach=1.0
        )

    def test_building_calculations(self):
        """Test basic building geometry calculations"""
        self.assertEqual(self.building.volume, 8000)  # 1000 sq ft * 8 ft height
        
        # Surface area = 2(lw + lh + wh) where l=w=sqrt(1000)
        expected_surface_area = 2 * (1000 + 2 * 8 * math.sqrt(1000))
        self.assertAlmostEqual(self.building.surface_area, expected_surface_area, places=2)

    def test_load_calculation(self):
        """Test heat load calculations with known values"""
        # Test with 1°F temperature difference for simple verification
        conductive_load, infiltration_load = calculate_load(
            self.building,
            indoor_temp=71,
            outdoor_temp=70
        )
        
        # Conductive load should be surface_area * 1°F / R-10
        expected_conductive = self.building.surface_area / 10
        self.assertAlmostEqual(conductive_load, expected_conductive, places=2)
        
        # Infiltration load should be 1.08 * 1ACH * 8000ft³ * 1°F
        expected_infiltration = 1.08 * 1.0 * 8000 * 1
        self.assertAlmostEqual(infiltration_load, expected_infiltration, places=2)

    def test_gas_furnace_consumption(self):
        """Test gas furnace energy consumption calculation"""
        results = calculate_energy_consumption(
            building=self.building,
            heating_system=HeatingSystem.GAS_FURNACE,
            cooling_system=None,
            indoor_temp_heat=70,
            outdoor_temp=60,
            mode="heating"
        )
        
        # Verify gas consumption calculation
        # With 95% efficiency, therms = (total_load / 0.95) / 100000
        expected_therms = results["total_load_btuh"] / 0.95 / 100000
        self.assertAlmostEqual(results["gas_consumption_therm"], expected_therms, places=4)
        self.assertEqual(results["energy_consumption_kwh"], 0)  # Should be 0 for gas

    def test_central_ac_consumption(self):
        """Test central AC energy consumption calculation"""
        results = calculate_energy_consumption(
            building=self.building,
            heating_system=None,
            cooling_system=CoolingSystem.CENTRAL_AC,
            indoor_temp_cool=75,
            outdoor_temp=85,
            mode="cooling"
        )
        
        # Verify electricity consumption calculation
        # SEER 16 -> EER ~14 -> BTU/Wh = 14
        self.assertTrue(results["energy_consumption_kwh"] > 0)
        self.assertEqual(results["gas_consumption_therm"], 0)  # Should be 0 for electric

if __name__ == '__main__':
    unittest.main()
