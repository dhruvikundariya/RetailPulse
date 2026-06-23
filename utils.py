# utils.py
import os
import pandas as pd
import numpy as np
import pickle
import plotly.io as pio

# Set Plotly default template to none so our custom styling takes full effect
pio.templates.default = "none"

def ensure_directories():
    """Ensure data/ and models/ directories exist."""
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)

def generate_sample_data():
    """
    Generates realistic, high-quality, static datasets and saves them to data/
    and a pre-trained Random Forest model in models/ if they don't exist.
    This ensures the dashboard runs out-of-the-box before the user connects their final files.
    """
    ensure_directories()
    
    # 1. Executive & Revenue Trend (past 12 months)
    revenue_file = os.path.join("data", "revenue_trend.csv")
    if not os.path.exists(revenue_file):
        dates = pd.date_range(start="2025-06-01", end="2026-05-31", freq="D")
        np.random.seed(42)
        
        # Base trend with seasonality and weekly cycle
        base = np.linspace(20000, 35000, len(dates))
        seasonality = 5000 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
        weekly = 3000 * (dates.dayofweek >= 5)  # weekend bump
        noise = np.random.normal(0, 1500, len(dates))
        
        revenue = base + seasonality + weekly + noise
        orders = (revenue / np.random.normal(85, 3, len(dates))).astype(int)
        customers = (orders * np.random.uniform(0.85, 0.95, len(dates))).astype(int)
        
        df_rev = pd.DataFrame({
            "Date": dates.strftime("%Y-%m-%d"),
            "Revenue": np.round(revenue, 2),
            "Orders": orders,
            "Customers": customers
        })
        df_rev.to_csv(revenue_file, index=False)

    # 2. Customer Analytics & Spending (1000 customers)
    cust_analytics_file = os.path.join("data", "customer_analytics.csv")
    if not os.path.exists(cust_analytics_file):
        np.random.seed(42)
        n_cust = 1000
        
        spending = np.random.exponential(scale=500, size=n_cust) + 50
        freq = np.random.poisson(lam=4, size=n_cust) + 1
        clv = spending * freq * np.random.uniform(1.2, 2.5, size=n_cust)
        
        # Assign segments based on CLV and Frequency
        segments = []
        for c, f in zip(clv, freq):
            if c > 2500 and f >= 7:
                segments.append("Champions")
            elif c > 1200 and f >= 4:
                segments.append("Loyal Customers")
            elif c > 500 and f >= 2:
                segments.append("New Customers")
            elif c > 200 and f < 2:
                segments.append("At Risk Customers")
            else:
                segments.append("Lost Customers")
                
        df_cust = pd.DataFrame({
            "CustomerID": [f"CUST-{10000+i}" for i in range(n_cust)],
            "Spending": np.round(spending, 2),
            "PurchaseFrequency": freq,
            "CLV": np.round(clv, 2),
            "Segment": segments
        })
        df_cust.to_csv(cust_analytics_file, index=False)

    # 3. RFM Clustering Results
    rfm_file = os.path.join("data", "rfm_data.csv")
    if not os.path.exists(rfm_file):
        np.random.seed(42)
        n_cust = 1000
        
        recency = np.random.randint(1, 365, size=n_cust)
        frequency = np.random.poisson(lam=5, size=n_cust) + 1
        monetary = np.random.exponential(scale=300, size=n_cust) + 30
        
        # Simple clustering assignment
        cluster = []
        segment = []
        for r, f, m in zip(recency, frequency, monetary):
            if r <= 30 and f >= 8 and m >= 800:
                cluster.append(0) # Cluster 0: Champions
                segment.append("Champions")
            elif r <= 90 and f >= 4 and m >= 400:
                cluster.append(1) # Cluster 1: Loyal
                segment.append("Loyal Customers")
            elif r <= 60 and f <= 2:
                cluster.append(2) # Cluster 2: New
                segment.append("New Customers")
            elif r > 180 and f >= 3:
                cluster.append(3) # Cluster 3: Can't Lose Them / At Risk
                segment.append("At Risk Customers")
            else:
                cluster.append(4) # Cluster 4: Hibernating / Lost
                segment.append("Lost Customers")

        df_rfm = pd.DataFrame({
            "CustomerID": [f"CUST-{10000+i}" for i in range(n_cust)],
            "Recency": recency,
            "Frequency": frequency,
            "Monetary": np.round(monetary, 2),
            "Segment": segment,
            "Cluster": cluster
        })
        df_rfm.to_csv(rfm_file, index=False)

    # 4. Demand Forecasting (historical + 30 days forecast)
    forecast_file = os.path.join("data", "demand_forecast.csv")
    if not os.path.exists(forecast_file):
        np.random.seed(42)
        dates = pd.date_range(start="2026-05-01", end="2026-06-30", freq="D")
        
        sales = []
        forecast = []
        lower_ci = []
        upper_ci = []
        
        for i, d in enumerate(dates):
            # Base sales function
            base_val = 1200 + 300 * np.sin(2 * np.pi * d.dayofyear / 365) + (d.dayofweek >= 5) * 400
            
            if d <= pd.Timestamp("2026-05-31"):
                # Historical
                val = base_val + np.random.normal(0, 100)
                sales.append(round(val, 2))
                forecast.append(None)
                lower_ci.append(None)
                upper_ci.append(None)
            else:
                # Forecasted
                sales.append(None)
                f_val = base_val + 50 # Add a small trend
                forecast.append(round(f_val, 2))
                lower_ci.append(round(f_val - 150 - (i-31)*5, 2)) # CI expands over time
                upper_ci.append(round(f_val + 150 + (i-31)*5, 2))
                
        df_forecast = pd.DataFrame({
            "Date": dates.strftime("%Y-%m-%d"),
            "HistoricalSales": sales,
            "ForecastedSales": forecast,
            "LowerCI": lower_ci,
            "UpperCI": upper_ci
        })
        df_forecast.to_csv(forecast_file, index=False)

    # 5. Inventory Optimization (50 products)
    inventory_file = os.path.join("data", "inventory_data.csv")
    if not os.path.exists(inventory_file):
        np.random.seed(42)
        products = [
            "Optima Serum", "Luxe Hydrator", "Aqua Cleanser", "Derma Toner",
            "Glow Oil", "Revive Cream", "Brightening Gel", "Mineral SPF",
            "Charcoal Mask", "Squalane Drop", "Retinol Boost", "Peptide Filler",
            "C-Boost Serum", "Clay Detox", "Rose Mist", "Exfoliating Scrub",
            "Night Repair", "Eye Lift Cream", "Lip Plumper", "Hyaluronic Acid",
            "Niacinamide 10%", "Salicylic Gel", "Zinc Balm", "Centella Toner",
            "Ceramide Cream"
        ] * 2
        # Add suffixes to distinguish duplicates
        products = [f"{p} ({'Standard' if i < 25 else 'Pro'})" for i, p in enumerate(products)]
        categories = ["Serums", "Moisturizers", "Cleansers", "Toners", "Treatments"] * 10
        
        demand = np.random.randint(50, 800, size=50)
        stock = np.random.randint(10, 500, size=50)
        reorder_point = (demand * 0.15 + np.random.randint(20, 50, size=50)).astype(int)
        reorder_qty = (demand * 0.4).astype(int)
        
        status = []
        risk = []
        for s, rp in zip(stock, reorder_point):
            if s <= rp * 0.3:
                status.append("Out of Stock")
                risk.append("Critical")
            elif s <= rp:
                status.append("Reorder Alert")
                risk.append("High")
            elif s <= rp * 1.5:
                status.append("Good")
                risk.append("Medium")
            else:
                status.append("Overstocked")
                risk.append("Low")
                
        df_inv = pd.DataFrame({
            "ProductID": [f"PROD-{2000+i}" for i in range(50)],
            "ProductName": products,
            "Category": categories,
            "Demand": demand,
            "StockLevel": stock,
            "ReorderPoint": reorder_point,
            "ReorderQty": reorder_qty,
            "Status": status,
            "Risk": risk
        })
        df_inv.to_csv(inventory_file, index=False)

    # 6. Churn Prediction & Customers
    churn_file = os.path.join("data", "churn_data.csv")
    if not os.path.exists(churn_file):
        np.random.seed(42)
        n_cust = 200
        
        names = [
            "Sophia Martinez", "Liam Anderson", "Olivia Taylor", "Noah Thomas", 
            "Jackson White", "Emma Harris", "Aiden Martin", "Ava Thompson", 
            "Lucas Garcia", "Isabella Martinez", "Mia Robinson", "Ethan Clark",
            "Charlotte Rodriguez", "Oliver Lewis", "Amelia Lee", "Elijah Walker",
            "Harper Hall", "James Allen", "Evelyn Young", "Benjamin King",
            "Logan Wright", "Abigail Scott", "Alexander Green", "Emily Baker",
            "Michael Adams", "Elizabeth Nelson", "Daniel Hill", "Sofia Ramirez",
            "Henry Campbell", "Avery Mitchell", "Sebastian Roberts", "Evelyn Carter"
        ] * 7
        names = names[:n_cust]
        
        prob = np.random.beta(a=2, b=5, size=n_cust)
        prob = np.round(prob, 3)
        
        risk_cats = []
        for p in prob:
            if p >= 0.7:
                risk_cats.append("High Risk")
            elif p >= 0.40:
                risk_cats.append("Medium Risk")
            else:
                risk_cats.append("Low Risk")
                
        df_churn = pd.DataFrame({
            "CustomerID": [f"CUST-{10000+i}" for i in range(n_cust)],
            "Name": names,
            "ChurnProbability": prob,
            "RiskCategory": risk_cats,
            "LastActiveDays": np.random.randint(1, 180, size=n_cust),
            "Status": ["Active" if p < 0.7 else "At Risk" for p in prob]
        })
        df_churn.to_csv(churn_file, index=False)

    # 7. Model Metrics & Feature Importance
    metrics_file = os.path.join("data", "model_metrics.csv")
    if not os.path.exists(metrics_file):
        df_metrics = pd.DataFrame({
            "Model": ["Random Forest", "XGBoost", "Gradient Boosting", "Logistic Regression"],
            "Accuracy": [0.895, 0.884, 0.879, 0.812],
            "Precision": [0.882, 0.871, 0.865, 0.785],
            "Recall": [0.854, 0.840, 0.835, 0.742],
            "F1_Score": [0.868, 0.855, 0.850, 0.763]
        })
        df_metrics.to_csv(metrics_file, index=False)
        
    feat_file = os.path.join("data", "feature_importance.csv")
    if not os.path.exists(feat_file):
        df_feat = pd.DataFrame({
            "Feature": ["Monetary Value", "Purchase Frequency", "Recency (Days)", "Last Order Value", "Discount Usage %", "Support Tickets", "Account Age (Months)", "Web Session Time"],
            "Importance": [0.324, 0.245, 0.187, 0.092, 0.063, 0.045, 0.029, 0.015]
        })
        df_feat.to_csv(feat_file, index=False)

    # 8. Pre-trained Mock Random Forest Model (to support live simulation/prediction)
    model_file = os.path.join("models", "random_forest_churn.pkl")
    if not os.path.exists(model_file):
        try:
            from sklearn.ensemble import RandomForestClassifier
            # Train a simple model on 3 features: Recency, Frequency, Monetary
            X = np.random.randn(100, 3)
            y = np.random.randint(0, 2, 100)
            model = RandomForestClassifier(n_estimators=10, random_state=42)
            model.fit(X, y)
            with open(model_file, "wb") as f:
                pickle.dump(model, f)
        except ImportError:
            # If sklearn is not available, we save a mock class that emulates it
            class MockRF:
                def predict_proba(self, X):
                    # Expects 2D array, returns probabilities
                    return np.array([[1 - 0.35, 0.35] for _ in range(len(X))])
            mock_model = MockRF()
            with open(model_file, "wb") as f:
                pickle.dump(mock_model, f)

