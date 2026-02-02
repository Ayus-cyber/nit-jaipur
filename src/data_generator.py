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
            "current_stock_level": np.random.randint(0, 100)
        })
    df_products = pd.DataFrame(products)
    df_products.to_csv(f"{base_path}/products.csv", index=False)
    print("Products generated.")

    # 3. Generate Basic Customer Info (Initialize)
    num_customers = 200
    customers = []
    segments = ['HS', 'AR', 'New', 'Loyal'] 
    loyalty_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    
    for i in range(num_customers):
        join_date = fake.date_between(start_date='-2y', end_date='today')
        customers.append({
            "customer_id": i + 1,
            "first_name": fake.first_name(),
            "email": fake.email(),
            "segment_id": np.random.choice(segments),
            "customer_phone": fake.phone_number(),
            "customer_since": join_date,
            "join_date_obj": join_date # temp for logic
        })
    
    # 4. Generate Sales Line Items (store_sales_line_items)
    sales_data = []
    num_transactions = 2000
    
    today = datetime.now().date()
    
    for i in range(num_transactions):
        cust = random.choice(customers)
        prod = random.choice(products)
        store = random.choice(stores)
        
        # Ensure transaction is after customer joined
        start_date = cust["join_date_obj"]
        days_active = (today - start_date).days
        
        if days_active <= 0:
            txn_date = start_date
        else:
            txn_date = start_date + timedelta(days=np.random.randint(0, days_active))
            
        qty = np.random.randint(1, 5)
        price_paid = prod["standard_price"] * qty * np.random.uniform(0.8, 1.0)
        
        sales_data.append({
            "transaction_id": i + 1,
            "date": txn_date,
            "customer_id": cust["customer_id"],
            "product_id": prod["product_id"],
            "store_id": store["store_id"],
            "quantity": qty,
            "total_amount": round(price_paid, 2)
        })
    
    df_sales = pd.DataFrame(sales_data)
    df_sales.to_csv(f"{base_path}/store_sales_line_items.csv", index=False)
    print("Sales generated.")

    # 5. Enrich Customers with Derived Data (Loyalty, Last Purchase)
    for cust in customers:
        cust_sales = [s for s in sales_data if s["customer_id"] == cust["customer_id"]]
        
        if cust_sales:
            last_purchase = max(s["date"] for s in cust_sales)
            total_spend = sum(s["total_amount"] for s in cust_sales)
            # 1 point per $10 spent + random bonus
            points = int(total_spend / 10) + np.random.randint(0, 50)
            
            # Update loyalty status based on points
            if points > 1000: tier = 'Platinum'
            elif points > 500: tier = 'Gold'
            elif points > 200: tier = 'Silver'
            else: tier = 'Bronze'
        else:
            last_purchase = cust["join_date_obj"] # No purchase yet
            points = 0
            tier = 'Bronze'
            
        cust["last_purchase_date"] = last_purchase
        cust["total_loyalty_points"] = points
        cust["loyalty_status"] = tier
        
        del cust["join_date_obj"] # cleanup
        
    df_customers = pd.DataFrame(customers)
    
    # Reorder columns to match logical flow
    cols = ["customer_id", "first_name", "email", "customer_phone", "customer_since", 
            "loyalty_status", "total_loyalty_points", "last_purchase_date", "segment_id"]
    df_customers = df_customers[cols]
    
    df_customers.to_csv(f"{base_path}/customer_details.csv", index=False)
    print("Customers generated (refined).")

    # 6. Generate Promotions
    promotions = [
        {"promotion_id": 1, "promotion_name": "Summer Sale", "start_date": "2025-06-01", "end_date": "2025-06-15", "discount_percentage": 0.20, "applicable_category": "Apparel"},
        {"promotion_id": 2, "promotion_name": "Tech Fest", "start_date": "2025-09-01", "end_date": "2025-09-10", "discount_percentage": 0.15, "applicable_category": "Electronics"},
        {"promotion_id": 3, "promotion_name": "Clearance", "start_date": "2025-11-20", "end_date": "2025-11-30", "discount_percentage": 0.50, "applicable_category": "All"},
        {"promotion_id": 4, "promotion_name": "Loyalty Bonus", "start_date": "2025-01-01", "end_date": "2025-12-31", "discount_percentage": 0.05, "applicable_category": "All"}
    ]
    df_promo = pd.DataFrame(promotions)
    df_promo.to_csv(f"{base_path}/promotion_details.csv", index=False)
    
    # 7. Loyalty Rules
    rules = [
        {"rule_id": 1, "rule_name": "Standard Earning", "details": "1 point per $1"},
        {"rule_id": 2, "rule_name": "Weekend Bonus", "details": "2x points on weekends"}
    ]
    df_rules = pd.DataFrame(rules)
    df_rules.to_csv(f"{base_path}/loyalty_rules.csv", index=False)
    print("Promotions and Rules generated.")

if __name__ == "__main__":
    generate_data()
