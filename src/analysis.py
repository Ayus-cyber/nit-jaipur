import pandas as pd
import numpy as np

def load_data(base_path="data"):
    stores = pd.read_csv(f"{base_path}/stores.csv")
    products = pd.read_csv(f"{base_path}/products.csv")
    customers = pd.read_csv(f"{base_path}/customer_details.csv")
    sales = pd.read_csv(f"{base_path}/store_sales_line_items.csv")
    promotions = pd.read_csv(f"{base_path}/promotion_details.csv")
    
    # Convert dates
    sales['date'] = pd.to_datetime(sales['date'])
    customers['last_purchase_date'] = pd.to_datetime(customers['last_purchase_date'])
    
    return stores, products, customers, sales, promotions

def analyze_inventory_sales_correlation(sales, products):
    """
    Goal 1: Analyze how inventory levels correlate with sales.
    We aggregate sales by product and compare with current stock.
    """
    # Sales velocity (items sold in last 30 days)
    recent_date = sales['date'].max() - pd.Timedelta(days=30)
    recent_sales = sales[sales['date'] >= recent_date]
    
    product_sales = recent_sales.groupby('product_id')['quantity'].sum().reset_index()
    product_sales.rename(columns={'quantity': 'sales_velocity_30d'}, inplace=True)
    
    # Merge with stock levels
    analysis_df = pd.merge(products[['product_id', 'product_name', 'current_stock_level', 'category']], 
                           product_sales, on='product_id', how='left')
    analysis_df['sales_velocity_30d'] = analysis_df['sales_velocity_30d'].fillna(0)
    
    # Correlation
    correlation = analysis_df[['current_stock_level', 'sales_velocity_30d']].corr().iloc[0,1]
    
    return analysis_df, correlation

def identify_missed_opportunities(sales, products, customers):
    """
    Goal 4: Which customers are likely to increase spending if inventory improves?
    Logic: Find customers who bought items in the past that are now low in stock.
    """
    low_stock_threshold = 10
    low_stock_products = products[products['current_stock_level'] < low_stock_threshold]['product_id'].tolist()
    
    # Find customers who historically bought these products
    target_sales = sales[sales['product_id'].isin(low_stock_products)]
    target_customers = target_sales['customer_id'].unique()
    
    # Get details
    opportunity_customers = customers[customers['customer_id'].isin(target_customers)].copy()
    opportunity_customers['potential_spend_increase'] = "High" # Placeholder logic
    
    return opportunity_customers, len(low_stock_products)

def simulate_optimization_impact(sales, products):
    """
    Goal 5: How will store-level inventory optimization impact overall sales?
    Simulation: Assume low stock items had adequate stock, extrapolate sales velocity.
    """
    # Calculate average daily sales per product
    daily_sales = sales.groupby(['product_id', 'date'])['quantity'].sum().reset_index()
    avg_daily_sales = daily_sales.groupby('product_id')['quantity'].mean().reset_index()
    avg_daily_sales.rename(columns={'quantity': 'avg_daily_units'}, inplace=True)
    
    # Merge
    sim_df = pd.merge(products, avg_daily_sales, on='product_id', how='left')
    sim_df['avg_daily_units'] = sim_df['avg_daily_units'].fillna(0)
    
    # Scenario: If stock was 0, we missed sales. 
    # Let's assume for items with stock < 5, we missed 20% of potential sales due to stockouts
    sim_df['estimated_missed_sales_units'] = sim_df.apply(
        lambda x: x['avg_daily_units'] * 30 * 0.2 if x['current_stock_level'] < 5 else 0, axis=1
    )
    
    sim_df['estimated_missed_revenue'] = sim_df['estimated_missed_sales_units'] * sim_df['standard_price']
    
    total_potential_uplift = sim_df['estimated_missed_revenue'].sum()
    
    return total_potential_uplift, sim_df
