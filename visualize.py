from typing import List, Tuple
import os

import matplotlib.pyplot as plt
import numpy as np

from carbon_accountant import CarbonCalculator
from workload_process import Workload

colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "gray", "olive", "cyan"]



def save_fig(filename):
    if not os.path.exists("./output"):
        os.makedirs("./output")
    plt.savefig(f"./output/{filename}")


def component_contribution(
    workloads: List[Workload],
    calculator: CarbonCalculator,
    filename="component_contribution.png"
):
    """
    Visualize the contribution of each component to the total carbon footprint.
    """
    for x, workload in enumerate(workloads):
        totals = calculator.calculate_totals_per_component(workload)
        assert len(totals) <= len(colors), "Too many components to visualize."

        bottom = 0.
        for c, (dev, emission) in zip(colors, totals.items()):
            label = dev.category() if x == 0 else None
            plt.bar(x, emission, width=0.5, color=c, bottom=bottom, label=label)
            plt.text(
                x,
                bottom + emission / 2,
                f"{emission:.03f}",
                color='black',
                fontsize=10,
                fontweight='bold'
            )

            bottom += emission

    plt.xticks(range(len(workloads)), [w.name for w in workloads])    
    plt.title(f"Workloads Component Contributions")
    plt.legend()
    plt.xlabel("Different workloads")
    plt.ylabel("Carbon Footprint (kg CO₂-eq)")
    save_fig(filename)


def embodied_and_operational_groups(group_names: List[str], group_data: List[List[Tuple[float, float]]], filename="embodied_operational_groups.png"):
    """
    Visualize the embodied and operational carbon footprints for different groups.
    """
    bar_width = 0.5
    gap_between_groups = 1.0

    x_positions = []

    current_x = 0
    for _ in range(len(group_names)):
        positions_for_this_group = np.arange(current_x, current_x + 2)
        x_positions.append(positions_for_this_group)
        current_x += 2 + gap_between_groups

    plt.figure(figsize=(8, 5))

    for group_idx, group_data in enumerate(group_data):
        positions_for_group = x_positions[group_idx]
        for bar_idx, (embodied, operational) in enumerate(group_data):
            x_center = positions_for_group[bar_idx]

            plt.bar(
                x_center,
                embodied,
                width=bar_width,
                color=colors[0],
                label="Embodied" if (group_idx == 0 and bar_idx == 0) else None
            )
            plt.bar(
                x_center,
                operational,
                width=bar_width,
                bottom=embodied,
                color=colors[1],
                label="Operational" if (group_idx == 0 and bar_idx == 0) else None
            )

    group_centers = []
    for positions_for_group in x_positions:
        leftmost = positions_for_group[0]
        rightmost = positions_for_group[-1]
        center = (leftmost + rightmost) / 2
        group_centers.append(center)

    plt.xticks(group_centers, group_names)
    plt.title("Embodied and Operational Carbon Footprints for Different Groups")
    plt.xlabel("Groups")
    plt.ylabel("Carbon Footprint (kg CO₂-eq)")
    plt.legend()
    save_fig(filename)


