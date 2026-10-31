"""
=============================================================================
🌱 SmartAgri Sentinel - IoT Sensor Simulator (sensor_sim.py)
Problem ID: IDHACK-P302 (AgriTech Hackathon Prototype)
=============================================================================

This module simulates incoming telemetry from physical IoT hardware (e.g.,
ESP32 / Arduino equipped with Capacitive Soil Moisture Sensors, DHT22
temperature & humidity sensors, and analog pH probes).

Why is this useful for Hackathons?
Judges often ask: "Can you demonstrate how the system handles different stress
conditions on the fly?"
With these scenario presets, the presenter can switch between drought,
waterlogging, fungal hazard, or normal weather in a single click!
=============================================================================
"""

import random


def generate_scenario_reading(scenario: str = "random", crop_name: str = "Wheat") -> dict:
    """
    Generates realistic sensor values tailored to specific agronomic scenarios.

    Scenarios:
        - "random": Natural field fluctuations around healthy baseline.
        - "drought": High heat, dry air, critically low soil moisture.
        - "waterlogged": Excessive moisture, high humidity, overcast conditions.
        - "fungal_risk": Warm incubator conditions (26°C - 29°C) with 85%+ humidity.
        - "optimal": Near-perfect conditions for maximum photosynthetic efficiency.
    """
    scenario = scenario.lower()

    if scenario == "drought":
        moisture = round(random.uniform(14.0, 24.5), 1)
        temperature = round(random.uniform(36.0, 42.5), 1)
        humidity = round(random.uniform(20.0, 35.0), 1)
        ph = round(random.uniform(6.5, 7.5), 1)

    elif scenario == "waterlogged":
        moisture = round(random.uniform(84.0, 96.0), 1)
        temperature = round(random.uniform(22.0, 26.0), 1)
        humidity = round(random.uniform(86.0, 95.0), 1)
        ph = round(random.uniform(6.2, 7.0), 1)

    elif scenario == "fungal_risk":
        moisture = round(random.uniform(55.0, 70.0), 1)
        temperature = round(random.uniform(24.0, 29.0), 1)  # Prime incubation zone
        humidity = round(random.uniform(86.0, 94.0), 1)     # High spore germination
        ph = round(random.uniform(6.0, 6.8), 1)

    elif scenario == "optimal":
        moisture = round(random.uniform(48.0, 62.0), 1)
        temperature = round(random.uniform(23.0, 28.5), 1)
        humidity = round(random.uniform(52.0, 68.0), 1)
        ph = round(random.uniform(6.3, 6.9), 1)

    else:
        # Generic random fluctuation
        moisture = round(random.uniform(35.0, 75.0), 1)
        temperature = round(random.uniform(18.0, 36.0), 1)
        humidity = round(random.uniform(40.0, 80.0), 1)
        ph = round(random.uniform(5.8, 7.8), 1)

    return {
        "moisture": moisture,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph
    }
