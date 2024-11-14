from config import Config
from src.utils import Utils
import matplotlib.pyplot as plt

values = {}
for i in range(0, 35):
    values[i] = Utils.get_interpolated_value(i, Config.GROWTH_RATE_TEMP)

survival_values = {}

for i in range(0, 100):
    survival_values[i] = Utils.get_interpolated_value(i, Config.SURVIVAL_TIME_WATER)


fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns, adjust the size as needed

# Plot Growth Rate vs Temperature on the first subplot
axs[0].plot(list(values.keys()), list(values.values()))
axs[0].set_xlabel('Temperature (°C)')
axs[0].set_ylabel('Growth Rate')
axs[0].set_title('Growth Rate vs Temperature')

# Plot Survival Time vs Water Availability on the second subplot
axs[1].plot(list(survival_values.keys()), list(survival_values.values()))
axs[1].set_xlabel('Water availability (%)')
axs[1].set_ylabel('Survival Time (days)')
axs[1].set_title('Survival Time vs Water Availability')

# Adjust layout to prevent overlapping labels and titles
plt.tight_layout()

# Show the combined plot
plt.show()