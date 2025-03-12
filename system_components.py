class Component:
    def __init__(self, name, embodied_carbon, lifetime_years, power_consumption, idle_power=0):
        self.name = name
        self.embodied_carbon = embodied_carbon  # Total embodied carbon (kg CO₂-eq)
        self.lifetime_years = lifetime_years    # Expected lifetime (years)
        self.power_consumption = power_consumption  # Watts
        self.idle_power = idle_power # Watts

    def category(self):
        """
        Return the category of the component based on power consumption.
        """
        return self.name.split("_")[0]

    def compute_allocated_embodied(self, usage_hours, annual_usage_hours=8760):
        """
        Allocate a fraction of embodied carbon based on the proportion of lifetime usage.
        annual_usage_hours: assumed maximum usage hours per year (default: 8760 for 24/7 usage).
        """
        total_lifetime_hours = self.lifetime_years * annual_usage_hours
        allocated = (usage_hours / total_lifetime_hours) * self.embodied_carbon
        return allocated

    def compute_operational(self, usage_hours, utilization, electricity_carbon_density):
        """
        Compute operational carbon based on usage.
        Convert power from Watts to kW (divide by 1000) and multiply by usage hours and carbon density.
        """
        actual_utilization = utilization / 100
        energy_kwh = (actual_utilization * (self.power_consumption - self.idle_power) + self.idle_power) * usage_hours / 1000
        return energy_kwh * electricity_carbon_density
