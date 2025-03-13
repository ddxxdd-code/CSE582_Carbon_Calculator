import argparse
import yaml

import carbon_accountant as accountant
import data_loader as loader
import system_components as components
import workload_process as workload
import visualize

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate the carbon footprint of a workload.")
    parser.add_argument("--csv_path", type=str, default="component_carbon_data.csv",
                        help="Path to the CSV file containing component carbon data.")
    parser.add_argument("--electricity_carbon_density", type=float, default=0.68,
                        help="electricity carbon density (kg CO₂ per kWh)")
    parser.add_argument("--usage", type=str, default="example_usage.yaml")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Step 1: Load component data
    data_loader = loader.CarbonDataLoader(args.csv_path)
    components = data_loader.load_components()
    
    # Step 2: Define a workload using a YAML file
    # Example usage: 20h 50% CPU, 10h 20% Disk, 40h 100% GPU, 2h 5% Network
    with open(args.usage, 'r') as file:
        usages = yaml.safe_load(file)
    procedures = [workload.Workload(usage, name) for name, usage in usages.items()]

    # Step 3: Calculate carbon totals
    calculator = accountant.CarbonCalculator(components, args.electricity_carbon_density)
    
    for procedure in procedures:
        embodied_total, operational_total = calculator.calculate_totals(procedure)
        # Step 4: Display the results
        print(f"Carbon Footprint for {procedure.name}:")
        print(f"  Total Allocated Embodied Carbon: {embodied_total:.2f} kg CO₂-eq")
        print(f"  Total Operational Carbon: {operational_total:.2f} kg CO₂-eq")

    visualize.component_contribution(procedures, calculator)

if __name__ == "__main__":
    main()
