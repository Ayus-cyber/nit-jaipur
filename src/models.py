import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def build_future_spend_model(sales, customers):
    """
    Goal 2: Estimate future spend next quarter.
    """
    # 1. Feature Engineering: RFM
    # Aggregate sales by customer
    customer_metrics = sales.groupby('customer_id').agg({
        'date': lambda x: (sales['date'].max() - x.max()).days, # Recency
        'transaction_id': 'count', # Frequency
        'total_amount': 'sum' # Monetary
    }).reset_index()
    
    customer_metrics.columns = ['customer_id', 'recency', 'frequency', 'total_spend']
    
    # Merge with customer details
    data = pd.merge(customers, customer_metrics, on='customer_id', how='left')
    data.fillna(0, inplace=True)
    
    # Target Variable Simulation: 
    # In a real scenario, we'd predict next qtr based on stats. 
    # Here, we'll simulate "Future Spend" as a function of past behavior + noise for demo purposes
    # Since we generated random data, we need a proxy target to train a model that "looks" real.
    data['future_spend_target'] = (
        data['total_spend'] * 0.2 + 
        (1000 - data['recency']) * 0.5 + 
        np.random.normal(0, 50, len(data))
    )
    data['future_spend_target'] = data['future_spend_target'].clip(lower=0)
    
    # Encode categorical
    le = LabelEncoder()
    data['loyalty_code'] = le.fit_transform(data['loyalty_status'])
    
    features = ['recency', 'frequency', 'total_spend', 'total_loyalty_points', 'loyalty_code']
    X = data[features]
    y = data['future_spend_target']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    data['predicted_future_spend'] = model.predict(X)
    
    return data[['customer_id', 'first_name', 'predicted_future_spend', 'future_spend_target']], model

def predict_promotions(customers, sales, promotions):
    """
    Goal 3: likely discount / promotional offers
    """
    # Simple logic: 
    # High loyalty -> High Discount
    # At Risk (High recency) -> High Discount
    # Recent purchase (Low recency) -> Low Discount
    
    # Calculate recency again if needed, or reuse from somewhere. 
    # For speed, we'll just use customers 'last_purchase_date'
    
    today = pd.to_datetime('today')
    customers['days_since_last'] = (today - pd.to_datetime(customers['last_purchase_date'])).dt.days
    
    def recommend_discount(row):
        base_discount = 0.05
        
        # Loyalty boost
        if row['loyalty_status'] == 'Platinum': base_discount += 0.15
        elif row['loyalty_status'] == 'Gold': base_discount += 0.10
        elif row['loyalty_status'] == 'Silver': base_discount += 0.05
        
        # Retention boost
        if row['days_since_last'] > 90: base_discount += 0.10
        
        return min(base_discount, 0.40) # Max 40%
        
    customers['recommended_discount'] = customers.apply(recommend_discount, axis=1)
    
    return customers[['customer_id', 'first_name', 'loyalty_status', 'days_since_last', 'recommended_discount']]
