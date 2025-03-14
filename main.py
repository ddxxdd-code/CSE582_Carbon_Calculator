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

NICS_PER_NODE = 8


def network_traffic(model_size: float, data_size: float, dp: int, pp: int) -> float:
    model_size_byte = 2 * model_size # fp 16
    data_size_byte = 8192 * 2 * data_size # 2 for fp 16, 8192 from ollama embedding
    forward_traffic = (pp - 1) * data_size_byte
    backward_traffic =  dp * model_size_byte
    pp_traffic = forward_traffic + backward_traffic
    dp_traffic = model_size_byte * (dp - 1) * 2 # Assume ring allreduce
    return pp_traffic + dp_traffic


def nic_hours(nic: str, traffic: float, dp: int, pp: int):
    nics_num = dp * pp * NICS_PER_NODE
    traffic_per_nic = traffic / nics_num
    SECONDS_PER_HOUR = 3600
    CX6_SPEED = 2.5e10 # 200 Gbps = 2.5e10 bytes/s
    CX7_SPEED = 5e10 # 400 Gbps = 5e10 bytes/s
    if "6" in nic: # 200 Gbps
        return traffic_per_nic / CX6_SPEED / SECONDS_PER_HOUR
    elif "7" in nic:
        return traffic_per_nic / CX7_SPEED / SECONDS_PER_HOUR
    else:
        raise ValueError("Unknown NIC model")


def draw_nic_graph(components):
    CX6 = "NIC_ConnectX6"
    CX7 = "NIC_ConnectX7"
    MODEL_SIZE = 70e9 # 70B parameters
    DATA_SIZE = 4e12 # 4T tokens
    DATA_PARALLEL = 8
    PIPELINE_PARALLEL = 16
    traffic = network_traffic(MODEL_SIZE, DATA_SIZE, DATA_PARALLEL, PIPELINE_PARALLEL)
    print(f"Traffic: {traffic}")
    print(f"NIC Hours CX6: {nic_hours(CX6, traffic, 8, 8)}")
    print(f"NIC Hours CX7: {nic_hours(CX7, traffic, 8, 8)}")
    parallel_plan = [(8, 16), (16, 8), (32, 4)]
    group_names = []
    group_data = []
    for dp, pp in parallel_plan:
        group_name = f"dp={dp},pp={pp}"
        group_names.append(group_name)
        group_data.append([])
        for nic in [CX6, CX7]:
            traffic = network_traffic(MODEL_SIZE, DATA_SIZE, dp, pp)
            h = nic_hours(nic, traffic, dp, pp) * dp * pp * NICS_PER_NODE
            info = {"hours": h, "utilization": 100}
            procedure = workload.Workload({nic: info}, group_name + f"nic={nic}")
            calculator = accountant.CarbonCalculator(components, 0.68)
            embodied_total, operational_total = calculator.calculate_totals(procedure)
            group_data[-1].append((embodied_total, operational_total))
            print(f"Carbon Footprint for {procedure.name}:")
            print(f"  Total Allocated Embodied Carbon: {embodied_total:.2f} kg CO₂-eq")
            print(f"  Total Operational Carbon: {operational_total:.2f} kg CO₂-eq")

    visualize.embodied_and_operational_groups(group_names, group_data)

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

    draw_nic_graph(components)

if __name__ == "__main__":
    main()
