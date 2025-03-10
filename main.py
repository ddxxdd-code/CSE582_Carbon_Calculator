import carbon_accountant as accountant
import data_loader as loader
import system_components as components
import workload_process as workload

def main():
    # Example CSV file path
    csv_path = 'component_carbon_data.csv'
    
    # Step 1: Load component data
    data_loader = loader.CarbonDataLoader(csv_path)
    components = data_loader.load_components()
    
    # Step 2: Define a workload
    # Example usage: 20h 50% CPU, 10h 20% Disk, 40h 100% GPU, 2h 5% Network
    usage = {"CPU_EPYC7734": (20, 50), "SSD_Samsung_16TB": (10, 20), "GPU_A100": (40, 100), "NIC_ConnectX6": (2, 5)}
    procedure = workload.Workload(usage)
    
    # Step 3: Input electricity carbon density (kg CO₂ per kWh)
    electricity_carbon_density = 0.68  # for example, 0.68 kg CO₂/kWh
    
    # Step 4: Calculate carbon totals
    calculator = accountant.CarbonCalculator(components, electricity_carbon_density)
    embodied_total, operational_total = calculator.calculate_totals(procedure)
    
    # Step 5: Display the results
    print(f"Total Allocated Embodied Carbon: {embodied_total:.2f} kg CO₂-eq")
    print(f"Total Operational Carbon: {operational_total:.2f} kg CO₂-eq")

if __name__ == "__main__":
    main()
