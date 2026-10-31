"""
=============================================================================
🌱 SmartAgri Sentinel - Advisory & Alert Rule Engine (advisory.py)
Problem ID: IDHACK-P302 (AgriTech Hackathon Prototype)
=============================================================================

This module is the core decision-making brain of the application.
It uses domain-informed agronomic threshold rules (if-else statements)
to analyze sensor readings and produce real-time, actionable alerts.

Key Evaluation Pillars:
1. Soil Moisture Management (Irrigation pump control & waterlogging prevention)
2. Microclimate / Thermal Stress (Heat exhaustion & frost damage protection)
3. Disease / Fungal Hazard Assessment (Relative humidity + temperature interaction)
4. Soil pH Nutrient Availability (Liming or acid correction)

Why Rule-Based Logic for Hackathon Stage?
- Deterministic, explainable, and zero false-hallucinations compared to complex LLMs.
- Runs instantly on low-power microcontrollers / Raspberry Pi edge devices in the field.
- Easy for professors/judges to verify during viva.
=============================================================================
"""


def evaluate_farm_conditions(crop_name: str, moisture: float, temperature: float, humidity: float, ph: float = 6.5) -> dict:
    """
    Evaluates current soil and ambient weather parameters against agricultural thresholds.

    Parameters:
        crop_name (str): Crop type (e.g. 'Wheat', 'Tomato', 'Rice', 'Maize', 'Cotton')
        moisture (float): Volumetric soil moisture percentage (0.0 to 100.0%)
        temperature (float): Ambient air temperature in Celsius (°C)
        humidity (float): Relative air humidity percentage (0.0 to 100.0%)
        ph (float): Soil acidity level (pH scale: 0 to 14)

    Returns:
        dict: {
            "status": "Optimal" | "Warning" | "Critical",
            "badge_color": "green" | "orange" | "red",
            "primary_advisory": str,
            "actions": list of str,
            "flags": list of str
        }
    """
    actions = []
    flags = []
    severity_scores = []  # 0 = Normal, 1 = Warning, 2 = Critical

    # -------------------------------------------------------------------------
    # RULE LAYER 1: Soil Moisture & Irrigation Control
    # -------------------------------------------------------------------------
    # Agronomic context:
    # Most field crops experience wilting point below 30% moisture.
    # Saturated soil (> 80%) suffocates roots and causes anaerobic root rot.
    # Special case: Rice is semi-aquatic and can tolerate higher moisture.
    is_rice = (crop_name.lower() == "rice")

    if is_rice:
        low_threshold = 45.0
        high_threshold = 92.0
    else:
        low_threshold = 30.0
        high_threshold = 78.0

    if moisture < (low_threshold - 10.0):
        # Critical Drought / Severe Dehydration
        flags.append("🚨 Critical Soil Dehydration")
        actions.append("IMMEDIATE ACTION: Turn ON main irrigation pump. Soil is below permanent wilting point.")
        severity_scores.append(2)
    elif moisture < low_threshold:
        # Mild Water Deficit
        flags.append("⚠️ Low Soil Moisture")
        actions.append(f"Turn ON drip irrigation system for 30-45 minutes. Moisture is at {moisture:.1f}%.")
        severity_scores.append(1)
    elif moisture > high_threshold:
        # Waterlogging
        flags.append("🌊 Waterlogging / Saturated Soil")
        actions.append("PAUSE all irrigation. Clear field drainage canals to prevent root rot and anaerobic soil conditions.")
        severity_scores.append(1 if moisture < 88.0 else 2)
    else:
        # Optimal Water Zone
        flags.append("✅ Soil Moisture Optimal")

    # -------------------------------------------------------------------------
    # RULE LAYER 2: Ambient Temperature & Heat/Frost Stress
    # -------------------------------------------------------------------------
    # Agronomic context:
    # > 38°C causes flower abortion and photosynthetic shutdown (Heat stress).
    # < 10°C stunts vegetative growth and risks chill injury.
    if temperature > 40.0:
        flags.append("🔥 Extreme Heat Wave")
        actions.append("Deploy shade nets and initiate overhead misting/sprinklers to lower canopy temperature.")
        severity_scores.append(2)
    elif temperature > 34.0:
        flags.append("☀️ Elevated Temperature Warning")
        actions.append("High evapotranspiration detected. Schedule evening irrigation to reduce water loss.")
        severity_scores.append(1)
    elif temperature < 8.0:
        flags.append("❄️ Frost Warning")
        actions.append("Risk of frost damage to young seedlings. Apply straw mulch or cover with thermal fleece.")
        severity_scores.append(2)
    elif temperature < 14.0:
        flags.append("🧥 Low Temperature Caution")
        actions.append("Vegetative growth may slow down. Avoid heavy nitrogen fertilization during cold spells.")
        severity_scores.append(1)
    else:
        flags.append("✅ Temperature in Comfortable Range")

    # -------------------------------------------------------------------------
    # RULE LAYER 3: Humidity & Microclimate Fungal Infection Risk
    # -------------------------------------------------------------------------
    # Agronomic context:
    # Warm, humid conditions (Humidity > 80% with Temp 20°C - 32°C) are the
    # classic "Disease Triangle" incubator for Powdery Mildew, Early Blight & Rust.
    if humidity > 80.0 and (20.0 <= temperature <= 32.0):
        flags.append("🍄 High Fungal Disease Outbreak Risk")
        actions.append("Warm humid microclimate favors fungal spores. Inspect underside of leaves and prepare preventive organic bio-fungicide (e.g. Neem oil spray).")
        severity_scores.append(2)
    elif humidity > 85.0:
        flags.append("💧 High Relative Humidity")
        actions.append("Ensure adequate plant spacing and pruning for aeration to keep leaf surfaces dry.")
        severity_scores.append(1)
    elif humidity < 25.0:
        flags.append("🏜️ Very Dry Air")
        actions.append("Dry atmospheric conditions accelerate transpiration. Monitor crop for rapid moisture depletion.")
        severity_scores.append(1)
    else:
        flags.append("✅ Humidity Normal")

    # -------------------------------------------------------------------------
    # RULE LAYER 4: Soil pH (Nutrient Bioavailability)
    # -------------------------------------------------------------------------
    # Agronomic context:
    # Ideal soil pH is 6.0 to 7.2. Outside this range, essential minerals (N, P, K)
    # become chemically locked and unavailable to root systems.
    if ph < 5.5:
        flags.append("🧪 Highly Acidic Soil")
        actions.append(f"Soil pH is acidic ({ph:.1f}). Apply agricultural limestone (calcium carbonate) to restore neutrality.")
        severity_scores.append(1)
    elif ph > 8.0:
        flags.append("🧪 Highly Alkaline Soil")
        actions.append(f"Soil pH is alkaline ({ph:.1f}). Incorporate elemental sulfur or organic compost to buffer pH.")
        severity_scores.append(1)
    else:
        flags.append("✅ Soil pH Balanced")

    # -------------------------------------------------------------------------
    # FINAL STATUS RESOLUTION
    # -------------------------------------------------------------------------
    max_severity = max(severity_scores) if severity_scores else 0

    if max_severity == 2:
        status = "Critical"
        badge_color = "red"
        primary_advisory = actions[0] if actions else "Critical farm condition detected. Immediate intervention recommended."
    elif max_severity == 1:
        status = "Warning"
        badge_color = "orange"
        primary_advisory = actions[0] if actions else "Sub-optimal parameters observed. Preventive adjustments suggested."
    else:
        status = "Optimal"
        badge_color = "green"
        primary_advisory = f"All parameters for {crop_name} are within healthy agronomic limits. Keep up regular routine monitoring."
        actions.append("Maintain current irrigation schedule.")
        actions.append("Soil and microclimate conditions are ideal for photosythesis and root growth.")

    return {
        "status": status,
        "badge_color": badge_color,
        "primary_advisory": primary_advisory,
        "actions": actions,
        "flags": flags
    }
