# CSE582_Carbon_Calculator
Calculation of procedure's carbon footprint including embodied carbon and operational carbon in terms of kgCO2eq
## Preparation
Put all code and `component_carbon_data.csv` in the same directory
## Usage
`$ python3 main.py`
## Sample output
```
Total Allocated Embodied Carbon: 0.09 kg CO₂-eq
Total Operational Carbon: 13.95 kg CO₂-eq
```
## Notice
Definition of workload procedure involves component hours and average utilization of the component in the procedure. The component hour should be calculated as summation of per-device hour. More careful carbon (energy) accounting can be implemented by extending the component class and define device-specific carbon (energy) model.
