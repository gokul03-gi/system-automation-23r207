import csv
import random

num_records = 100
csv_file = "sensor_history.csv"

# Sensor data ranges
TEMP_RANGE = (25, 100)       # °C
PRESSURE_RANGE = (1, 120)    # bar (example)
RPM_RANGE = (500, 3000)      # RPM
FREQUENCY_RANGE = (45, 60)   # Hz
CURRENT_RANGE = (1, 200)    # A

# Warning thresholds
TEMP_WARNING = 85
PRESSURE_WARNING = 110
RPM_WARNING = 2800
FREQUENCY_WARNING = 55
CURRENT_WARNING = 150

with open(csv_file, mode="w", newline="") as file:

    fieldnames = [
        "Temperature",
        "Pressure",
        "RPM",
        "Frequency",
        "Current",
        "State"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(num_records):

        temperature = round(random.uniform(*TEMP_RANGE), 2)
        pressure = round(random.uniform(*PRESSURE_RANGE), 2)
        rpm = random.randint(*RPM_RANGE)
        frequency = round(random.uniform(*FREQUENCY_RANGE), 2)
        current = round(random.uniform(*CURRENT_RANGE), 2)

        state = (
            "Warning"
            if temperature > TEMP_WARNING
            or pressure > PRESSURE_WARNING
            or rpm > RPM_WARNING
            or frequency > FREQUENCY_WARNING
            or current > CURRENT_WARNING
            else "Normal"
        )

        writer.writerow({
            "Temperature": temperature,
            "Pressure": pressure,
            "RPM": rpm,
            "Frequency": frequency,
            "Current": current,
            "State": state
        })

        print(
            f"Reading {i + 1:03}: "
            f"Temp={temperature:.2f} °C, "
            f"Pressure={pressure:.2f}, "
            f"RPM={rpm}, "
            f"Frequency={frequency:.2f} Hz, "
            f"Current={current:.2f} A, "
            f"State={state}"
        )

print(f"\nSensor history saved to {csv_file}")
print(f"Total records generated: {num_records}")