"""
=============================================================================
🌱 SmartAgri Sentinel - Modern IoT Farm Monitoring & Advisory System
Problem Statement ID: IDHACK-P302 | Hackathon Intermediate Track
Team / Developer: 2nd-Year Computer Science Engineering Student
=============================================================================

Tech Stack:
- Python 3.x
- Streamlit (Rapid, reactive web UI for hackathon demonstrations)
- SQLite3 (Zero-setup local database for fast persistent storage)
- Pandas (Tabular reports and trend visualization)

Key Features:
1. Dashboard / Home Screen: Real-time farm telemetry cards, health badge, trend charts.
2. Input / Monitoring Module: Manual sensor inputs + 1-Click IoT Telemetry Simulator.
3. Advisory / Alert Engine: Rule-based if-else reasoning producing instant recommendations.
4. History / Reports View: Historical tabular logs, filtering, summary stats, and CSV export.
=============================================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Import our custom modules
import database as db
import advisory as adv_engine
import sensor_sim

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SmartAgri Sentinel | IDHACK-P302",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean cards, vibrant status badges, and readability
st.markdown("""
<style>
    /* Main card container */
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 4px;
        font-weight: 500;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 4px;
    }
    /* Health status banners */
    .status-badge-optimal {
        background-color: #dcfce7;
        color: #166534;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #86efac;
    }
    .status-badge-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #fcd34d;
    }
    .status-badge-critical {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #fca5a5;
    }
    .advisory-box {
        background-color: #eff6ff;
        border-left: 5px solid #3b82f6;
        padding: 14px 18px;
        border-radius: 6px;
        margin-top: 12px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATABASE INITIALIZATION
# -----------------------------------------------------------------------------
# Initialize DB tables and seed initial mock history on first run
db.init_db()

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & PROJECT INFO
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌱 SmartAgri Sentinel")
    st.caption("**Problem ID:** IDHACK-P302 (AgriTech Track)")
    st.caption("**Built by:** 2nd-Year CS Engineering Team")
    st.markdown("---")

    st.markdown("### 🚜 Farm Sector Selection")
    active_crop = st.selectbox(
        "Target Crop:",
        ["Wheat", "Tomato", "Rice", "Maize", "Cotton"],
        index=0,
        help="Agronomic thresholds (like water tolerance) adapt automatically based on the crop."
    )
    active_zone = st.selectbox(
        "Field Zone:",
        ["Zone A - North Field", "Zone B - South Greenhouse", "Zone C - River Basin"],
        index=0
    )

    st.markdown("---")
    st.markdown("### ⚡ Quick Demo Actions")

    # Quick seed reset for testing
    if st.button("🔄 Reset Sample Demo Data", help="Reloads clean sample history"):
        db.clear_all_readings()
        db.seed_mock_data_if_empty()
        st.success("Sample telemetry reloaded!")
        st.rerun()

    st.markdown("---")
    st.info("💡 **Quick Tip:**\nUse the **Input & IoT Simulation** tab to trigger drought or fungal scenarios and see the Advisory Engine respond instantly!")

# -----------------------------------------------------------------------------
# 4. MAIN APP TABS
# -----------------------------------------------------------------------------
tab_dashboard, tab_input, tab_history = st.tabs([
    "📊 Farm Dashboard",
    "📝 Input & IoT Simulation",
    "📋 History & Reports"
])

# =============================================================================
# TAB 1: DASHBOARD / HOME SCREEN
# =============================================================================
with tab_dashboard:
    st.subheader(f"🌾 Live Farm Overview: {active_zone} ({active_crop})")

    # Fetch latest entry from database
    latest = db.get_latest_reading()

    if latest:
        # Evaluate current conditions with our rule-based engine
        advisory_result = adv_engine.evaluate_farm_conditions(
            crop_name=latest['crop_name'],
            moisture=latest['moisture'],
            temperature=latest['temperature'],
            humidity=latest['humidity'],
            ph=latest['ph']
        )

        status_class = f"status-badge-{advisory_result['status'].lower()}"
        status_icon = "🟢" if advisory_result['status'] == "Optimal" else ("🟡" if advisory_result['status'] == "Warning" else "🔴")

        # Top Banner with Overall Farm Health & Timestamp
        col_banner_left, col_banner_right = st.columns([3, 1])
        with col_banner_left:
            st.markdown(f"""
            <div style="margin-bottom: 12px;">
                <span class="{status_class}">{status_icon} Farm Health: {advisory_result['status'].upper()}</span>
                <span style="color: #64748b; margin-left: 12px; font-size: 0.9rem;">
                    Last updated: <b>{latest['timestamp']}</b>
                </span>
            </div>
            """, unsafe_allow_html=True)
        with col_banner_right:
            st.markdown(f"**Monitored Crop:** `{latest['crop_name']}`")

        # Key Telemetry Cards (Soil Moisture, Temp, Humidity, Soil pH)
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)

        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">💧 Soil Moisture</div>
                <div class="metric-value">{latest['moisture']:.1f}%</div>
                <div class="metric-sub">Target: 40% - 75%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🌡️ Air Temperature</div>
                <div class="metric-value">{latest['temperature']:.1f}°C</div>
                <div class="metric-sub">Ideal: 20°C - 32°C</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">💨 Air Humidity</div>
                <div class="metric-value">{latest['humidity']:.1f}%</div>
                <div class="metric-sub">Safe: 40% - 75%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🧪 Soil pH</div>
                <div class="metric-value">{latest['ph']:.1f}</div>
                <div class="metric-sub">Optimal: 6.0 - 7.5</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # Advisory & Alert Highlight Box
        # ---------------------------------------------------------------------
        st.markdown("### 📢 Active Agronomic Advisory")
        with st.container():
            st.markdown(f"""
            <div class="advisory-box">
                <h4 style="margin: 0 0 6px 0; color: #1e3a8a;">🤖 Automated Action Advisory:</h4>
                <p style="font-size: 1.05rem; margin: 0; color: #1e293b;">{latest['advisory']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Detailed Flag checklist
            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                st.markdown("**Field Condition Diagnoses:**")
                for flag in advisory_result['flags']:
                    st.write(flag)
            with col_rec2:
                st.markdown("**Recommended Field Actions:**")
                for act in advisory_result['actions']:
                    st.markdown(f"- {act}")

        st.markdown("---")

        # ---------------------------------------------------------------------
        # Telemetry Trends (Line Charts)
        # ---------------------------------------------------------------------
        st.markdown("### 📈 Recent Environmental Trends")
        chronological_data = db.get_readings_chronological(limit=20)

        if len(chronological_data) > 1:
            df_trends = pd.DataFrame(chronological_data)
            # Short timestamp label for clean X-axis
            df_trends['Time'] = pd.to_datetime(df_trends['timestamp']).dt.strftime('%H:%M:%S')

            trend_col1, trend_col2 = st.columns(2)

            with trend_col1:
                st.caption("💧 Soil Moisture vs. Air Humidity (%)")
                chart_data1 = df_trends.set_index('Time')[['moisture', 'humidity']]
                chart_data1.columns = ['Soil Moisture (%)', 'Air Humidity (%)']
                st.line_chart(chart_data1, color=["#0284c7", "#38bdf8"])

            with trend_col2:
                st.caption("🌡️ Temperature Curve (°C)")
                chart_data2 = df_trends.set_index('Time')[['temperature']]
                chart_data2.columns = ['Temperature (°C)']
                st.line_chart(chart_data2, color=["#f97316"])
        else:
            st.info("Log at least 2 readings to view time-series charts.")

    else:
        st.warning("No sensor telemetry recorded yet. Go to 'Input & IoT Simulation' tab to add your first reading!")


# =============================================================================
# TAB 2: INPUT / MONITORING MODULE & IOT SIMULATOR
# =============================================================================
with tab_input:
    st.subheader("📥 Sensor Data Ingestion & Field Input")
    st.write(
        "Collect parameters either through manual farmer observation or simulate "
        "live hardware telemetry from an IoT sensor node (ESP32/Arduino + Soil Probe)."
    )

    # Segment into two columns: Left is IoT Scenario Simulator, Right is Form
    sim_col, form_col = st.columns([1, 1], gap="large")

    with sim_col:
        st.markdown("#### ⚡ 1-Click IoT Hardware Simulator")
        st.caption("Simulate real-world stress conditions to test the advisory engine live during judging:")

        scenario = st.radio(
            "Select Test Scenario:",
            [
                ("optimal", "🌿 Normal Sunny Day (Healthy farm baseline)"),
                ("drought", "🔥 Severe Drought (Low moisture, high temp)"),
                ("waterlogged", "🌊 Monsoon Flood (High moisture, soil saturated)"),
                ("fungal_risk", "🍄 Fungal Disease Threat (Warm 26°C + 90% humidity)"),
                ("random", "🎲 Random Ambient Reading")
            ],
            format_func=lambda x: x[1]
        )[0]

        if st.button("📡 Ingest Simulated IoT Telemetry", type="primary", use_container_width=True):
            sim_vals = sensor_sim.generate_scenario_reading(scenario=scenario, crop_name=active_crop)

            # Evaluate advisory
            eval_res = adv_engine.evaluate_farm_conditions(
                crop_name=active_crop,
                moisture=sim_vals['moisture'],
                temperature=sim_vals['temperature'],
                humidity=sim_vals['humidity'],
                ph=sim_vals['ph']
            )

            # Insert into SQLite database
            db.insert_reading(
                crop_name=active_crop,
                zone_id=active_zone,
                moisture=sim_vals['moisture'],
                temperature=sim_vals['temperature'],
                humidity=sim_vals['humidity'],
                ph=sim_vals['ph'],
                status=eval_res['status'],
                advisory=eval_res['primary_advisory']
            )

            st.success(f"✅ Telemetry ingested successfully! Status: **{eval_res['status']}**")
            st.toast("Telemetry saved to SQLite database!", icon="🌱")
            st.rerun()

        st.markdown("---")
        st.markdown("""
        **Hardware Simulation Context:**
        In physical deployment, this feed connects to:
        - `Capacitive Soil Moisture Sensor v1.2` (Analog Pin A0)
        - `DHT22 / SHT31 Temperature & Humidity Sensor` (Digital Pin D4)
        - `Analog pH Sensor Kit` (Analog Pin A1)
        """)

    with form_col:
        st.markdown("#### ✍️ Manual Sensor Entry Form")
        st.caption("Farmers or agronomists can log handheld meter readings manually:")

        with st.form("manual_entry_form", clear_on_submit=False):
            input_crop = st.selectbox("Crop Type", ["Wheat", "Tomato", "Rice", "Maize", "Cotton"], index=0)
            input_zone = st.selectbox("Field Zone", ["Zone A - North Field", "Zone B - South Greenhouse", "Zone C - River Basin"], index=0)

            val_moisture = st.slider("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=45.0, step=0.5)
            val_temp = st.slider("Ambient Temperature (°C)", min_value=-5.0, max_value=55.0, value=27.0, step=0.5)
            val_humidity = st.slider("Air Humidity (%)", min_value=5.0, max_value=100.0, value=60.0, step=0.5)
            val_ph = st.number_input("Soil pH (0 - 14 scale)", min_value=0.0, max_value=14.0, value=6.5, step=0.1)

            submitted = st.form_submit_button("💾 Save Reading to Database", use_container_width=True)

            if submitted:
                # Validation
                if val_moisture < 0 or val_moisture > 100:
                    st.error("Invalid soil moisture range.")
                else:
                    # Run rule engine
                    eval_res = adv_engine.evaluate_farm_conditions(
                        crop_name=input_crop,
                        moisture=val_moisture,
                        temperature=val_temp,
                        humidity=val_humidity,
                        ph=val_ph
                    )

                    # Save to DB
                    db.insert_reading(
                        crop_name=input_crop,
                        zone_id=input_zone,
                        moisture=val_moisture,
                        temperature=val_temp,
                        humidity=val_humidity,
                        ph=val_ph,
                        status=eval_res['status'],
                        advisory=eval_res['primary_advisory']
                    )

                    st.success(f"Reading saved! Engine status: {eval_res['status']}")
                    st.rerun()


# =============================================================================
# TAB 3: HISTORY & REPORTS VIEW
# =============================================================================
with tab_history:
    st.subheader("📋 Historical Sensor Logs & Advisory Audit Trail")
    st.write("Browse all historical readings stored in the local SQLite database.")

    all_logs = db.get_all_readings(limit=100)

    if all_logs:
        df = pd.DataFrame(all_logs)

        # Top summary stats
        stat_c1, stat_c2, stat_c3, stat_c4 = st.columns(4)
        stat_c1.metric("Total Records", len(df))
        stat_c2.metric("Avg Soil Moisture", f"{df['moisture'].mean():.1f}%")
        stat_c3.metric("Avg Temperature", f"{df['temperature'].mean():.1f}°C")
        critical_alerts_count = len(df[df['status'].isin(['Warning', 'Critical'])])
        stat_c4.metric("Alerts Triggered", critical_alerts_count)

        st.markdown("<br>", unsafe_allow_html=True)

        # Filters for presentation
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            filter_crop = st.multiselect("Filter by Crop:", options=df['crop_name'].unique(), default=df['crop_name'].unique())
        with f_col2:
            filter_status = st.multiselect("Filter by Health Status:", options=df['status'].unique(), default=df['status'].unique())

        filtered_df = df[(df['crop_name'].isin(filter_crop)) & (df['status'].isin(filter_status))]

        # Display Dataframe cleanly
        display_columns = ['id', 'timestamp', 'crop_name', 'zone_id', 'moisture', 'temperature', 'humidity', 'ph', 'status', 'advisory']
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
                "crop_name": st.column_config.TextColumn("Crop"),
                "zone_id": st.column_config.TextColumn("Zone"),
                "moisture": st.column_config.NumberColumn("Moisture (%)", format="%.1f%%"),
                "temperature": st.column_config.NumberColumn("Temp (°C)", format="%.1f°C"),
                "humidity": st.column_config.NumberColumn("Humidity (%)", format="%.1f%%"),
                "ph": st.column_config.NumberColumn("pH", format="%.1f"),
                "status": st.column_config.TextColumn("Status"),
                "advisory": st.column_config.TextColumn("Action Advisory", width="large"),
            },
            hide_index=True
        )

        # CSV Download Button
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Report as CSV",
            data=csv_data,
            file_name=f"agritech_sensor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download audit log for agronomic analysis or submission"
        )
    else:
        st.info("No logs present. Use the Input tab to generate or record telemetry.")

