# dashboard_pages/customer_analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px
import utils
import styles

def render(theme="light"):
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">Customer Analytics</h1>
            <p class="header-subtitle">Deep dive into customer spending patterns, ordering frequencies, and value distribution</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load customer analytics data
    df_cust = utils.load_csv_data("customer_analytics.csv")
    
    if df_cust.empty:
        st.warning("Customer data is not available. Please verify your data/ folder.")
        return

    # Calculate KPIs
    avg_clv = df_cust["CLV"].mean()
    avg_freq = df_cust["PurchaseFrequency"].mean()
    high_value_custs = df_cust[df_cust["CLV"] > 1500]["CustomerID"].nunique()
    
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        st.markdown(
            styles.render_kpi_card("Average Customer CLV", utils.format_currency(avg_clv), delta="4.6%", delta_up=True),
            unsafe_allow_html=True
        )
    with kpi_cols[1]:
        st.markdown(
            styles.render_kpi_card("Avg Purchase Frequency", f"{avg_freq:.1f} orders", delta="1.2%", delta_up=True),
            unsafe_allow_html=True
        )
    with kpi_cols[2]:
        st.markdown(
            styles.render_kpi_card("High-Value Customers", utils.format_number(high_value_custs), delta="5.8%", delta_up=True),
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # First row of charts (Only 2 charts here)
    row1_cols = st.columns([1, 1])
    
    with row1_cols[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Customer Spending Distribution</h3>", unsafe_allow_html=True)
        
        fig_hist = px.histogram(
            df_cust,
            x="Spending",
            nbins=25,
            color_discrete_sequence=[utils.DISCRETE_PALETTE[0]],
            labels={"Spending": "Total Amount Spent ($)"}
        )
        utils.style_plotly_fig(fig_hist, theme)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with row1_cols[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>CLV vs. Purchase Frequency</h3>", unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            df_cust,
            x="PurchaseFrequency",
            y="CLV",
            color="Segment",
            size="Spending",
            color_discrete_sequence=utils.DISCRETE_PALETTE,
            labels={"PurchaseFrequency": "Order Count", "CLV": "Customer Lifetime Value ($)"}
        )
        utils.style_plotly_fig(fig_scatter, theme)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Top Customers Table
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Top Performing Customers</h3>", unsafe_allow_html=True)
    
    top_custs = df_cust.sort_values("CLV", ascending=False).head(8).copy()
    top_custs["Spending"] = top_custs["Spending"].apply(utils.format_currency)
    top_custs["CLV"] = top_custs["CLV"].apply(utils.format_currency)
    
    st.dataframe(
        top_custs,
        column_config={
            "CustomerID": "Customer ID",
            "Spending": "Total Spend",
            "PurchaseFrequency": "Order Frequency",
            "CLV": "Customer Lifetime Value",
            "Segment": "Segment Class"
        },
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
