"""
DAY 1 · HANDS-ON — Build Your Rule Engine
23IF02 System Automation

Work through the TODOs in order. Each one matches a step on the
"Hands-on · Build Your Rule Engine" slide. Run this file after each
step to see your progress:

    python hands_on_starter.py

Need the answer? See hands_on_solution.py — but try it yourself first.
"""

import random
import time

LOG_FILE = "day1_log.txt"
MACHINES = ("Machine-01", "Machine-02", "Machine-03", "Machine-04", "Machine-05")


# ---------------------------------------------------------------------------
# STEP 1 — Generate simulated sensor data
# ---------------------------------------------------------------------------
def generate_sensor_data():
    """Return a dict with at least 'temperature', 'pressure', 'vibration'."""
    return {
        "temperature": random.uniform(50, 95),
        "pressure": random.uniform(90, 120),
        "vibration": random.uniform(0.5, 8.0),
        "current": random.uniform(40, 180),
    }


# ---------------------------------------------------------------------------
# STEP 2 — Write your first automation rules
# STEP 7 — Add a rule of your own (add another dict to this list)
# STEP 8 — Add one priority rule (lower "priority" number checked first)
# ---------------------------------------------------------------------------
RULES = [
    {
        "name": "HIGH_TEMP",
        "priority": 1,
        "condition": lambda r: r.get("temperature") is not None and r["temperature"] > 85,
        "action": "STOP_MACHINE",
    },
    {
        "name": "HIGH_PRESSURE",
        "priority": 2,
        "condition": lambda r: r.get("pressure") is not None and r["pressure"] > 110,
        "action": "REDUCE_LOAD",
    },
    {
        "name": "HIGH_VIBRATION",
        "priority": 3,
        "condition": lambda r: r.get("vibration") is not None and r["vibration"] > 6,
        "action": "CHECK_ALIGNMENT",
    },
    {
        "name": "HIGH_CURRENT",
        "priority": 4,
        "condition": lambda r: r.get("current") is not None and r["current"] > 150,
        "action": "SHUTDOWN",
    },
]


# ---------------------------------------------------------------------------
# STEP 3 — Detect machine state from the rules
# ---------------------------------------------------------------------------
def evaluate_rules(reading, rules):
    """Return (rule_name, action) for the first matching rule, checked in
    priority order (lowest number first). If nothing matches, return
    ("NO_RULE_FIRED", "CONTINUE_NORMAL")."""
    for rule in sorted(rules, key=lambda item: item.get("priority", 999)):
        if rule["condition"](reading):
            return rule["name"], rule["action"]
    return "NO_RULE_FIRED", "CONTINUE_NORMAL"


# ---------------------------------------------------------------------------
# STEP 4 — Trigger an action when a rule fires
# ---------------------------------------------------------------------------
def take_action(action):
    """Return a human-readable string describing what happens for this action."""
    handlers = {
        "STOP_MACHINE": "Emergency stop: machine power cut.",
        "REDUCE_LOAD": "Reduce machine load and inspect the process.",
        "CHECK_ALIGNMENT": "Inspect alignment and check for vibration issues.",
        "SHUTDOWN": "Shut down the drive to prevent motor overload.",
        "CONTINUE_NORMAL": "Continue normal operations.",
    }
    return handlers.get(action, f"(no handler yet for action: {action})")


# ---------------------------------------------------------------------------
# STEP 5 — Log every decision made
# ---------------------------------------------------------------------------
def log_decision(machine, reading, rule_name, action):
    """Append one line to LOG_FILE with the machine, reading, rule, and action."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(
            f"machine={machine} reading={reading} rule={rule_name} action={action}\n"
        )


# ---------------------------------------------------------------------------
# STEP 6 — Add a second sensor to the system (current is included above)
# ---------------------------------------------------------------------------


def main():
    for tick in range(1, 11):
        running_machines = []
        stopped_machines = []
        print(f"[Tick {tick:02d}]")
        for machine in MACHINES:
            reading = generate_sensor_data()
            rule_name, action = evaluate_rules(reading, RULES)
            outcome = take_action(action)

            if action in {"STOP_MACHINE", "SHUTDOWN"}:
                stopped_machines.append(f"{machine} - {rule_name}: {outcome}")
                status = "STOPPED"
            else:
                running_machines.append(machine)
                status = "RUNNING"

            print(f"  {machine} [{status}]")
            print(f"    Sensors: {reading}")
            print(f"    Rule: {rule_name}")
            print(f"    Action: {outcome}")
            log_decision(machine, reading, rule_name, action)

        print(f"  Running machines: {', '.join(running_machines) or 'None'}")
        if stopped_machines:
            print("  Stopped machines (condition triggered):")
            for machine in stopped_machines:
                print(f"    - {machine}")
        else:
            print("  Stopped machines: None")
        print()

        time.sleep(0.2)


if __name__ == "__main__":
    main()
