"""
=============================================================================
🌱 SmartAgri Sentinel - Unit & Integration Test Suite (test_system.py)
Problem ID: IDHACK-P302
=============================================================================

Demonstrates automated testing of our core database and rule engine logic.
Can be executed during judging:
    python test_system.py
=============================================================================
"""

import sys
import database as db
import advisory as adv_engine
import sensor_sim


def test_database_operations():
    print("[TEST 1] Initializing Database & Inserting Test Telemetry...")
    db.init_db()
    
    # Insert test reading
    db.insert_reading(
        crop_name="Tomato",
        zone_id="Zone Test",
        moisture=22.5,
        temperature=35.0,
        humidity=45.0,
        ph=6.4,
        status="Warning",
        advisory="Low moisture detected. Drip irrigation recommended."
    )
    
    latest = db.get_latest_reading()
    assert latest is not None, "Error: Latest reading was None"
    assert latest["crop_name"] == "Tomato", "Error: Crop name mismatch"
    assert latest["moisture"] == 22.5, "Error: Moisture value mismatch"
    print(" -> PASS: Database insertion and retrieval verified.")


def test_advisory_rules():
    print("[TEST 2] Verifying Advisory Rule Engine Logic...")
    
    # Scenario A: Drought condition
    res_drought = adv_engine.evaluate_farm_conditions(
        crop_name="Wheat",
        moisture=18.0,
        temperature=38.0,
        humidity=30.0,
        ph=6.5
    )
    assert res_drought["status"] in ["Warning", "Critical"], "Error: Drought should trigger Warning or Critical"
    print(" -> PASS: Drought condition successfully flagged.")
    
    # Scenario B: Fungal risk condition (warm + high humidity)
    res_fungal = adv_engine.evaluate_farm_conditions(
        crop_name="Wheat",
        moisture=60.0,
        temperature=27.0,
        humidity=88.0,
        ph=6.5
    )
    assert any("Fungal" in flag for flag in res_fungal["flags"]), "Error: Fungal hazard flag not generated"
    print(" -> PASS: Fungal microclimate risk successfully flagged.")
    
    # Scenario C: Optimal baseline
    res_optimal = adv_engine.evaluate_farm_conditions(
        crop_name="Wheat",
        moisture=55.0,
        temperature=25.0,
        humidity=60.0,
        ph=6.5
    )
    assert res_optimal["status"] == "Optimal", "Error: Optimal conditions should yield Optimal status"
    print(" -> PASS: Optimal conditions evaluated correctly.")


def test_sensor_simulator():
    print("[TEST 3] Verifying Sensor Simulator Scenarios...")
    for scenario in ["optimal", "drought", "waterlogged", "fungal_risk"]:
        telemetry = sensor_sim.generate_scenario_reading(scenario=scenario, crop_name="Wheat")
        assert 0.0 <= telemetry["moisture"] <= 100.0, f"Invalid moisture for {scenario}"
        assert -10.0 <= telemetry["temperature"] <= 60.0, f"Invalid temperature for {scenario}"
        assert 0.0 <= telemetry["humidity"] <= 100.0, f"Invalid humidity for {scenario}"
        assert 0.0 <= telemetry["ph"] <= 14.0, f"Invalid pH for {scenario}"
    print(" -> PASS: Sensor simulator outputs within physically valid ranges.")


if __name__ == "__main__":
    # Ensure stdout handles unicode if needed
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    print("==================================================")
    print("[RUN] Running SmartAgri Sentinel Test Suite (IDHACK-P302)")
    print("==================================================")
    try:
        test_database_operations()
        test_advisory_rules()
        test_sensor_simulator()
        print("==================================================")
        print("[SUCCESS] ALL TESTS PASSED! System is Hackathon-Ready.")
        print("==================================================")
    except AssertionError as e:
        print(f"[FAIL] Test Failed: {e}")
        sys.exit(1)
