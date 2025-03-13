from typing import Dict

from workload_process import Workload
from system_components import Component

class CarbonCalculator:
    def __init__(self, components, electricity_carbon_density, annual_usage_hours=8760):
        """
        components: dict of component objects keyed by name.
        electricity_carbon_density: kg CO₂ per kWh.
        annual_usage_hours: hours per year assumed for full usage.
        """
        self.components = components
        self.electricity_carbon_density = electricity_carbon_density
        self.annual_usage_hours = annual_usage_hours

    def embodied_per_component(self, workload) -> Dict[Component, float]:
        """
        raise ValueError if component not found in database
        """
        return {
            self.components[name]: self.components[name].compute_allocated_embodied(usage_hours, self.annual_usage_hours) 
            for name, (usage_hours, _) in workload.usage.items()
        }
    
    def operational_per_component(self, workload) -> Dict[Component, float]:
        """
        raise ValueError if component not found in database
        """
        return {
            self.components[name]: self.components[name].compute_operational(usage_hours, utilization, self.electricity_carbon_density)
            for name, (usage_hours, utilization) in workload.usage.items()
        }
    
    def calculate_totals_per_component(self, workload) -> Dict[Component, float]:
        """
        raise ValueError if component not found in database
        """
        embodied = self.embodied_per_component(workload)
        operational = self.operational_per_component(workload)
        return {name: embodied[name] + operational[name] for name in embodied}

    def calculate_totals(self, workload):
        total_embodied = 0.0
        total_operational = 0.0
        for comp_name, (usage_hours, utilization) in workload.usage.items():
            if comp_name in self.components:
                comp = self.components[comp_name]
                embodied = comp.compute_allocated_embodied(usage_hours, self.annual_usage_hours)
                operational = comp.compute_operational(usage_hours, utilization, self.electricity_carbon_density)
                total_embodied += embodied
                total_operational += operational
            else:
                print(f"Warning: Component '{comp_name}' not found in database.")
        return total_embodied, total_operational
