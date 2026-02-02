# Inventory & Store Performance Analytics Setup

## Overview
This project analyzes the correlation between store inventory levels and customer purchasing behavior. It includes a data generation module, a predictive modeling engine, and an interactive dashboard.

### Goals Covered
1.  **Inventory-Sales Correlation**: Analyze how stock levels drive sales.
2.  **Future Spend Prediction**: Estimate customer value for the next quarter.
3.  **Promotional Targeting**: Recommend discounts based on loyalty and behavior.
4.  **Sensitivity Analysis**: Identify customers at risk due to stockouts.
5.  **Optimization Impact**: Simulate revenue uplift from better inventory management.

## Project Structure
```
├── data/                   # Generated mock data files
├── src/
│   ├── data_generator.py   # Script to create synthetic data
│   ├── analysis.py         # Statistical analysis logic
│   ├── models.py           # Machine learning models (Random Forest)
│   ├── dashboard.py        # Streamlit dashboard app
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3.8+ installed.
```bash
pip install -r requirements.txt
```

### 2. Generate Data
Run the data generator to create the CSV files in the `data/` directory.
```bash
python src/data_generator.py
```

### 3. Run Dashboard
Launch the Streamlit application.
```bash
streamlit run src/dashboard.py
```

## Dashboard Features
- **Overview**: High-level sales and customer KPIs.
- **Inventory Correlation**: Interactive scatter plots showing the relationship between stock availability and sales velocity.
- **Customer Predictions**: ML-driven predictions for future customer spending.
- **Promo Recommendations**: Automated logic for assigning discount tiers.
- **Optimization Simulations**: "What-if" analysis for inventory planning.
