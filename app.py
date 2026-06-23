# app.py
import streamlit as st
import os

# Set page configuration FIRST
st.set_page_config(
    page_title="RetailPulse - AI Customer Analytics & Demand Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import local modules
import utils
import styles
from dashboard_pages import (
    executive_dashboard,
    customer_analytics,
    customer_segmentation,
    demand_forecasting,
    inventory_optimization,
    churn_prediction,
    advanced_ml_analytics,
    what_if_analysis
)

# Ensure folders and sample datasets are initialized
utils.generate_sample_data()

# Force light theme
st.session_state.theme = "light"

# Sidebar Branding
st.sidebar.markdown(
    """
    <div class="sidebar-logo">
        RetailPulse
        <div style="font-size: 0.8rem; font-weight: 500; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 4px;">
            AI Analytics Platform
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<hr style='margin: 8px 0; opacity: 0.15;'>", unsafe_allow_html=True)

# Page Navigation List
st.sidebar.markdown("<div style='font-size:0.8rem; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;'>Navigation Menu</div>", unsafe_allow_html=True)
page_selection = st.sidebar.radio(
    "Go To Page",
    [
        "💼 Executive Dashboard",
        "👥 Customer Analytics",
        "🎯 Customer Segmentation",
        "📈 Demand Forecasting",
        "📦 Inventory Optimization",
        "🚨 Churn Prediction",
        "⚙️ Advanced ML Analytics",
        "🔮 What-If Analysis"
    ],
    index=0,
    label_visibility="collapsed"
)

# Strip icons from selection to get base route
clean_page_name = page_selection.split(" ", 1)[1]

# Inject Light theme custom CSS
st.markdown(styles.get_css(), unsafe_allow_html=True)

# Routing Table (Force light theme)
if clean_page_name == "Executive Dashboard":
    executive_dashboard.render("light")
elif clean_page_name == "Customer Analytics":
    customer_analytics.render("light")
elif clean_page_name == "Customer Segmentation":
    customer_segmentation.render("light")
elif clean_page_name == "Demand Forecasting":
    demand_forecasting.render("light")
elif clean_page_name == "Inventory Optimization":
    inventory_optimization.render("light")
elif clean_page_name == "Churn Prediction":
    churn_prediction.render("light")
elif clean_page_name == "Advanced ML Analytics":
    advanced_ml_analytics.render("light")
elif clean_page_name == "What-If Analysis":
    what_if_analysis.render("light")

# Sidebar Footer
st.sidebar.markdown("<br><br><hr style='margin: 8px 0; opacity: 0.15;'>", unsafe_allow_html=True)
st.sidebar.markdown(
    f"""
    <div style="font-size:0.75rem; color:#64748b; text-align:center;">
        <b>RetailPulse v1.0.0</b><br>
        Commercial Analytics System<br>
        Workspace: <code>Cwd/retail_pulse</code>
    </div>
    """,
    unsafe_allow_html=True
)
