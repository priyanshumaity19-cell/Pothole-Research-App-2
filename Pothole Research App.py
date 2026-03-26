import streamlit as st

# --- COPY & PASTE STARTING HERE ---
st.set_page_config(page_title="RoadWatch AI", layout="wide")

# Injection of Custom CSS for the "Modern Tech" look
st.markdown("""
    <style>
    /* 1. Main Background and Font */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    /* 2. Glassmorphism Effect for Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border: 1px solid rgba(0, 242, 255, 0.2) !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        transition: transform 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 242, 255, 0.5) !important;
    }

    /* 3. Neon Gradient Title */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 45px;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00f2ff, #7000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    /* 4. Styled Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 5. Custom Button Styling */
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        padding: 10px 20px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HOW TO USE THE NEW TITLE ---
st.markdown('<h1 class="hero-title">RoadWatch AI & Civic Reporting</h1>', unsafe_allow_html=True)
st.write("Research Focus: Passive accelerometer-based detection & orientation normalization")

# --- YOUR METRICS (They will auto-style) ---
cols = st.columns(4)
cols[0].metric("Total Incidents", "100", "+12% vs last week")
cols[1].metric("Avg. Jolt Magnitude", "0.78g", "Target: 0.5g")
cols[2].metric("Precision (v1.8)", "82%", "Target: >85%")
cols[3].metric("Localization Error", "5.4m", "Target: <5m")

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RoadWatch | Pothole Analytics Dashboard",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS FOR INDUSTRIAL AESTHETIC ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATA GENERATION (Based on your Research ) ---
# In a real app, replace this with your PostGIS/PostgreSQL connection
@st.cache_data
def load_data():
    # Simulate DBSCAN clustered incidents 
    n_points = 100
    data = pd.DataFrame({
        'lat': np.random.normal(22.5726, 0.05, n_points), # Kolkata centered 
        'lon': np.random.normal(88.3639, 0.05, n_points),
        'severity_score': np.random.uniform(1, 10, n_points),
        'report_count': np.random.randint(1, 15, n_points),
        'recorded_at': [datetime.now() - timedelta(days=np.random.randint(0, 30)) for _ in range(n_points)]
    })
    # Severity Thresholding 
    data['status'] = data['severity_score'].apply(
        lambda x: 'Severe' if x >= 7 else ('Moderate' if x >= 4 else 'Minor')
    )
    return data

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://img.icons8.com/ios-filled/100/ffffff/pothole.png", width=80)
st.sidebar.title("RoadWatch AI")
st.sidebar.markdown("---")

date_filter = st.sidebar.slider("Analysis Time Range (Days)", 1, 30, 7)
min_severity = st.sidebar.select_slider("Minimum Severity Threshold", options=["Minor", "Moderate", "Severe"], value="Moderate")

# --- HEADER SECTION ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🛣️ Pothole Analytics & Civic Reporting")
    st.markdown(f"**Research Focus:** Passive accelerometer-based detection & orientation normalization ")

with col_h2:
    st.write("")
    st.button("📄 Generate PDF Complaint", help="Triggers Puppeteer Complaint Engine ")

# --- KEY PERFORMANCE INDICATORS (KPIs) ---
st.markdown("### Technical Metrics Overview")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Total Incidents", len(df), "+12% vs last week")
with kpi2:
    st.metric("Avg. Jolt Magnitude", "0.78g", "Target: 0.6g ")
with kpi3:
    st.metric("Precision (v1.0)", "82%", "Target: ≥80% ")
with kpi4:
    st.metric("Localization Error", "5.4m", "Target: <8m ")

# --- INTERACTIVE SPATIAL ANALYSIS ---
st.markdown("### Real-time Geospatial Heatmap")
# Color scaling for severity 
df['color_r'] = df['severity_score'].apply(lambda x: 255 if x >= 7 else (255 if x >= 4 else 255))
df['color_g'] = df['severity_score'].apply(lambda x: 0 if x >= 7 else (165 if x >= 4 else 255))
df['color_b'] = df['severity_score'].apply(lambda x: 0 if x >= 7 else (0 if x >= 4 else 0))

view_state = pdk.ViewState(latitude=22.5726, longitude=88.3639, zoom=11, pitch=45)

layer = pdk.Layer(
    "ColumnLayer",
    data=df,
    get_position="[lon, lat]",
    get_elevation="severity_score * 100",
    elevation_scale=50,
    radius=100,
    get_fill_color="[color_r, color_g, color_b, 200]",
    pickable=True,
    auto_highlight=True,
)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=view_state,
    layers=[layer],
    tooltip={"text": "Severity: {severity_score}\nReports: {report_count}"}
))

# --- ANALYTICS & TRENDS ---
col_a1, col_a2 = st.columns(2)

with col_a1:
    st.markdown("#### Severity Distribution")
    fig_sev = px.histogram(df, x="severity_score", color="status", 
                          template="plotly_dark", nbins=10,
                          color_discrete_map={'Severe':'#ff4b4b', 'Moderate':'#ffa500', 'Minor':'#ffff00'})
    st.plotly_chart(fig_sev, use_container_width=True)

with col_a2:
    st.markdown("#### Detection Frequency (24h Window)")
    # Simulating the recency score logic from your research 
    df_sorted = df.sort_values('recorded_at')
    fig_trend = px.line(df_sorted, x="recorded_at", y="report_count", 
                        template="plotly_dark", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

# --- RESEARCH LOGIC DOCUMENTATION ---
with st.expander("Technical Architecture & Logic"):
    st.write("""
    **Passive Detection Pipeline:**
    1. **Gravity Removal:** High-pass filter separating static gravity from dynamic acceleration.
    2. **Coordinate Normalization:** Using rotation vector sensors (Accel+Gyro fusion) to project Z-axis to road-normal.
    3. **Speed Gating:** Suppression of events where GPS speed < 5 km/h or > 80 km/h.
    4. **DBSCAN Clustering:** Grouping independent reports within a 15-meter epsilon.
    """)

st.sidebar.markdown("---")
st.sidebar.info("RoadWatch CSE Final Year Project ")
