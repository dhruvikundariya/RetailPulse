# dashboard_pages/demand_forecasting.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import utils
import styles

def render(theme="light"):
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">Demand Forecasting</h1>
            <p class="header-subtitle">Machine learning forecasts for sales trends, seasonality, and expected volumes</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load forecast data
    df_fore = utils.load_csv_data("demand_forecast.csv")
    
    if df_fore.empty:
        st.warning("Forecast dataset is not available. Please verify your data/ folder.")
        return

    # Parse dates
    df_fore["Date"] = pd.to_datetime(df_fore["Date"])
    
    # Separate historical and forecast
    hist_df = df_fore[df_fore["HistoricalSales"].notna()]
    fore_df = df_fore[df_fore["ForecastedSales"].notna()]
    
    # Calculate KPIs
    avg_hist_sales = hist_df["HistoricalSales"].mean()
    avg_fore_sales = fore_df["ForecastedSales"].mean()
    
    forecast_growth = ((avg_fore_sales - avg_hist_sales) / avg_hist_sales * 100) if avg_hist_sales > 0 else 0
    expected_revenue = fore_df["ForecastedSales"].sum()
    demand_index = min(100, max(0, int(50 + forecast_growth * 2.5)))
    
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        st.markdown(
            styles.render_kpi_card(
                "Forecast Growth %", 
                f"{forecast_growth:.2f}%", 
                delta="Increased Demand" if forecast_growth > 0 else "Decreased Demand", 
                delta_up=forecast_growth > 0
            ),
            unsafe_allow_html=True
        )
    with kpi_cols[1]:
        st.markdown(
            styles.render_kpi_card(
                "Expected Revenue (30d)", 
                utils.format_currency(expected_revenue), 
                delta="Next 30 Days Forecast", 
                delta_up=True
            ),
            unsafe_allow_html=True
        )
    with kpi_cols[2]:
        st.markdown(
            styles.render_kpi_card(
                "Demand Index", 
                f"{demand_index}/100", 
                delta="Strong Momentum" if demand_index > 70 else "Stable Demand", 
                delta_up=demand_index > 50
            ),
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Forecast Line Chart with Confidence Interval (Main chart)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Historical Sales & Demand Forecast</h3>", unsafe_allow_html=True)
    
    fig = go.Figure()
    
    # Historical Trace
    fig.add_trace(
        go.Scatter(
            x=hist_df["Date"],
            y=hist_df["HistoricalSales"],
            name="Historical Sales",
            line=dict(color="#6366f1", width=3),
            mode="lines"
        )
    )
    
    # Forecast Trace
    fig.add_trace(
        go.Scatter(
            x=fore_df["Date"],
            y=fore_df["ForecastedSales"],
            name="Forecasted Sales",
            line=dict(color="#a855f7", width=3, dash="dash"),
            mode="lines"
        )
    )
    
    # Confidence Interval Shading
    # Upper CI boundary
    fig.add_trace(
        go.Scatter(
            x=fore_df["Date"],
            y=fore_df["UpperCI"],
            showlegend=False,
            line=dict(width=0),
            mode="lines",
            hoverinfo="skip"
        )
    )
    # Lower CI boundary filled to Upper CI
    fig.add_trace(
        go.Scatter(
            x=fore_df["Date"],
            y=fore_df["LowerCI"],
            name="95% Confidence Interval",
            fill="tonexty",
            fillcolor="rgba(168, 85, 247, 0.08)",
            line=dict(width=0),
            mode="lines",
            hoverinfo="skip"
        )
    )
    
    fig.update_layout(
        xaxis_title="Timeline",
        yaxis_title="Unit Sales"
    )
    utils.style_plotly_fig(fig, theme)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Seasonality Analysis
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Weekly Seasonality Analysis</h3>", unsafe_allow_html=True)
    
    hist_df_copy = hist_df.copy()
    hist_df_copy["DayOfWeek"] = hist_df_copy["Date"].dt.day_name()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_season = hist_df_copy.groupby("DayOfWeek")["HistoricalSales"].mean().reindex(order).reset_index()
    
    fig_week = px.bar(
        weekly_season,
        x="DayOfWeek",
        y="HistoricalSales",
        color="HistoricalSales",
        color_continuous_scale=utils.CONTINUOUS_SCALE,
        labels={"DayOfWeek": "Day of the Week", "HistoricalSales": "Average Sales Volume"}
    )
    fig_week.update_layout(coloraxis_showscale=False)
    utils.style_plotly_fig(fig_week, theme)
    st.plotly_chart(fig_week, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