def load_csv_data(filename):
    """Safely loads a CSV file from data/ folder."""
    path = os.path.join("data", filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        # Fallback to empty df if missing
        return pd.DataFrame()

def load_ml_model(filename):
    """Safely loads a pickled ML model from models/ folder."""
    path = os.path.join("models", filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def style_plotly_fig(fig, theme="dark"):
    """
    Applies unified premium CSS theme values to a Plotly figure.
    """
    if theme == "dark":
        text_color = "#f3f4f6"
        grid_color = "rgba(255, 255, 255, 0.08)"
        zeroline_color = "rgba(255, 255, 255, 0.15)"
        tooltip_bg = "#1f2937"
        tooltip_border = "#374151"
    else:
        text_color = "#1e293b"
        grid_color = "rgba(0, 0, 0, 0.05)"
        zeroline_color = "rgba(0, 0, 0, 0.1)"
        tooltip_bg = "#ffffff"
        tooltip_border = "#e2e8f0"

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit, sans-serif", color=text_color, size=12),
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=text_color)
        ),
        hoverlabel=dict(
            bgcolor=tooltip_bg,
            bordercolor=tooltip_border,
            font=dict(family="Outfit, sans-serif", size=12, color=text_color)
        )
    )
    
    # Configure axes
    fig.update_xaxes(
        showgrid=True,
        gridcolor=grid_color,
        zeroline=True,
        zerolinecolor=zeroline_color,
        tickfont=dict(color=text_color)
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=grid_color,
        zeroline=True,
        zerolinecolor=zeroline_color,
        tickfont=dict(color=text_color)
    )
    
    return fig

# Custom discrete color palette matching blue-purple SaaS branding
DISCRETE_PALETTE = ['#6366f1', '#a855f7', '#ec4899', '#3b82f6', '#10b981', '#f59e0b', '#64748b']
CONTINUOUS_SCALE = [[0.0, '#6366f1'], [0.5, '#a855f7'], [1.0, '#ec4899']]

def format_currency(val):
    """Format value as USD currency."""
    if val >= 1_000_000:
        return f"${val / 1_000_000:.2f}M"
    elif val >= 1_000:
        return f"${val / 1_000:.1f}K"
    return f"${val:.2f}"

def format_number(val):
    """Format integers nicely."""
    if val >= 1_000_000:
        return f"{val / 1_000_000:.2f}M"
    elif val >= 1_000:
        return f"{val / 1_000:.1f}K"
    return f"{val:,}"
