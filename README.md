# RetailPulse – AI-Powered Customer Analytics & Demand Forecasting Platform

## Project Overview

RetailPulse is a Business Intelligence and Customer Analytics platform developed using Data Science, Machine Learning, and Streamlit.

The system helps retail businesses analyze customer behavior, forecast future demand, identify potential customer churn, optimize inventory levels, and support business decision-making through interactive dashboards.

The platform transforms raw retail transaction data into actionable insights using advanced analytics and predictive modeling.

## Problem Statement

Retail businesses generate large volumes of customer transaction data every day. However, extracting meaningful insights from this data is challenging.

RetailPulse addresses this challenge by providing:

- Customer Segmentation
- Revenue Analysis
- Demand Forecasting
- Churn Prediction
- Inventory Optimization
- What-If Business Simulations

through a unified analytics dashboard.

## Features

### Executive Dashboard
- Business KPI monitoring
- Revenue tracking
- Customer analytics

### Customer Analytics
- Customer behavior analysis
- Revenue contribution insights

### Customer Segmentation
- RFM Analysis
- Customer grouping

### Demand Forecasting
- Future sales prediction
- Trend analysis

### Churn Prediction
- High-risk customer identification
- Customer retention insights

### Inventory Optimization
- Reorder recommendations
- Stock management support

### What-If Analysis
- Business scenario simulation
- Strategic decision support

## Tech Stack

### Programming Language
- Python

### Data Analysis
- Pandas
- NumPy

### Machine Learning
- Scikit-Learn

### Data Visualization
- Plotly
- Matplotlib
- Seaborn

### Dashboard Development
- Streamlit

### Deployment
- Docker
- Streamlit Cloud

### Dataset
- Online Retail II Dataset

## Project Structure

RetailPulse/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
│
├── dashboard_pages/
├── data/
├── models/
├── notebooks/
├── utils.py
└── styles.py

## Installation

Clone the repository:

git clone <repository-link>

cd retailpulse

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

## Dashboard Modules

The application contains:

1. Executive Dashboard
2. Customer Analytics
3. Customer Segmentation
4. Demand Forecasting
5. Inventory Optimization
6. Churn Prediction
7. Advanced Analytics
8. What-If Analysis

## Machine Learning Models

- Linear Regression
- Random Forest Regressor
- Decision Tree Regressor
- Gradient Boosting Regressor

Model performance was evaluated using standard machine learning metrics and compared to select the best-performing model.

## Results

RetailPulse successfully provides:

- Customer Segmentation using RFM Analysis
- Sales Trend Visualization
- Demand Forecasting
- Customer Churn Detection
- Inventory Optimization Insights
- Interactive Business Intelligence Dashboard

The platform enables data-driven decision-making for retail businesses.

## Future Improvements

- Real-time data integration
- Cloud deployment enhancements
- Automated model retraining
- Advanced recommendation engine
- Mobile responsive dashboard

## Author

Dhruvi Kundariya

Computer Science & Engineering
CHARUSAT University

Project: RetailPulse – AI-Powered Customer Analytics & Demand Forecasting Platform

## Dataset

The project uses the Online Retail II dataset containing customer transactions, invoice details, product purchases, quantities, and revenue information. The dataset was cleaned and transformed for customer analytics, demand forecasting, churn prediction, and inventory optimization.

## Docker Support

Build Docker Image:

docker build -t retailpulse .

Run Docker Container:

docker run -p 8501:8501 retailpulse

## Live Demo

Streamlit Cloud Deployment:

https://retailpulse-dhruvi.streamlit.app

## Screenshots

Dashboard screenshots are available below.
