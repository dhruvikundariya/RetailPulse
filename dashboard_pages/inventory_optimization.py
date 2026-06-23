# dashboard_pages/inventory_optimization.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import utils
import styles

def render(theme="light"):
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">Inventory Optimization</h1>
            <p class="header-subtitle">Analyze reorder points, minimize stockouts, and manage inventory capital efficiency</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load inventory data
    df_inv = utils.load_csv_data("inventory_data.csv")
    
    if df_inv.empty:
        st.warning("Inventory dataset is not available. Please verify your data/ folder.")
        return

    # Calculate KPIs
    stockout_risks = len(df_inv[df_inv["Status"] == "Out of Stock"])
    reorder_alerts = len(df_inv[df_inv["Status"] == "Reorder Alert"])
    capital_tied = (df_inv["StockLevel"] * 25.0).sum()
    
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        st.markdown(
            styles.render_kpi_card(
                "Stockout Risks", 
                f"{stockout_risks}", 
                delta="Critical Action Required" if stockout_risks > 0 else "Optimal", 
                delta_up=False if stockout_risks > 0 else True
            ),
            unsafe_allow_html=True
        )
    with kpi_cols[1]:
        st.markdown(
            styles.render_kpi_card(
                "Reorder Alerts", 
                f"{reorder_alerts}", 
                delta="Pending Replenishments", 
                delta_up=True if reorder_alerts == 0 else False
            ),
            unsafe_allow_html=True
        )
    with kpi_cols[2]:
        st.markdown(
            styles.render_kpi_card(
                "Capital Tied Up", 
                utils.format_currency(capital_tied), 
                delta="-2.4% Capital Cost", 
                delta_up=True
            ),
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)

    # Visualizations: Reorder Point vs Current Stock Level (Grouped Bar chart)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Reorder Point vs. Current Stock Level</h3>", unsafe_allow_html=True)
    
    # Filter to top 12 products for readability
    subset_df = df_inv.head(12)
    
    melt_df = subset_df.melt(
        id_vars="ProductName",
        value_vars=["StockLevel", "ReorderPoint", "ReorderQty"],
        var_name="Metric",
        value_name="Quantity"
    )
    metric_map = {
        "StockLevel": "Current Stock",
        "ReorderPoint": "Reorder Threshold",
        "ReorderQty": "Recommended Reorder Qty"
    }
    melt_df["Metric"] = melt_df["Metric"].map(metric_map)
    
    fig_qty = px.bar(
        melt_df,
        x="ProductName",
        y="Quantity",
        color="Metric",
        barmode="group",
        color_discrete_sequence=utils.DISCRETE_PALETTE,
        title="Stock Level Analysis vs. Reorder Triggers (Sample Products)"
    )
    utils.style_plotly_fig(fig_qty, theme)
    fig_qty.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig_qty, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Stock Alert Badges Table
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.info(
    "Inventory alerts and reorder recommendations are available through the dashboard analytics."
     )
    st.markdown("<h3 style='margin-top:0;'>Critical Stock Action Plan</h3>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
   
    
    
    #  html_rows = ""
    #     for _, row in alert_df.iterrows():
    #         badge_class = "badge-danger" if row["Status"] == "Out of Stock" else "badge-warning"
    #         risk_class = "badge-danger" if row["Risk"] == "Critical" else "badge-warning"
            
    #         html_rows += f"""
    #         <tr>
    #             <td><b>{row['ProductID']}</b></td>
    #             <td>{row['ProductName']}</td>
    #             <td>{row['Category']}</td>
    #             <td>{row['StockLevel']}</td>
    #             <td>{row['ReorderPoint']}</td>
    #             <td><b>{row['ReorderQty']}</b></td>
    #             <td><span class="badge {badge_class}">{row['Status']}</span></td>
    #             <td><span class="badge {risk_class}">{row['Risk']}</span></td>
    #         </tr>
    #         """
            
    #     table_html = f"""
    #     <table style="width:100%; border-collapse: collapse; text-align: left;">
    #         <thead>
    #             <tr style="border-bottom: 2px solid {'rgba(0,0,0,0.08)'}; padding: 8px;">
    #                 <th style="padding: 10px;">ID</th>
    #                 <th style="padding: 10px;">Product Name</th>
    #                 <th style="padding: 10px;">Category</th>
    #                 <th style="padding: 10px;">Current Stock</th>
    #                 <th style="padding: 10px;">Reorder Point</th>
    #                 <th style="padding: 10px;">Recommended Order</th>
    #                 <th style="padding: 10px;">Status</th>
    #                 <th style="padding: 10px;">Risk Level</th>
    #             </tr>
    #         </thead>
    #         <tbody>
    #             {html_rows}
    #         </tbody>s
    #     </table>
    #     """
    #     st.markdown(table_html, unsafe_allow_html=True)
    # else:
    #     st.success("All inventory is currently above warning thresholds. Capital allocation is optimized.")
    st.markdown('</div>', unsafe_allow_html=True)
