import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
np.random.seed(42)
random.seed(42)

def generate_data(base_path="data"):
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    print("Generating data...")

    # 1. Generate Stores
    num_stores = 5
    stores = []
    for i in range(num_stores):
        stores.append({
            "store_id": i + 1,
            "store_name": f"Store_{fake.city()}",
            "location": fake.state(),
            "size_sqft": np.random.randint(1000, 5000)
        })
    df_stores = pd.DataFrame(stores)
    df_stores.to_csv(f"{base_path}/stores.csv", index=False)
    print("Stores generated.")

    # 2. Generate Products
    categories = ['Electronics', 'Apparel', 'Home', 'Beauty', 'Sports']
    num_products = 50
    products = []
    for i in range(num_products):
        cat = np.random.choice(categories)
        products.append({
            "product_id": i + 1,
            "product_name": f"{cat}_Item_{i}",
            "category": cat,
            "standard_price": round(np.random.uniform(10, 500), 2),
            "current_stock_level": np.random.randint(0, 100) # Some with 0 for inventory analysis
        })
    df_products = pd.DataFrame(products)
    df_products.to_csv(f"{base_path}/products.csv", index=False)
    print("Products generated.")

    # 3. Generate Customers (customer_details)
    num_customers = 200
    customers = []
    segments = ['HS', 'AR', 'New', 'Loyal'] # HS=High Spender, AR=At Risk?
    loyalty_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    
    for i in range(num_customers):
        join_date = fake.date_between(start_date='-2y', end_date='today')
        customers.append({
            "customer_id": i + 1,
            "first_name": fake.first_name(),
            "email": fake.email(),
            "loyalty_status": np.random.choice(loyalty_tiers, p=[0.5, 0.3, 0.15, 0.05]),
            "total_loyalty_points": np.random.randint(0, 5000),
            "last_purchase_date": fake.date_between(start_date='-6m', end_date='today'),
            "segment_id": np.random.choice(segments),
            "Customer_phone": fake.phone_number(),
            "Customer_since": join_date
        })
    df_customers = pd.DataFrame(customers)
    df_customers.to_csv(f"{base_path}/customer_details.csv", index=False)
    print("Customers generated.")

    # 4. Generate Sales Line Items (store_sales_line_items)
    # create transactions over last year
    sales_data = []
    num_transactions = 2000
    
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(num_transactions):
        txn_date = start_date + timedelta(days=np.random.randint(0, 365))
        cust = random.choice(customers)
        prod = random.choice(products)
        store = random.choice(stores)
        
        qty = np.random.randint(1, 5)
        # Price paid might include discount
        price_paid = prod["standard_price"] * qty * np.random.uniform(0.8, 1.0)
        
        sales_data.append({
            "transaction_id": i + 1,
            "date": txn_date.date(),
            "customer_id": cust["customer_id"],
            "product_id": prod["product_id"],
            "store_id": store["store_id"],
            "quantity": qty,
            "total_amount": round(price_paid, 2)
        })
    
    df_sales = pd.DataFrame(sales_data)
    df_sales.to_csv(f"{base_path}/store_sales_line_items.csv", index=False)
    print("Sales generated.")

    # 5. Generate Promotions (promotion_details)
    promotions = [
        {"promotion_id": 1, "promotion_name": "Summer Sale", "start_date": "2025-06-01", "end_date": "2025-06-15", "discount_percentage": 0.20, "applicable_category": "Apparel"},
        {"promotion_id": 2, "promotion_name": "Tech Fest", "start_date": "2025-09-01", "end_date": "2025-09-10", "discount_percentage": 0.15, "applicable_category": "Electronics"},
        {"promotion_id": 3, "promotion_name": "Clearance", "start_date": "2025-11-20", "end_date": "2025-11-30", "discount_percentage": 0.50, "applicable_category": "All"},
        {"promotion_id": 4, "promotion_name": "Loyalty Bonus", "start_date": "2025-01-01", "end_date": "2025-12-31", "discount_percentage": 0.05, "applicable_category": "All"}
    ]
    df_promo = pd.DataFrame(promotions)
    df_promo.to_csv(f"{base_path}/promotion_details.csv", index=False)
    
    # 6. Loyalty Rules
    rules = [
        {"rule_id": 1, "rule_name": "Standard Earning", "details": "1 point per $1"},
        {"rule_id": 2, "rule_name": "Weekend Bonus", "details": "2x points on weekends"}
    ]
    df_rules = pd.DataFrame(rules)
    df_rules.to_csv(f"{base_path}/loyalty_rules.csv", index=False)
    print("Promotions and Rules generated.")

if __name__ == "__main__":
    generate_data()
