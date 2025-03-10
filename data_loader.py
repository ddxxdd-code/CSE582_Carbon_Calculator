import pandas as pd
import system_components as component

class CarbonDataLoader:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def load_components(self):
        df = pd.read_csv(self.csv_path)
        components = {}
        # Expect CSV columns: name, embodied_carbon, lifetime_years, power_consumption
        # Assuming carbon in eqCo2, lifetime in years, power in Watts
        for _, row in df.iterrows():
            comp = component.Component(
                name=row['name'],
                embodied_carbon=row['embodied_carbon'],
                lifetime_years=row['lifetime_years'],
                power_consumption=row['power_consumption'],
                idle_power = row['idle_power']
            )
            components[comp.name] = comp
        return components
