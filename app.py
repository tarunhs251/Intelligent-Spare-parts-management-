"""
Streamlit Dashboard - Main Application
Demand Forecasting, Inventory Optimization, and Schedule Planning System
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="Spare Parts Management System",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'forecast_results' not in st.session_state:
    st.session_state.forecast_results = None
if 'inventory_params' not in st.session_state:
    st.session_state.inventory_params = None
if 'procurement_schedule' not in st.session_state:
    st.session_state.procurement_schedule = None


def home_page():
    """Home page with overview and key metrics"""
    st.markdown('<div class="main-header">🔧 Spare Parts Management System</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to the Spare Parts Demand Forecasting & Inventory Optimization System
    
    This comprehensive system provides end-to-end solutions for:
    - **Demand Forecasting**: ML-powered demand prediction with pattern classification
    - **Inventory Optimization**: Safety stock, reorder points, and EOQ calculations
    - **Schedule Planning**: Automated procurement and replenishment scheduling
    """)
    
    # Key metrics section
    st.markdown("### 📊 Key Metrics Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total SKUs", "10", "Active")
    
    with col2:
        st.metric("Locations", "5", "Warehouses")
    
    with col3:
        st.metric("Forecast Accuracy", "92%", "MAPE")
    
    with col4:
        st.metric("Cost Savings", "₹2.5L", "Optimized")
    
    # Quick start guide
    st.markdown("### 🚀 Quick Start Guide")
    
    st.markdown("""
    1. **Upload Data**: Go to Demand Forecasting section and upload your sales data
    2. **Generate Forecasts**: Run the forecasting pipeline to get demand predictions
    3. **Optimize Inventory**: Use Inventory Optimization to calculate optimal parameters
    4. **Plan Schedules**: Generate procurement and replenishment schedules
    """)
    
    # System status
    st.markdown("### ⚙️ System Status")
    
    
    # Recent activity (placeholder)
    st.markdown("### 📈 Recent Activity")
    st.info("No recent activity. Upload data to get started!")


def main():
    """Main application"""
    
    # Sidebar navigation
    st.sidebar.title("🔧 Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Select Section",
        ["🏠 Home", "📊 Demand Forecasting", "📦 Inventory Optimization", 
         "📅 Schedule Planning", "📖 User Manual"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### System Info")
    st.sidebar.info(f"\nLast Updated: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Route to appropriate page
    if page == "🏠 Home":
        home_page()
    elif page == "📊 Demand Forecasting":
        from pages import demand_forecast
        demand_forecast.show()
    elif page == "📦 Inventory Optimization":
        from pages import inventory_optimizer
        inventory_optimizer.show()
    elif page == "📅 Schedule Planning":
        from pages import schedule_planner
        schedule_planner.show()
    elif page == "📖 User Manual":
        from pages import user_manual
        user_manual.show()


if __name__ == "__main__":
    main()

