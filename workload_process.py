class Workload:
    def __init__(self, usage_dict):
        """
        usage_dict: A dictionary mapping component names to usage hours and avg utilization (percentage).
        Example: {"CPU": (20, 100), "Disk": (20, 50), "GPU": (10, 100), "Network": (10, 10)}
        """
        self.usage = {device: (info["hours"], info["utilization"]) for device, info in usage_dict.items()}
