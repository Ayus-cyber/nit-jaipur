import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analysis import load_data, analyze_inventory_sales_correlation, identify_missed_opportunities, simulate_optimization_impact
from models import build_future_spend_model, predict_promotions

st.set_page_config(page_title="Store Performance Analytics", layout="wide")

st.title("📊 Retail Inventory & Store Performance Dashboard")

# Load Data
try:
    stores, products, customers, sales, promotions = load_data()
except FileNotFoundError:
    st.error("Data not found. Please run `python src/data_generator.py` first.")
    st.stop()

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Overview", "Inventory Correlation", "Customer Predictions", "Promo Recommendations", "Optimization Simulations"])

if page == "Overview":
    st.header("Global KPIs")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Stores", len(stores))
    col2.metric("Total Products", len(products))
    col3.metric("Total Customers", len(customers))
    col4.metric("Total Revenue", f"${sales['total_amount'].sum():,.0f}")
    
    st.subheader("Recent Sales Trend")
    sales_trend = sales.groupby('date')['total_amount'].sum().reset_index()
    fig = px.line(sales_trend, x='date', y='total_amount', title="Daily Sales Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Inventory Correlation":
    st.header("Goal 1: Inventory vs Sales Correlation")
    
    analysis_df, correlation = analyze_inventory_sales_correlation(sales, products)
    
    st.metric("Correlation Coefficient (Stock vs Sales Velocity)", f"{correlation:.2f}")
    
    if correlation > 0.5:
        st.success("Strong positive correlation: Better stock levels drive higher sales.")
    elif correlation < -0.5:
        st.warning("Negative correlation: Verify if low stock items are artificially limited.")
    else:
        st.info("Weak correlation: Sales may be driven by factors other than stock availability.")
        
    fig = px.scatter(analysis_df, x='current_stock_level', y='sales_velocity_30d', 
                     hover_name='product_name', color='category',
                     title="Stock Level vs Sales Velocity (30d)", trendline="ols")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(analysis_df)

elif page == "Customer Predictions":
    st.header("Goal 2: Future Spend Prediction")
    st.write("Predicted customer spend for the next quarter based on RFM analysis.")
    
    with st.spinner("Training model..."):
        pred_df, model = build_future_spend_model(sales, customers)
    
    col1, col2 = st.columns(2)
    col1.metric("Avg Predicted Spend", f"${pred_df['predicted_future_spend'].mean():.2f}")
    
    fig = px.histogram(pred_df, x='predicted_future_spend', title="Distribution of Predicted Spend")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(pred_df.sort_values('predicted_future_spend', ascending=False))

elif page == "Promo Recommendations":
    st.header("Goal 3: Personalized Promotion Logic")
    
    promo_df = predict_promotions(customers, sales, promotions)
    
    st.write("Recommended discount percentages based on Loyalty Tier and Recency.")
    
    fig = px.box(promo_df, x='loyalty_status', y='recommended_discount', title="Discount Range by Loyalty Tier")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(promo_df)

elif page == "Optimization Simulations":
    st.header("Goal 4 & 5: Inventory Optimization Impact")
    
    # Sensitivity
    st.subheader("Goal 4: Missed Opportunities (Stockouts)")
    opp_customers, num_low_items = identify_missed_opportunities(sales, products, customers)
    st.metric("Low Stock Items (<10 units)", num_low_items)
    st.write(f"Customers affected by low stock in their preferred categories: {len(opp_customers)}")
    st.dataframe(opp_customers.head(10))
    
    # Optimization
    st.subheader("Goal 5: Revenue Uplift from Optimization")
    uplift, sim_df = simulate_optimization_impact(sales, products)
    
    st.metric("Potential Revenue Uplift", f"${uplift:,.2f}", delta="Estimated Gain")
    st.write("This simulation assumes a 20% sales recovery for items currently facing stockouts if inventory was optimized.")
    
    fig = px.bar(sim_df.sort_values('estimated_missed_revenue', ascending=False).head(10), 
                 x='product_name', y='estimated_missed_revenue',
                 title="Top 10 Products with Missed Revenue Opportunity")
    st.plotly_chart(fig, use_container_width=True)
