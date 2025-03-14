from carbon_accountant import CarbonCalculator
from workload_process import Workload
import data_loader as loader
import matplotlib.pyplot as plt

NUMBER_OF_GPU=1024
TRAINING_DATA = 4 * 10**12
MODEL_SIZE = 70 * 10**9

GPU_TFLOPS = {
    "GPU_T4": 65, 
    "GPU_V100": 112,
    "GPU_A100": 312,
    "GPU_H100": 980,
}

data_loader = loader.CarbonDataLoader("component_carbon_data.csv")
components = data_loader.load_components()

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--electricity_carbon_density", type=float, default=0.68)
    parser.add_argument("--csv_path", type=str, default="component_carbon_data.csv")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    total_tflops = 6 * TRAINING_DATA * MODEL_SIZE


    calculator = CarbonCalculator(components, args.electricity_carbon_density)
    # for gpu in ["A100"]:
    for gpu in ["T4", "V100", "A100", "H100"]:
        gpu_name = "GPU_" + gpu

        st, ed = components[gpu_name].idle_power, components[gpu_name].power_consumption
        actual_power_list = [st + x * (ed - st) / 10 for x in range(11)][1:]

        results = {}

        for actual_power in actual_power_list:
            power_util = (actual_power - components[gpu_name].idle_power) / (components[gpu_name].power_consumption - components[gpu_name].idle_power)
            real_tflops = GPU_TFLOPS[gpu_name] * 10 ** 12 * power_util ** 0.8
            hours = int(total_tflops / NUMBER_OF_GPU / real_tflops) / 60 / 60
            usage_dict = {
                gpu_name: {
                    "hours": hours,
                    "utilization": power_util * 100
                }
            }
            embodied_total, operational_total = calculator.calculate_totals(Workload(usage_dict, ""))
            results[power_util * 100] = (embodied_total, operational_total)

        plt.plot(list(results.keys()), [embodied_total + operational_total for _, (embodied_total, operational_total) in results.items()], marker='o', label=gpu_name)

    plt.xlabel('Power Utilization Percentage (%)')
    plt.ylabel('Carbon (kg CO₂-eq)')
    plt.title('Carbon Footprint for GPUs')
    plt.legend()
    plt.savefig(f'output/gpu.png')