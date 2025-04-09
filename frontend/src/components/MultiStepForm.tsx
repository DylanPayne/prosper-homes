'use client';

import { useState } from 'react';
import AddressForm from './AddressForm';

interface HomeDetails {
  squareFootage: string;
  numFloors: string;
  heatingSystem: string;
  coolingSystem: string;
}

interface PlanDetails {
  type: 'replace' | 'dual-fuel' | 'heat-pump';
  title: string;
  currentCosts: {
    heating: number;
    cooling: number;
  };
  newCosts: {
    heating: number;
    cooling: number;
  };
  installationCost: number;
  eligibleRebates: number;
  description: string;
}

interface FormData {
  address: string;
  lat: number;
  lng: number;
  homeDetails: HomeDetails;
  selectedPlan: PlanDetails | null;
}

export default function MultiStepForm() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<FormData>({
    address: '',
    lat: 0,
    lng: 0,
    homeDetails: {
      squareFootage: '',
      numFloors: '1',
      heatingSystem: 'furnace',
      coolingSystem: 'central_ac'
    },
    selectedPlan: null
  });

  const [expandedPlan, setExpandedPlan] = useState<string | null>(null);

  const handleAddressSelect = (address: string, lat: number, lng: number) => {
    setFormData(prev => ({
      ...prev,
      address,
      lat,
      lng
    }));
    setStep(2);
  };

  const handleHomeDetailsChange = (field: keyof HomeDetails, value: string) => {
    setFormData(prev => ({
      ...prev,
      homeDetails: { ...prev.homeDetails, [field]: value }
    }));
  };

  const handleHomeDetailsSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setStep(3);
  };

  // Mock data - replace with actual calculations
  const plans: PlanDetails[] = [
    {
      type: 'replace',
      title: 'Replace',
      currentCosts: { heating: 1200, cooling: 300 },
      newCosts: { heating: 800, cooling: 300 },
      installationCost: 8000,
      eligibleRebates: 2000,
      description: 'Replace your existing system with a high-efficiency model'
    },
    {
      type: 'dual-fuel',
      title: 'Dual-Fuel',
      currentCosts: { heating: 1200, cooling: 300 },
      newCosts: { heating: 600, cooling: 250 },
      installationCost: 12000,
      eligibleRebates: 3500,
      description: 'Combine a heat pump with your existing heating system'
    },
    {
      type: 'heat-pump',
      title: 'Heat Pump',
      currentCosts: { heating: 1200, cooling: 300 },
      newCosts: { heating: 400, cooling: 200 },
      installationCost: 15000,
      eligibleRebates: 5000,
      description: 'Switch to an all-electric heat pump system'
    }
  ];

  const togglePlanDetails = (planType: string) => {
    setExpandedPlan(expandedPlan === planType ? null : planType);
  };

  const renderPlanCard = (plan: PlanDetails) => {
    const isExpanded = expandedPlan === plan.type;
    const annualSavings = 
      (plan.currentCosts.heating + plan.currentCosts.cooling) - 
      (plan.newCosts.heating + plan.newCosts.cooling);
    
    return (
      <div key={plan.type} className="bg-white rounded-lg shadow-md overflow-hidden">
        <div 
          onClick={() => togglePlanDetails(plan.type)}
          className="cursor-pointer p-6 hover:bg-gray-50 transition-colors"
        >
          <h3 className="text-xl font-semibold text-gray-900 mb-2">{plan.title}</h3>
          <p className="text-lg text-green-600 font-medium">
            ${annualSavings}/year savings
          </p>
        </div>
        
        {isExpanded && (
          <div className="px-6 pb-6 space-y-4 border-t border-gray-100">
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <h4 className="text-sm font-medium text-gray-500 mb-2">Current Annual Costs</h4>
                <p className="text-gray-900">Heating: ${plan.currentCosts.heating}</p>
                <p className="text-gray-900">Cooling: ${plan.currentCosts.cooling}</p>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-500 mb-2">New Annual Costs</h4>
                <p className="text-green-600">Heating: ${plan.newCosts.heating}</p>
                <p className="text-green-600">Cooling: ${plan.newCosts.cooling}</p>
              </div>
            </div>
            
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-gray-500">Installation Details</h4>
              <p className="text-gray-900">Cost: ${plan.installationCost.toLocaleString()}</p>
              <p className="text-green-600">Eligible Rebates: ${plan.eligibleRebates.toLocaleString()}</p>
              <p className="text-gray-900 mt-4">{plan.description}</p>
            </div>
          </div>
        )}
      </div>
    );
  };

  switch (step) {
    case 1:
      return (
        <div>
          <h2 className="text-2xl font-semibold mb-6 text-white">Enter Your Address</h2>
          <AddressForm onAddressSelect={handleAddressSelect} />
        </div>
      );
    case 2:
      return (
        <div className="space-y-6 max-w-md mx-auto">
          <h2 className="text-2xl font-semibold mb-6 text-white">Home Details</h2>
          <form onSubmit={handleHomeDetailsSubmit} className="space-y-6">
            <div>
              <label htmlFor="squareFootage" className="block text-sm font-medium mb-2 text-white">
                Square Footage
              </label>
              <input
                type="number"
                id="squareFootage"
                value={formData.homeDetails.squareFootage}
                onChange={(e) => handleHomeDetailsChange('squareFootage', e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-gray-900 bg-white"
                required
              />
            </div>

            <div>
              <label htmlFor="numFloors" className="block text-sm font-medium mb-2 text-white">
                Number of Floors
              </label>
              <select
                id="numFloors"
                value={formData.homeDetails.numFloors}
                onChange={(e) => handleHomeDetailsChange('numFloors', e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white text-gray-900"
              >
                <option value="1">1 Floor</option>
                <option value="2">2 Floors</option>
                <option value="3">3 Floors</option>
                <option value="4">4+ Floors</option>
              </select>
            </div>

            <div>
              <label htmlFor="heatingSystem" className="block text-sm font-medium mb-2 text-white">
                Current Heating System
              </label>
              <select
                id="heatingSystem"
                value={formData.homeDetails.heatingSystem}
                onChange={(e) => handleHomeDetailsChange('heatingSystem', e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white text-gray-900"
              >
                <option value="furnace">Gas Furnace</option>
                <option value="boiler">Gas Boiler</option>
                <option value="electric">Electric Heating</option>
                <option value="heat_pump">Heat Pump</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label htmlFor="coolingSystem" className="block text-sm font-medium mb-2 text-white">
                Current Cooling System
              </label>
              <select
                id="coolingSystem"
                value={formData.homeDetails.coolingSystem}
                onChange={(e) => handleHomeDetailsChange('coolingSystem', e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white text-gray-900"
              >
                <option value="central_ac">Central AC</option>
                <option value="window_ac">Window AC Units</option>
                <option value="heat_pump">Heat Pump</option>
                <option value="none">No Cooling System</option>
              </select>
            </div>

            <div className="pt-4">
              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              >
                Continue
              </button>
            </div>
          </form>
        </div>
      );
    case 3:
      return (
        <div className="max-w-2xl mx-auto">
          <h2 className="text-2xl font-semibold mb-6 text-white">Bill Impact</h2>
          <div className="space-y-4">
            {plans.map(renderPlanCard)}
          </div>
        </div>
      );
    default:
      return null;
  }
}
