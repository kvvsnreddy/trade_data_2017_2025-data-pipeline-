# main_pipeline.py
import pandas as pd
from src.parsing.parse_goods_description import parse_goods_description
from src.cleaning.clean_base import clean_data
from src.feature_engineering.features import add_features
from src.db.load_to_db import load_to_database

def run_pipeline():
    """Complete pipeline execution"""
    print("Starting data pipeline...")
    
    # Load raw data
    print("Loading raw data...")
    df = pd.read_excel("data/raw/Sample Data 2.xlsx")
    print(f"Loaded {len(df)} records")
    
    # Clean data
    print("Cleaning data...")
    df = clean_data(df)
    
    # Parse goods description
    print("Parsing goods description...")
    df = parse_goods_description(df)
    
    # Add features
    print("Adding features...")
    df = add_features(df)
    
    # Save processed data
    print("Saving processed data...")
    df.to_csv("data/processed/trade_cleaned.csv", index=False)
    
    # Load to database
    print("Loading to database...")
    load_to_database(df)
    
    print("Pipeline completed successfully!")
    
    # Summary
    print(f"\nSummary:")
    print(f"- Total records processed: {len(df)}")
    print(f"- Date range: {df['date_of_shipment'].min()} to {df['date_of_shipment'].max()}")
    print(f"- Categories found: {df['category'].nunique()}")
    print(f"- Unique suppliers: {df['supplier_name'].nunique()}")
    print(f"- Total business value: ₹{df['grand_total_inr'].sum():,.2f}")

if __name__ == "__main__":
    run_pipeline()