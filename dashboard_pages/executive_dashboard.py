# dashboard_pages/executive_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import utils
import styles

def render(theme="light"):
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">Executive Dashboard</h1>
            <p class="header-subtitle">Key performance indicators, sales volume trends, and product performance overview</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load data
    df_rev = utils.load_csv_data("revenue_trend.csv")
    df_cust = utils.load_csv_data("customer_analytics.csv")
    
    if df_rev.empty or df_cust.empty:
        st.warning("Please verify that all datasets exist in the data/ folder.")
        return

    # Calculate metrics
    total_revenue = df_rev["Revenue"].sum()
    total_orders = df_rev["Orders"].sum()
    total_customers = df_cust["CustomerID"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Render KPI Cards in columns (4 cards)
    kpi_cols = st.columns(4)
    
    with kpi_cols[0]:
        st.markdown(
            styles.render_kpi_card("Total Revenue", utils.format_currency(total_revenue), delta="12.4%", delta_up=True),
            unsafe_allow_html=True
        )
    with kpi_cols[1]:
        st.markdown(
            styles.render_kpi_card("Total Customers", utils.format_number(total_customers), delta="8.2%", delta_up=True),
            unsafe_allow_html=True
        )
    with kpi_cols[2]:
        st.markdown(
            styles.render_kpi_card("Total Orders", utils.format_number(total_orders), delta="10.5%", delta_up=True),
            unsafe_allow_html=True
        )
    with kpi_cols[3]:
        st.markdown(
            styles.render_kpi_card("Average Order Value", utils.format_currency(avg_order_value), delta="1.8%", delta_up=True),
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualizations Row 1: Daily Revenue Trend & Top Categories
    row1_cols = st.columns([2, 1])
    
    with row1_cols[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Daily Revenue Trend</h3>", unsafe_allow_html=True)
        
        fig_rev = px.area(
            df_rev, 
            x="Date", 
            y="Revenue",
            color_discrete_sequence=[utils.DISCRETE_PALETTE[0]]
        )
        fig_rev.update_traces(line=dict(width=2), fillcolor="rgba(99, 102, 241, 0.15)")
        utils.style_plotly_fig(fig_rev, theme)
        st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row1_cols[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Top Categories by Demand</h3>", unsafe_allow_html=True)
        
        df_inv = utils.load_csv_data("inventory_data.csv")
        if not df_inv.empty:
            df_cat = df_inv.groupby("Category")["Demand"].sum().reset_index().sort_values("Demand", ascending=True)
            fig_cat = px.bar(
                df_cat,
                y="Category",
                x="Demand",
                orientation="h",
                color="Demand",
                color_continuous_scale=utils.CONTINUOUS_SCALE
            )
            fig_cat.update_layout(coloraxis_showscale=False)
            utils.style_plotly_fig(fig_cat, theme)
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No category data available.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Visualizations Row 2: Monthly Sales Trend (Clean bar chart)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Monthly Sales Performance</h3>", unsafe_allow_html=True)
    
    df_rev["Month"] = pd.to_datetime(df_rev["Date"]).dt.strftime("%b %Y")
    df_month = df_rev.groupby("Month", sort=False)["Revenue"].sum().reset_index()
    
    fig_month = px.bar(
        df_month,
        x="Month",
        y="Revenue",
        color="Revenue",
        color_continuous_scale=utils.CONTINUOUS_SCALE
    )
    fig_month.update_layout(coloraxis_showscale=False)
    utils.style_plotly_fig(fig_month, theme)
    st.plotly_chart(fig_month, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
