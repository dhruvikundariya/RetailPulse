# dashboard_pages/what_if_analysis.py
import streamlit as st
import pandas as pd
import numpy as np
import utils
import styles

def render(theme="light"):
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">What-If Analysis</h1>
            <p class="header-subtitle">Simulate business scenarios and model the financial impact of growth, demand, churn, and inventory changes</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load baselines from data
    df_rev = utils.load_csv_data("revenue_trend.csv")
    df_inv = utils.load_csv_data("inventory_data.csv")
    
    if df_rev.empty or df_inv.empty:
        st.warning("Baseline datasets are not available. Please verify your data/ folder.")
        return

    # Calculate current baselines
    baseline_revenue = df_rev["Revenue"].sum()
    baseline_inv_cost = (df_inv["StockLevel"] * 25.0).sum()
    baseline_retention = 78.4
    
    total_products = len(df_inv)
    out_of_stock_products = len(df_inv[df_inv["Status"] == "Out of Stock"])
    baseline_stockout_risk = (out_of_stock_products / total_products * 100) if total_products > 0 else 8.0
    if baseline_stockout_risk == 0:
        baseline_stockout_risk = 8.0

    # Layout: Controls on left, results on right
    layout_cols = st.columns([1, 2])
    
    with layout_cols[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Scenario Variables</h3>", unsafe_allow_html=True)
        st.write("Adjust variables to simulate market conditions:")
        
        # Sliders
        rev_growth = st.slider("Revenue Growth %", -20, 50, 10, step=1, help="Expected organic customer acquisition growth")
        demand_increase = st.slider("Demand Volume Increase %", -10, 50, 15, step=1, help="Spike in customer transactions and sales volume")
        churn_change = st.slider("Churn Rate Change %", -30, 30, -5, step=1, help="Percentage point shift in customer churn (Negative is improvement)")
        inv_buffer = st.slider("Inventory Safety Buffer %", 0, 100, 20, step=5, help="Extra safety stock held to prevent stockouts")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with layout_cols[1]:
        # Perform dynamic simulations
        proj_revenue = baseline_revenue * (1 + rev_growth / 100) * (1 + (demand_increase * 0.8) / 100)
        rev_diff = proj_revenue - baseline_revenue
        rev_delta_pct = (rev_diff / baseline_revenue * 100)
        
        proj_inv_cost = baseline_inv_cost * (1 + (demand_increase * 0.5) / 100) * (1 + (inv_buffer * 0.8) / 100)
        inv_diff = proj_inv_cost - baseline_inv_cost
        inv_delta_pct = (inv_diff / baseline_inv_cost * 100)
        
        proj_retention = min(99.5, max(30.0, baseline_retention - churn_change))
        retention_diff = proj_retention - baseline_retention
        
        proj_stockout_risk = baseline_stockout_risk * (1 + demand_increase / 100) / (1 + inv_buffer / 100)
        proj_stockout_risk = min(100.0, max(0.5, proj_stockout_risk))
        stockout_diff = proj_stockout_risk - baseline_stockout_risk
        
        # Display simulated metrics in 2x2 grid
        metric_cols = st.columns(2)
        
        with metric_cols[0]:
            st.markdown(
                styles.render_kpi_card(
                    "Projected Revenue", 
                    utils.format_currency(proj_revenue), 
                    delta=f"{rev_delta_pct:+.1f}% vs baseline", 
                    delta_up=rev_diff >= 0
                ),
                unsafe_allow_html=True
            )
            st.markdown(
                styles.render_kpi_card(
                    "Projected Retention Rate", 
                    f"{proj_retention:.1f}%", 
                    delta=f"{retention_diff:+.1f}% vs baseline", 
                    delta_up=retention_diff >= 0
                ),
                unsafe_allow_html=True
            )
            
        with metric_cols[1]:
            st.markdown(
                styles.render_kpi_card(
                    "Projected Inventory Cost", 
                    utils.format_currency(proj_inv_cost), 
                    delta=f"{inv_delta_pct:+.1f}% vs baseline", 
                    delta_up=inv_diff <= 0
                ),
                unsafe_allow_html=True
            )
            st.markdown(
                styles.render_kpi_card(
                    "Projected Stockout Risk", 
                    f"{proj_stockout_risk:.1f}%", 
                    delta=f"{stockout_diff:+.1f}% vs baseline", 
                    delta_up=stockout_diff <= 0
                ),
                unsafe_allow_html=True
            )
            
    # Strategic Recommendation Engine
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color:#8b5cf6;'>Scenario Recommendation Engine</h3>", unsafe_allow_html=True)
    
    if proj_stockout_risk > 15:
        rec_title = "WARNING: HIGH STOCKOUT RISK"
        rec_desc = "Your simulated demand volume increase is outpacing your inventory safety buffer. This is highly likely to cause stockouts on high-demand items, resulting in lost sales and customer frustration. **Action:** Increase your Inventory Safety Buffer to at least 35% or prioritize vendor delivery speed."
        rec_badge = "badge-danger"
    elif proj_revenue > baseline_revenue * 1.15 and proj_inv_cost < baseline_inv_cost * 1.1:
        rec_title = "OPTIMIZED HIGH-GROWTH SCENARIO"
        rec_desc = "Excellent operational balance! Your organic revenue growth and customer retention enhancements are generating high returns while inventory costs are kept in check. Capital efficiency is maximized. **Action:** Proceed with marketing campaigns and maintain current inventory parameters."
        rec_badge = "badge-success"
    elif churn_change > 10:
        rec_title = "CRITICAL CHURN RISK WARNING"
        rec_desc = "A 10% or higher increase in customer churn will erode your organic revenue gains. It costs 5x more to acquire a new customer than to retain an existing one. **Action:** Launch an immediate re-engagement email sequence to 'At Risk' customers with targeted discount offers."
        rec_badge = "badge-danger"
    else:
        rec_title = "STABLE OPERATIONAL EQUILIBRIUM"
        rec_desc = "The simulated inputs indicate stable business continuity. Revenue and customer metrics remain healthy, and stockout risk is under control. **Action:** Continuously monitor RFM cluster movements to identify early-warning churn signals."
        rec_badge = "badge-warning"
        
    st.markdown(
        f"""
        <div style="padding: 12px 18px; border-radius: 10px; background-color: rgba(99, 102, 241, 0.05); border-left: 5px solid #8b5cf6;">
            <div style="font-weight: 800; font-size: 1.05rem; display: flex; align-items: center; gap: 10px;">
                <span class="badge {rec_badge}">{rec_title}</span>
            </div>
            <p style="margin-top: 8px; margin-bottom: 0; font-size: 0.95rem; line-height: 1.5; color: #4b5563;">{rec_desc}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
