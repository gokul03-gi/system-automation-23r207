import os
import time
import random
import joblib
import pandas as pd

from datetime import datetime
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# --------------------------------------------------
# 1. FILE PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(BASE_DIR, "..", "day2", "day2_sample.csv")

MODEL_PATH = os.path.join(BASE_DIR, "..", "day2", "predictive_maintenance_model.pkl")

HISTORY_PATH = os.path.join(BASE_DIR, "live_machine_history.csv")

# --------------------------------------------------
# 2. MACHINE CONFIGURATION
# --------------------------------------------------

MACHINES = [
    "Machine-01",
    "Machine-02",
    "Machine-03",
    "Machine-04",
    "Machine-05"
]

FEATURES = [
    "temperature",
    "pressure",
    "rpm",
    "frequency",
    "current"
]

# --------------------------------------------------
# 3. LOAD DATASET AND MODEL
# --------------------------------------------------

if not os.path.isfile(CSV_PATH):
    raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

if not os.path.isfile(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

df = pd.read_csv(CSV_PATH)
model = joblib.load(MODEL_PATH)

df.columns = df.columns.str.strip().str.lower()

required_columns = FEATURES + ["state"]
missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    raise ValueError(f"Dataset is missing required columns: {missing_columns}")

_, test_data, _, test_labels = train_test_split(
    df[FEATURES],
    df["state"],
    test_size=0.2,
    random_state=42
)
test_accuracy = accuracy_score(test_labels, model.predict(test_data))

print("Dataset loaded successfully.")
print("Predictive maintenance model loaded.")
print(f"Held-out dataset accuracy: {test_accuracy * 100:.2f}%")
print("Starting live machine monitoring...\n")

# --------------------------------------------------
# 4. GENERATE SIMULATED SENSOR DATA
# --------------------------------------------------

def generate_sensor_data():
    return {
        "temperature": round(random.uniform(25, 100), 2),
        "pressure": round(random.uniform(1, 120), 2),
        "rpm": random.randint(500, 3000),
        "frequency": round(random.uniform(45, 60), 2),
        "current": round(random.uniform(1, 200), 2)
    }

# --------------------------------------------------
# 5. DAY 1: RULE-BASED AUTOMATION
# --------------------------------------------------

def evaluate_rules(data):
    if data["temperature"] > 85:
        return "HIGH_TEMP", "INSPECT_TEMPERATURE"

    elif data["pressure"] > 110:
        return "HIGH_PRESSURE", "CHECK_PRESSURE"

    elif data["rpm"] > 2800:
        return "HIGH_RPM", "CHECK_MOTOR_SPEED"

    elif data["frequency"] > 55:
        return "HIGH_FREQUENCY", "CHECK_FREQUENCY"

    elif data["current"] > 150:
        return "HIGH_CURRENT", "CHECK_MOTOR_LOAD"

    return "NO_RULE_FIRED", "CONTINUE_NORMAL"

# --------------------------------------------------
# 6. SAVE LIVE DATA
# --------------------------------------------------

def save_history(record):
    history_df = pd.DataFrame([record])

    history_df.to_csv(
        HISTORY_PATH,
        mode="a",
        header=not os.path.exists(HISTORY_PATH),
        index=False
    )

# --------------------------------------------------
# 7. LIVE MACHINE MONITORING
# --------------------------------------------------

def live_monitor():
    cycle = 0

    try:
        while True:
            cycle += 1

            print("\n" + "=" * 65)
            print(f"LIVE MONITORING - CYCLE {cycle}")
            print("=" * 65)

            for machine in MACHINES:
                data = generate_sensor_data()

                # Machine learning prediction
                input_data = pd.DataFrame(
                    [[data[feature] for feature in FEATURES]],
                    columns=FEATURES
                )

                prediction = model.predict(input_data)[0]

                # Rule-based evaluation
                rule, action = evaluate_rules(data)

                # Combined status
                status = (
                    "WARNING"
                    if str(prediction).strip().lower() == "warning"
                    or rule != "NO_RULE_FIRED"
                    else "NORMAL"
                )

                timestamp = datetime.now().isoformat(
                    timespec="seconds"
                )

                # Display readings
                print(f"\nMachine: {machine}")
                print(f"Time: {timestamp}")
                print(f"Temperature: {data['temperature']} °C")
                print(f"Pressure: {data['pressure']}")
                print(f"RPM: {data['rpm']}")
                print(f"Frequency: {data['frequency']} Hz")
                print(f"Current: {data['current']} A")
                print(f"ML Prediction: {prediction}")
                print(f"Rule Triggered: {rule}")
                print(f"Recommended Action: {action}")
                print(f"Machine Status: {status}")

                if status == "WARNING":
                    print("!!! MAINTENANCE ALERT !!!")

                # Save history
                record = {
                    "timestamp": timestamp,
                    "machine": machine,
                    **data,
                    "ml_prediction": prediction,
                    "rule_triggered": rule,
                    "recommended_action": action,
                    "machine_status": status
                }

                save_history(record)

            print("\nNext cycle starts in 2 seconds...")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        print("History saved to:", HISTORY_PATH)


# --------------------------------------------------
# 8. START MONITORING
# --------------------------------------------------

if __name__ == "__main__":
    live_monitor()