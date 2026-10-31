# 🌱 SmartAgri Sentinel: IoT Farm Monitoring & Advisory System
**Problem Statement ID:** `IDHACK-P302` | **Category:** AgriTech (Intermediate Difficulty)  
**Developer Persona:** 2nd-Year Computer Science & Engineering Student Hackathon Team  

---

## 📌 Executive Summary
**SmartAgri Sentinel** is an end-to-end, lightweight farm monitoring and advisory prototype engineered for smallholder farmers and greenhouse managers. It combines real-time IoT soil and weather telemetry ingestion with a deterministic, rule-based agronomic advisory engine to deliver instantaneous irrigation and disease-prevention recommendations.

Built with Python, Streamlit, and SQLite, the system is 100% offline-ready, serverless, and designed for deployment on low-cost edge computing nodes (e.g., Raspberry Pi gateways) in rural farming zones.

---

## 🚀 Key Features

### 1. 📊 Real-Time Dashboard & Health Status
- **Live Telemetry Cards:** High-visibility cards for Soil Moisture (%), Ambient Temperature (°C), Air Humidity (%), and Soil pH.
- **Dynamic Health Status:** Color-coded status badge (`OPTIMAL`, `WARNING`, `CRITICAL`) reflecting overall field stability.
- **Trend Visualizations:** Interactive time-series line charts tracking moisture, humidity, and temperature trends to spot rapid soil dry-out.

### 2. 📝 Input & IoT Telemetry Simulator Module
- **Manual Logging:** Intuitive sliders and numeric inputs for farmers with handheld soil probes.
- **1-Click IoT Telemetry Simulator:** Instantly generates realistic sensor feeds for multiple real-world scenarios:
  - *Normal Sunny Day* (Balanced baseline)
  - *Severe Drought* (Heatwave + low moisture trigger)
  - *Monsoon Flood* (Waterlogging + root rot risk)
  - *Fungal Spore Threat* (Warm temperature + high humidity disease incubator)
  - *Random Ambient Reading* (Field telemetry noise)

### 3. 🧠 Advisory & Alert Engine (`advisory.py`)
Deterministic, rule-based decision engine (`if-else` hierarchy) rooted in agronomic science:
- **Water Management:** Detects permanent wilting point (<30% moisture) to trigger irrigation pumps; prevents root rot by alerting on saturation (>78%).
- **Thermal Stress:** Flags frost threats (<8°C) and severe heat exhaustion (>38°C) with misting recommendations.
- **Disease Triangle Modeling:** Flags fungal outbreaks when warm microclimates (20°C - 32°C) coincide with high humidity (>80%).
- **Soil pH Diagnostics:** Alerts on acidic (<5.5) or alkaline (>8.0) soils with corrective liming/composting advisories.

### 4. 📋 History & Audit Reports
- **Persistent SQLite Storage:** Auto-creates and maintains `farm_data.db`.
- **Search & Multi-Filters:** Filter logs by crop variety or health severity status.
- **Instant CSV Export:** One-click download of audit logs for agricultural officers or loan insurance verification.

---

## 🏗️ Architecture & File Structure

```
hack2/
├── app.py              # Main Streamlit web application & user interface
├── database.py         # SQLite database management, CRUD operations & mock seed data
├── advisory.py         # Rule-based agronomic advisory & alert engine
├── sensor_sim.py       # Simulated IoT telemetry scenario generator
├── test_system.py      # Automated unit & integration tests
├── requirements.txt    # Minimal project dependencies
└── README.md           # Project documentation
```

---

## 💻 How to Run the Prototype

### 1. Prerequisites
Ensure Python 3.9+ is installed on your machine.

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python -m streamlit run app.py
```
The application will automatically open in your default browser at `http://localhost:8501`.

---

## 📜 Problem ID & Metadata
- **Problem ID:** `IDHACK-P302`
- **Target Audience:** Smallholder agricultural producers, greenhouse operators, agricultural students.
- **License:** Open Source MIT (Academic & Hackathon Prototype)
