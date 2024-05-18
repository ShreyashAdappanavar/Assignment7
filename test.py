import psutil
import numpy as np

def measure_cpu_memory_usage():
    # Measure initial memory usage in megabytes
    memory_usage_start = psutil.virtual_memory().used / 1024**2

    # Perform a computational task
    a = 3
    for _ in range(1_000_000):
        a += 1

    # Measure final memory usage in megabytes
    memory_usage_end = psutil.virtual_memory().used / 1024**2

    # Calculate the difference in memory usage
    memory_usage_change = np.abs(memory_usage_end - memory_usage_start)

    # Return results
    return memory_usage_change

# Measure CPU usage over a 1-second interval
cpu_usage_percent = psutil.cpu_percent(interval=1)

# Calculate the memory usage during the computational task
memory_change = measure_cpu_memory_usage()

# Generate a random integer between 0 and 9
random_integer = np.random.randint(10)

print(f"CPU Usage (%): {cpu_usage_percent}")
print(f"Memory Usage Change (MB): {memory_change}")
print(f"Random Integer: {random_integer}")
