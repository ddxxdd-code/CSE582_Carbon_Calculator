from typing import List
import os

import matplotlib.pyplot as plt

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
